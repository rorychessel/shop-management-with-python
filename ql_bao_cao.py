import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from connection import connect_db
from datetime import datetime

# Hàm tính tổng doanh thu
def tinh_tong_doanh_thu():
    connection = connect_db()
    if connection is None:
        return 0
    try:
        cursor = connection.cursor()
        query = """
            SELECT COALESCE(SUM(tong_tien), 0)
            FROM don_hang
            WHERE tthai_thanh_toan = 'Đã thanh toán' AND tthai_van_don = 'Đã giao'
        """
        cursor.execute(query)
        return cursor.fetchone()[0]
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tính tổng doanh thu: {e}")
        return 0
    finally:
        cursor.close()
        connection.close()

# Hàm tính tổng chi phí nhập hàng
def tinh_tong_chi_phi_nhap_hang():
    connection = connect_db()
    if connection is None:
        return 0
    try:
        cursor = connection.cursor()
        query = """
            SELECT COALESCE(SUM(tong_tien), 0)
            FROM phieu_nhap
        """
        cursor.execute(query)
        return cursor.fetchone()[0]
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tính tổng chi phí nhập hàng: {e}")
        return 0
    finally:
        cursor.close()
        connection.close()

# Hàm tính lãi/lỗ
def tinh_lai_lo():
    connection = connect_db()
    if connection is None:
        return 0
    try:
        cursor = connection.cursor()
        # Tính tổng doanh thu
        cursor.execute("""
            SELECT COALESCE(SUM(tong_tien), 0)
            FROM don_hang
            WHERE tthai_thanh_toan = 'Đã thanh toán' AND tthai_van_don = 'Đã giao'
        """)
        doanh_thu = cursor.fetchone()[0]
        
        # Tính tổng chi phí nhập hàng dựa trên giá nhập
        cursor.execute("""
            SELECT COALESCE(SUM(pnsp.gia_nhap * pnsp.so_luong), 0)
            FROM phieu_nhap_san_pham pnsp
            JOIN phieu_nhap pn ON pnsp.ma_phieu_nhap = pn.ma_phieu_nhap
        """)
        chi_phi = cursor.fetchone()[0]
        
        return doanh_thu - chi_phi
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tính lãi/lỗ: {e}")
        return 0
    finally:
        cursor.close()
        connection.close()

# Hàm lấy danh sách khách hàng tiềm năng (top 5 khách hàng có số đơn hàng nhiều nhất)
def lay_khach_hang_tiem_nang():
    connection = connect_db()
    if connection is None:
        return []
    try:
        cursor = connection.cursor()
        query = """
            SELECT kh.ma_khach_hang, kh.ho_ten, COUNT(dh.ma_don_hang) as so_lan_mua
            FROM khach_hang kh
            LEFT JOIN don_hang dh ON kh.ma_khach_hang = dh.ma_khach_hang
            WHERE dh.tthai_thanh_toan = 'Đã thanh toán' AND dh.tthai_van_don = 'Đã giao'
            GROUP BY kh.ma_khach_hang, kh.ho_ten
            ORDER BY so_lan_mua DESC
            LIMIT 5
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi lấy khách hàng tiềm năng: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# Hàm lấy danh sách sản phẩm bán chạy (top 5 sản phẩm có số lượng bán cao nhất)
def lay_san_pham_ban_chay():
    connection = connect_db()
    if connection is None:
        return []
    try:
        cursor = connection.cursor()
        query = """
            SELECT sp.ma_san_pham, sp.ten, COALESCE(SUM(dhsp.so_luong), 0) as tong_so_luong
            FROM san_pham sp
            LEFT JOIN don_hang_san_pham dhsp ON sp.ma_san_pham = dhsp.ma_san_pham
            LEFT JOIN don_hang dh ON dhsp.ma_don_hang = dh.ma_don_hang
            WHERE dh.tthai_thanh_toan = 'Đã thanh toán' AND dh.tthai_van_don = 'Đã giao'
            GROUP BY sp.ma_san_pham, sp.ten
            ORDER BY tong_so_luong DESC
            LIMIT 5
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi lấy sản phẩm bán chạy: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# Form báo cáo doanh thu
def show_bao_cao_doanh_thu(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Báo cáo doanh thu", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame hiển thị tổng doanh thu
    summary_frame = tk.LabelFrame(main_frame, text="Tổng quan", font=("Arial", 12))
    summary_frame.pack(pady=10, fill="x")

    tk.Label(summary_frame, text=f"Tổng doanh thu: {tinh_tong_doanh_thu():,.0f} VNĐ").pack(pady=5)
    lai_lo = tinh_lai_lo()
    tk.Label(summary_frame, text=f"Lãi/Lỗ: {lai_lo:,.0f} VNĐ", fg="green" if lai_lo >= 0 else "red").pack(pady=5)

    # Frame hiển thị kết quả
    result_frame = tk.LabelFrame(main_frame, text="Danh sách doanh thu", font=("Arial", 12))
    result_frame.pack(pady=10, fill="both", expand=True)

    columns = ("Mã đơn hàng", "Ngày đặt", "Tổng tiền", "Trạng thái thanh toán", "Trạng thái vận đơn")
    tree = ttk.Treeview(result_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Hàm cập nhật danh sách doanh thu
    def cap_nhat_doanh_thu():
        for item in tree.get_children():
            tree.delete(item)
        connection = connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    SELECT ma_don_hang, ngay_dat, tong_tien, tthai_thanh_toan, tthai_van_don
                    FROM don_hang
                    WHERE tthai_thanh_toan = 'Đã thanh toán' AND tthai_van_don = 'Đã giao'
                """
                cursor.execute(query)
                doanh_thu = cursor.fetchall()
                for row in doanh_thu:
                    tree.insert("", tk.END, values=row)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi lấy dữ liệu doanh thu: {e}")
            finally:
                cursor.close()
                connection.close()

    # Hàm vẽ biểu đồ doanh thu theo tháng
    def ve_bieu_do_doanh_thu():
        connection = connect_db()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            query = """
                SELECT DATE_FORMAT(ngay_dat, '%Y-%m') AS thang, COALESCE(SUM(tong_tien), 0)
                FROM don_hang
                WHERE tthai_thanh_toan = 'Đã thanh toán' AND tthai_van_don = 'Đã giao'
                GROUP BY thang
                ORDER BY thang
            """
            cursor.execute(query)
            data = cursor.fetchall()
            
            months = [row[0] for row in data]
            revenues = [row[1] for row in data]
            
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(months, revenues, color='skyblue')
            ax.set_xlabel('Tháng')
            ax.set_ylabel('Doanh thu (VNĐ)')
            ax.set_title('Biểu đồ doanh thu theo tháng')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            new_window = tk.Toplevel(window)
            new_window.title("Biểu đồ doanh thu")
            canvas = FigureCanvasTkAgg(fig, master=new_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi vẽ biểu đồ doanh thu: {e}")
        finally:
            cursor.close()
            connection.close()

    cap_nhat_doanh_thu()

    tk.Button(main_frame, text="Làm mới", command=cap_nhat_doanh_thu).pack(pady=5)
    tk.Button(main_frame, text="Vẽ biểu đồ doanh thu", command=ve_bieu_do_doanh_thu).pack(pady=5)
    tk.Button(main_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).pack(pady=5)

# Form báo cáo chi phí nhập hàng
def show_bao_cao_chi_phi_nhap_hang(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Báo cáo chi phí nhập hàng", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame hiển thị tổng chi phí
    summary_frame = tk.LabelFrame(main_frame, text="Tổng quan", font=("Arial", 12))
    summary_frame.pack(pady=10, fill="x")

    tk.Label(summary_frame, text=f"Tổng chi phí nhập hàng: {tinh_tong_chi_phi_nhap_hang():,.0f} VNĐ").pack(pady=5)

    # Frame hiển thị kết quả
    result_frame = tk.LabelFrame(main_frame, text="Danh sách chi phí", font=("Arial", 12))
    result_frame.pack(pady=10, fill="both", expand=True)

    columns = ("Mã phiếu nhập", "Ngày nhập", "Tổng chi phí", "Nhà cung cấp")
    tree = ttk.Treeview(result_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Hàm cập nhật danh sách chi phí
    def cap_nhat_chi_phi():
        for item in tree.get_children():
            tree.delete(item)
        connection = connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    SELECT ma_phieu_nhap, ngay_nhap, tong_tien, nha_cung_cap
                    FROM phieu_nhap
                """
                cursor.execute(query)
                chi_phi = cursor.fetchall()
                for row in chi_phi:
                    tree.insert("", tk.END, values=row)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi lấy dữ liệu chi phí: {e}")
            finally:
                cursor.close()
                connection.close()

    # Hàm vẽ biểu đồ chi phí nhập hàng theo tháng
    def ve_bieu_do_chi_phi():
        connection = connect_db()
        if not connection:
            return
        try:
            cursor = connection.cursor()
            query = """
                SELECT DATE_FORMAT(ngay_nhap, '%Y-%m') AS thang, COALESCE(SUM(tong_tien), 0)
                FROM phieu_nhap
                GROUP BY thang
                ORDER BY thang
            """
            cursor.execute(query)
            data = cursor.fetchall()
            
            months = [row[0] for row in data]
            costs = [row[1] for row in data]
            
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(months, costs, color='salmon')
            ax.set_xlabel('Tháng')
            ax.set_ylabel('Chi phí (VNĐ)')
            ax.set_title('Biểu đồ chi phí nhập hàng theo tháng')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            new_window = tk.Toplevel(window)
            new_window.title("Biểu đồ chi phí nhập hàng")
            canvas = FigureCanvasTkAgg(fig, master=new_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi vẽ biểu đồ chi phí: {e}")
        finally:
            cursor.close()
            connection.close()

    cap_nhat_chi_phi()

    tk.Button(main_frame, text="Làm mới", command=cap_nhat_chi_phi).pack(pady=5)
    tk.Button(main_frame, text="Vẽ biểu đồ chi phí", command=ve_bieu_do_chi_phi).pack(pady=5)
    tk.Button(main_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).pack(pady=5)

# Form báo cáo khách hàng
def show_bao_cao_khach_hang(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Báo cáo khách hàng", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame hiển thị khách hàng tiềm năng
    potential_frame = tk.LabelFrame(main_frame, text="Khách hàng tiềm năng", font=("Arial", 12))
    potential_frame.pack(pady=10, fill="both", expand=True)

    columns_potential = ("Mã khách hàng", "Tên", "Số lần mua")
    tree_potential = ttk.Treeview(potential_frame, columns=columns_potential, show="headings")
    
    for col in columns_potential:
        tree_potential.heading(col, text=col)
        tree_potential.column(col, width=120, anchor="center")
    
    scrollbar_potential = ttk.Scrollbar(potential_frame, orient="vertical", command=tree_potential.yview)
    tree_potential.configure(yscroll=scrollbar_potential.set)
    
    tree_potential.pack(side="left", fill="both", expand=True)
    scrollbar_potential.pack(side="right", fill="y")

    # Hàm cập nhật danh sách khách hàng tiềm năng
    def cap_nhat_khach_hang_tiem_nang():
        for item in tree_potential.get_children():
            tree_potential.delete(item)
        khach_hangs = lay_khach_hang_tiem_nang()
        for row in khach_hangs:
            tree_potential.insert("", tk.END, values=row)

    cap_nhat_khach_hang_tiem_nang()

    # Hàm vẽ biểu đồ khách hàng tiềm năng
    def ve_bieu_do_khach_hang():
        khach_hangs = lay_khach_hang_tiem_nang()
        if not khach_hangs:
            messagebox.showinfo("Thông báo", "Không có khách hàng tiềm năng để hiển thị!")
            return
        
        names = [row[1] for row in khach_hangs]
        so_lan_mua = [row[2] for row in khach_hangs]
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(names, so_lan_mua, color='lightgreen')
        ax.set_xlabel('Khách hàng')
        ax.set_ylabel('Số lần mua')
        ax.set_title('Biểu đồ khách hàng tiềm năng (Top 5)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        new_window = tk.Toplevel(window)
        new_window.title("Biểu đồ khách hàng tiềm năng")
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # Frame hiển thị sản phẩm bán chạy
    product_frame = tk.LabelFrame(main_frame, text="Sản phẩm bán chạy", font=("Arial", 12))
    product_frame.pack(pady=10, fill="both", expand=True)

    columns_product = ("Mã sản phẩm", "Tên", "Tổng số lượng bán")
    tree_product = ttk.Treeview(product_frame, columns=columns_product, show="headings")
    
    for col in columns_product:
        tree_product.heading(col, text=col)
        tree_product.column(col, width=120, anchor="center")
    
    scrollbar_product = ttk.Scrollbar(product_frame, orient="vertical", command=tree_product.yview)
    tree_product.configure(yscroll=scrollbar_product.set)
    
    tree_product.pack(side="left", fill="both", expand=True)
    scrollbar_product.pack(side="right", fill="y")

    # Hàm cập nhật danh sách sản phẩm bán chạy
    def cap_nhat_san_pham_ban_chay():
        for item in tree_product.get_children():
            tree_product.delete(item)
        san_phams = lay_san_pham_ban_chay()
        for row in san_phams:
            tree_product.insert("", tk.END, values=row)

    # Hàm vẽ biểu đồ sản phẩm bán chạy
    def ve_bieu_do_san_pham():
        san_phams = lay_san_pham_ban_chay()
        if not san_phams:
            messagebox.showinfo("Thông báo", "Không có sản phẩm bán chạy để hiển thị!")
            return
        
        names = [row[1] for row in san_phams]
        quantities = [row[2] for row in san_phams]
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(names, quantities, color='lightcoral')
        ax.set_xlabel('Sản phẩm')
        ax.set_ylabel('Tổng số lượng bán')
        ax.set_title('Biểu đồ sản phẩm bán chạy (Top 5)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        new_window = tk.Toplevel(window)
        new_window.title("Biểu đồ sản phẩm bán chạy")
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    cap_nhat_san_pham_ban_chay()

    tk.Button(main_frame, text="Làm mới khách hàng", command=cap_nhat_khach_hang_tiem_nang).pack(pady=5)
    tk.Button(main_frame, text="Vẽ biểu đồ khách hàng", command=ve_bieu_do_khach_hang).pack(pady=5)
    tk.Button(main_frame, text="Làm mới sản phẩm", command=cap_nhat_san_pham_ban_chay).pack(pady=5)
    tk.Button(main_frame, text="Vẽ biểu đồ sản phẩm", command=ve_bieu_do_san_pham).pack(pady=5)
    tk.Button(main_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).pack(pady=5)