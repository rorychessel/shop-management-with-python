import tkinter as tk
from tkinter import ttk, messagebox
from connection import connect_db

# Hàm lấy danh sách sản phẩm
def lay_danh_sach_san_pham():
    connection = connect_db()
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor()
        query = "SELECT ma_san_pham, ten, kich_co, gia_ban, so_luong_ton_kho FROM san_pham"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách sản phẩm: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# Form tra cứu số lượng hàng tồn kho
def show_tra_cuu_ton_kho_form(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Tra cứu số lượng hàng tồn kho", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame hiển thị kết quả
    result_frame = tk.LabelFrame(main_frame, text="Danh sách sản phẩm", font=("Arial", 12))
    result_frame.pack(pady=10, fill="both", expand=True)

    columns = ("Mã SP", "Tên", "Kích cỡ", "Giá bán", "Số lượng tồn")
    tree = ttk.Treeview(result_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Cập nhật danh sách sản phẩm
    def cap_nhat_danh_sach_san_pham():
        for item in tree.get_children():
            tree.delete(item)
        products = lay_danh_sach_san_pham()
        for product in products:
            tree.insert("", tk.END, values=product)

    cap_nhat_danh_sach_san_pham()

    tk.Button(main_frame, text="Làm mới", command=cap_nhat_danh_sach_san_pham).pack(pady=5)
    tk.Button(main_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).pack(pady=5)

# Form thêm phiếu nhập
def show_them_phieu_nhap_form(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Thêm phiếu nhập", font=("Arial", 14))
    label_title.pack(pady=10)

    # Lấy mã nhân viên hiện tại
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT ma_nhan_su FROM nhan_su WHERE id_tai_khoan = (SELECT id_tai_khoan FROM tai_khoan WHERE ten_dang_nhap = %s)"
            cursor.execute(query, (current_user,))
            ma_ns_nhap_hang = cursor.fetchone()[0]
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy mã nhân viên: {e}")
            ma_ns_nhap_hang = None
        finally:
            cursor.close()
            connection.close()

    # Các trường nhập liệu
    form_frame = tk.Frame(main_frame)
    form_frame.pack(pady=10)

    fields = ["Giờ nhập (HH:MM:SS)", "Ngày nhập (YYYY-MM-DD)", "Nhà cung cấp"]
    entries = {}

    for idx, field in enumerate(fields):
        tk.Label(form_frame, text=field + ":").grid(row=idx, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(form_frame)
        if field == "Giờ nhập (HH:MM:SS)":
            entry.insert(0, "")  # Để trống
        elif field == "Ngày nhập (YYYY-MM-DD)":
            entry.insert(0, "")  # Để trống
        elif field == "Nhà cung cấp":
            entry.insert(0, "")  # Để trống
        entry.grid(row=idx, column=1, padx=5, pady=5, sticky="ew")
        entries[field] = entry

    form_frame.grid_columnconfigure(1, weight=1)

    # Frame chọn sản phẩm
    product_frame = tk.LabelFrame(main_frame, text="Chọn sản phẩm", font=("Arial", 12))
    product_frame.pack(pady=10, fill="both", expand=True)

    columns = ("Mã SP", "Tên", "Kích cỡ", "Giá nhập", "Số lượng nhập")
    tree = ttk.Treeview(product_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    
    scrollbar = ttk.Scrollbar(product_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    selected_products = []

    # Cập nhật danh sách sản phẩm
    def cap_nhat_danh_sach_san_pham():
        for item in tree.get_children():
            tree.delete(item)
        products = lay_danh_sach_san_pham()
        for product in products:
            tree.insert("", tk.END, values=product[:3] + (0, 0))

    cap_nhat_danh_sach_san_pham()

    # Hàm chọn giá nhập và số lượng
    def chon_gia_so_luong(event):
        item = tree.selection()
        if not item:
            return
        item = item[0]
        ma_san_pham = tree.item(item, "values")[0]

        new_window = tk.Toplevel(window)
        new_window.title("Chọn giá và số lượng")
        new_window.geometry("300x200")

        tk.Label(new_window, text=f"Sản phẩm mã {ma_san_pham}:").pack(pady=10)
        tk.Label(new_window, text="Giá nhập:").pack(pady=5)
        entry_gia = tk.Entry(new_window)
        entry_gia.insert(0, str(tree.item(item, "values")[3] or 0))
        entry_gia.pack(pady=5)
        tk.Label(new_window, text="Số lượng nhập:").pack(pady=5)
        entry_so_luong = tk.Entry(new_window)
        entry_so_luong.insert(0, str(tree.item(item, "values")[4] or 0))
        entry_so_luong.pack(pady=5)

        def luu_gia_so_luong():
            gia = entry_gia.get()
            so_luong = entry_so_luong.get()
            if not (gia.isdigit() and so_luong.isdigit()) or int(gia) < 0 or int(so_luong) <= 0:
                messagebox.showwarning("Lỗi", "Giá nhập phải là số không âm và số lượng phải là số nguyên dương!")
                return
            gia = int(gia)
            so_luong = int(so_luong)

            current_values = list(tree.item(item, "values"))
            current_values[3] = gia
            current_values[4] = so_luong
            tree.item(item, values=tuple(current_values))

            product = current_values
            found = False
            for i, p in enumerate(selected_products):
                if p[0] == ma_san_pham:
                    if so_luong > 0:
                        selected_products[i] = product
                    else:
                        selected_products.pop(i)
                    found = True
                    break
            if not found and so_luong > 0:
                selected_products.append(product)

            new_window.destroy()

        tk.Button(new_window, text="Lưu", command=luu_gia_so_luong).pack(pady=5)
        tk.Button(new_window, text="Hủy", command=new_window.destroy).pack(pady=5)

    tree.bind("<Double-1>", chon_gia_so_luong)

    # Hàm xử lý thêm phiếu nhập
    def handle_them_phieu_nhap():
        gio_nhap = entries["Giờ nhập (HH:MM:SS)"].get()
        ngay_nhap = entries["Ngày nhập (YYYY-MM-DD)"].get()
        nha_cung_cap = entries["Nhà cung cấp"].get()

        if not all([gio_nhap, ngay_nhap, nha_cung_cap]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
            return

        if not selected_products or all(p[4] == 0 for p in selected_products):
            messagebox.showwarning("Lỗi", "Vui lòng chọn ít nhất một sản phẩm với số lượng lớn hơn 0!")
            return

        if ma_ns_nhap_hang is None:
            messagebox.showerror("Lỗi", "Không thể xác định mã nhân viên!")
            return

        connection = connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO phieu_nhap (gio_nhap, ngay_nhap, nha_cung_cap, tong_tien, ma_ns_nhan)
                    VALUES (%s, %s, %s, 0, %s)
                """, (gio_nhap, ngay_nhap, nha_cung_cap, ma_ns_nhap_hang))
                ma_phieu_nhap = cursor.lastrowid

                for product in selected_products:
                    if product[4] and int(product[4]) > 0:
                        so_luong = int(product[4])
                        gia_nhap = int(product[3])
                        thanh_tien = gia_nhap * so_luong
                        cursor.execute("""
                            INSERT INTO phieu_nhap_san_pham (ma_phieu_nhap, ma_san_pham, gia_nhap, so_luong)
                            VALUES (%s, %s, %s, %s)
                        """, (ma_phieu_nhap, product[0], gia_nhap, so_luong))

                        cursor.execute("""
                            UPDATE san_pham 
                            SET so_luong_ton_kho = so_luong_ton_kho + %s
                            WHERE ma_san_pham = %s
                        """, (so_luong, product[0]))

                connection.commit()
                messagebox.showinfo("Thành công", f"Đã thêm phiếu nhập mã {ma_phieu_nhap} thành công!")
                selected_products.clear()
                cap_nhat_danh_sach_san_pham()
                for entry in entries.values():
                    entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm phiếu nhập: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    tk.Button(form_frame, text="Thêm phiếu nhập", command=handle_them_phieu_nhap).grid(row=len(fields), column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)

# Form sửa phiếu nhập
def show_sua_phieu_nhap_form(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Sửa phiếu nhập", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame tìm kiếm phiếu nhập
    search_frame = tk.LabelFrame(main_frame, text="Tìm kiếm phiếu nhập", font=("Arial", 12))
    search_frame.pack(pady=10, fill="x")

    tk.Label(search_frame, text="Mã phiếu nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_ma_phieu = tk.Entry(search_frame)
    entry_ma_phieu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    search_frame.grid_columnconfigure(1, weight=1)

    # Frame thông tin phiếu nhập
    form_frame = tk.LabelFrame(main_frame, text="Thông tin phiếu nhập", font=("Arial", 12))
    form_frame.pack(pady=10, fill="x")

    fields = ["Giờ nhập (HH:MM:SS)", "Ngày nhập (YYYY-MM-DD)", "Nhà cung cấp"]
    entries = {}

    for idx, field in enumerate(fields):
        tk.Label(form_frame, text=field + ":").grid(row=idx, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(form_frame)
        entry.grid(row=idx, column=1, padx=5, pady=5, sticky="ew")
        entries[field] = entry
    form_frame.grid_columnconfigure(1, weight=1)

    # Frame chọn sản phẩm
    product_frame = tk.LabelFrame(main_frame, text="Sản phẩm trong phiếu nhập", font=("Arial", 12))
    product_frame.pack(pady=10, fill="both", expand=True)

    columns = ("Mã SP", "Tên", "Kích cỡ", "Giá nhập", "Số lượng nhập")
    tree = ttk.Treeview(product_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    
    scrollbar = ttk.Scrollbar(product_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    selected_products = []

    # Hàm tìm kiếm phiếu nhập
    def tim_kiem_phieu_nhap():
        ma_phieu = entry_ma_phieu.get()
        if not ma_phieu:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã phiếu nhập!")
            return

        connection = connect_db()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            query = """
                SELECT gio_nhap, ngay_nhap, nha_cung_cap
                FROM phieu_nhap
                WHERE ma_phieu_nhap = %s
            """
            cursor.execute(query, (ma_phieu,))
            phieu_nhap = cursor.fetchone()

            if not phieu_nhap:
                messagebox.showwarning("Không tìm thấy", "Không tìm thấy phiếu nhập với mã này!")
                return

            entries["Giờ nhập (HH:MM:SS)"].delete(0, tk.END)
            entries["Giờ nhập (HH:MM:SS)"].insert(0, phieu_nhap[0])
            entries["Ngày nhập (YYYY-MM-DD)"].delete(0, tk.END)
            entries["Ngày nhập (YYYY-MM-DD)"].insert(0, phieu_nhap[1])
            entries["Nhà cung cấp"].delete(0, tk.END)
            entries["Nhà cung cấp"].insert(0, phieu_nhap[2])

            # Lấy danh sách sản phẩm
            query_san_pham = """
                SELECT sp.ma_san_pham, sp.ten, sp.kich_co, pnsp.gia_nhap, pnsp.so_luong
                FROM phieu_nhap_san_pham pnsp
                JOIN san_pham sp ON pnsp.ma_san_pham = sp.ma_san_pham
                WHERE pnsp.ma_phieu_nhap = %s
            """
            cursor.execute(query_san_pham, (ma_phieu,))
            products = cursor.fetchall()

            for item in tree.get_children():
                tree.delete(item)
            selected_products.clear()
            for product in products:
                tree.insert("", tk.END, values=product)
                selected_products.append(list(product))

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm phiếu nhập: {e}")
        finally:
            cursor.close()
            connection.close()

    # Hàm chọn giá nhập và số lượng
    def chon_gia_so_luong(event):
        item = tree.selection()
        if not item:
            return
        item = item[0]
        ma_san_pham = tree.item(item, "values")[0]

        new_window = tk.Toplevel(window)
        new_window.title("Chọn giá và số lượng")
        new_window.geometry("300x200")

        tk.Label(new_window, text=f"Sản phẩm mã {ma_san_pham}:").pack(pady=10)
        tk.Label(new_window, text="Giá nhập:").pack(pady=5)
        entry_gia = tk.Entry(new_window)
        entry_gia.insert(0, str(tree.item(item, "values")[3] or 0))
        entry_gia.pack(pady=5)
        tk.Label(new_window, text="Số lượng nhập:").pack(pady=5)
        entry_so_luong = tk.Entry(new_window)
        entry_so_luong.insert(0, str(tree.item(item, "values")[4] or 0))
        entry_so_luong.pack(pady=5)

        def luu_gia_so_luong():
            gia = entry_gia.get()
            so_luong = entry_so_luong.get()
            if not (gia.isdigit() and so_luong.isdigit()) or int(gia) < 0 or int(so_luong) <= 0:
                messagebox.showwarning("Lỗi", "Giá nhập phải là số không âm và số lượng phải là số nguyên dương!")
                return
            gia = int(gia)
            so_luong = int(so_luong)

            current_values = list(tree.item(item, "values"))
            current_values[3] = gia
            current_values[4] = so_luong
            tree.item(item, values=tuple(current_values))

            product = current_values
            found = False
            for i, p in enumerate(selected_products):
                if p[0] == ma_san_pham:
                    if so_luong > 0:
                        selected_products[i] = product
                    else:
                        selected_products.pop(i)
                    found = True
                    break
            if not found and so_luong > 0:
                selected_products.append(product)

            new_window.destroy()

        tk.Button(new_window, text="Lưu", command=luu_gia_so_luong).pack(pady=5)
        tk.Button(new_window, text="Hủy", command=new_window.destroy).pack(pady=5)

    tree.bind("<Double-1>", chon_gia_so_luong)

    # Hàm xử lý sửa phiếu nhập
    def handle_sua_phieu_nhap():
        ma_phieu = entry_ma_phieu.get()
        if not ma_phieu:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã phiếu nhập!")
            return

        gio_nhap = entries["Giờ nhập (HH:MM:SS)"].get()
        ngay_nhap = entries["Ngày nhập (YYYY-MM-DD)"].get()
        nha_cung_cap = entries["Nhà cung cấp"].get()

        if not all([gio_nhap, ngay_nhap, nha_cung_cap]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
            return

        connection = connect_db()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            cursor.execute("START TRANSACTION")

            # Cập nhật thông tin phiếu nhập
            query_update = """
                UPDATE phieu_nhap 
                SET gio_nhap = %s, ngay_nhap = %s, nha_cung_cap = %s
                WHERE ma_phieu_nhap = %s
            """
            cursor.execute(query_update, (gio_nhap, ngay_nhap, nha_cung_cap, ma_phieu))
            if cursor.rowcount == 0:
                raise Exception("Không tìm thấy phiếu nhập để cập nhật!")

            # Lấy danh sách sản phẩm cũ
            query_old_products = """
                SELECT ma_san_pham, so_luong 
                FROM phieu_nhap_san_pham 
                WHERE ma_phieu_nhap = %s
            """
            cursor.execute(query_old_products, (ma_phieu,))
            old_products = {row[0]: row[1] for row in cursor.fetchall()}

            # Xóa sản phẩm cũ và khôi phục tồn kho
            cursor.execute("DELETE FROM phieu_nhap_san_pham WHERE ma_phieu_nhap = %s", (ma_phieu,))
            for ma_san_pham, so_luong in old_products.items():
                cursor.execute("""
                    UPDATE san_pham 
                    SET so_luong_ton_kho = so_luong_ton_kho - %s 
                    WHERE ma_san_pham = %s
                """, (so_luong, ma_san_pham))

            # Thêm sản phẩm mới và cập nhật tồn kho
            for product in selected_products:
                if product[4] and int(product[4]) > 0:
                    so_luong = int(product[4])
                    gia_nhap = int(product[3])
                    cursor.execute("""
                        INSERT INTO phieu_nhap_san_pham (ma_phieu_nhap, ma_san_pham, gia_nhap, so_luong)
                        VALUES (%s, %s, %s, %s)
                    """, (ma_phieu, product[0], gia_nhap, so_luong))

                    cursor.execute("""
                        UPDATE san_pham 
                        SET so_luong_ton_kho = so_luong_ton_kho + %s
                        WHERE ma_san_pham = %s
                    """, (so_luong, product[0]))

            connection.commit()
            messagebox.showinfo("Thành công", f"Đã sửa phiếu nhập mã {ma_phieu} thành công!")
            entry_ma_phieu.delete(0, tk.END)
            for entry in entries.values():
                entry.delete(0, tk.END)
            for item in tree.get_children():
                tree.delete(item)
            selected_products.clear()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi sửa phiếu nhập: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    tk.Button(search_frame, text="Tìm kiếm", command=tim_kiem_phieu_nhap).grid(row=1, column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Sửa phiếu nhập", command=handle_sua_phieu_nhap).grid(row=len(fields), column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)

# Form xóa phiếu nhập
def show_xoa_phieu_nhap_form(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Xóa phiếu nhập", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame tìm kiếm phiếu nhập
    search_frame = tk.LabelFrame(main_frame, text="Tìm kiếm phiếu nhập", font=("Arial", 12))
    search_frame.pack(pady=10, fill="x")

    tk.Label(search_frame, text="Mã phiếu nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_ma_phieu = tk.Entry(search_frame)
    entry_ma_phieu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    search_frame.grid_columnconfigure(1, weight=1)

    # Frame hiển thị thông tin
    info_frame = tk.LabelFrame(main_frame, text="Thông tin phiếu nhập", font=("Arial", 12))
    info_frame.pack(pady=10, fill="x")

    tk.Label(info_frame, text="Giờ nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    label_gio_nhap = tk.Label(info_frame, text="")
    label_gio_nhap.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(info_frame, text="Ngày nhập:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    label_ngay_nhap = tk.Label(info_frame, text="")
    label_ngay_nhap.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(info_frame, text="Nhà cung cấp:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    label_nha_cung_cap = tk.Label(info_frame, text="")
    label_nha_cung_cap.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Hàm tìm kiếm phiếu nhập
    def tim_kiem_phieu_nhap():
        ma_phieu = entry_ma_phieu.get()
        if not ma_phieu:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã phiếu nhập!")
            return

        connection = connect_db()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            query = """
                SELECT gio_nhap, ngay_nhap, nha_cung_cap
                FROM phieu_nhap
                WHERE ma_phieu_nhap = %s
            """
            cursor.execute(query, (ma_phieu,))
            phieu_nhap = cursor.fetchone()

            if not phieu_nhap:
                messagebox.showwarning("Không tìm thấy", "Không tìm thấy phiếu nhập với mã này!")
                return

            label_gio_nhap.config(text=phieu_nhap[0])
            label_ngay_nhap.config(text=phieu_nhap[1])
            label_nha_cung_cap.config(text=phieu_nhap[2])

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm phiếu nhập: {e}")
        finally:
            cursor.close()
            connection.close()

    # Hàm xóa phiếu nhập
    def handle_xoa_phieu_nhap():
        ma_phieu = entry_ma_phieu.get()
        if not ma_phieu:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã phiếu nhập!")
            return

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa phiếu nhập mã {ma_phieu}?"):
            connection = connect_db()
            if not connection:
                return

            try:
                cursor = connection.cursor()
                cursor.execute("START TRANSACTION")

                # Lấy danh sách sản phẩm để khôi phục tồn kho
                query_products = """
                    SELECT ma_san_pham, so_luong 
                    FROM phieu_nhap_san_pham 
                    WHERE ma_phieu_nhap = %s
                """
                cursor.execute(query_products, (ma_phieu,))
                products = cursor.fetchall()

                for product in products:
                    cursor.execute("""
                        UPDATE san_pham 
                        SET so_luong_ton_kho = so_luong_ton_kho - %s 
                        WHERE ma_san_pham = %s
                    """, (product[1], product[0]))

                # Xóa chi tiết nhập hàng
                cursor.execute("DELETE FROM phieu_nhap_san_pham WHERE ma_phieu_nhap = %s", (ma_phieu,))
                # Xóa phiếu nhập
                cursor.execute("DELETE FROM phieu_nhap WHERE ma_phieu_nhap = %s", (ma_phieu,))

                connection.commit()
                messagebox.showinfo("Thành công", f"Đã xóa phiếu nhập mã {ma_phieu} thành công!")
                entry_ma_phieu.delete(0, tk.END)
                label_gio_nhap.config(text="")
                label_ngay_nhap.config(text="")
                label_nha_cung_cap.config(text="")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi xóa phiếu nhập: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    tk.Button(search_frame, text="Tìm kiếm", command=tim_kiem_phieu_nhap).grid(row=1, column=0, columnspan=2, pady=5)
    tk.Button(info_frame, text="Xóa phiếu nhập", command=handle_xoa_phieu_nhap).grid(row=3, column=0, columnspan=2, pady=5)
    tk.Button(info_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).grid(row=4, column=0, columnspan=2, pady=5)

# Form cảnh báo hàng sắp hết
def show_canh_bao_hang_sap_het_form(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Cảnh báo hàng sắp hết", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame hiển thị kết quả
    result_frame = tk.LabelFrame(main_frame, text="Sản phẩm sắp hết", font=("Arial", 12))
    result_frame.pack(pady=10, fill="both", expand=True)

    columns = ("Mã SP", "Tên", "Kích cỡ", "Số lượng tồn")
    tree = ttk.Treeview(result_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Hàm cập nhật danh sách sản phẩm sắp hết (ngưỡng 10)
    def cap_nhat_danh_sach_sap_het():
        for item in tree.get_children():
            tree.delete(item)
        connection = connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT ma_san_pham, ten, kich_co, so_luong_ton_kho FROM san_pham WHERE so_luong_ton_kho <= 10"
                cursor.execute(query)
                products = cursor.fetchall()
                for product in products:
                    tree.insert("", tk.END, values=product)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách sản phẩm: {e}")
            finally:
                cursor.close()
                connection.close()

    cap_nhat_danh_sach_sap_het()

    tk.Button(main_frame, text="Làm mới", command=cap_nhat_danh_sach_sap_het).pack(pady=5)
    tk.Button(main_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).pack(pady=5)

# Form tra cứu phiếu nhập
def show_tra_cuu_phieu_nhap_form(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Tra cứu phiếu nhập", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame tìm kiếm phiếu nhập
    search_frame = tk.LabelFrame(main_frame, text="Nhập thông tin tìm kiếm", font=("Arial", 12))
    search_frame.pack(pady=10, fill="x")

    tk.Label(search_frame, text="Mã phiếu nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_ma_phieu = tk.Entry(search_frame)
    entry_ma_phieu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    search_frame.grid_columnconfigure(1, weight=1)

    # Frame hiển thị thông tin phiếu nhập
    info_frame = tk.LabelFrame(main_frame, text="Thông tin phiếu nhập", font=("Arial", 12))
    info_frame.pack(pady=10, fill="both", expand=True)

    tk.Label(info_frame, text="Giờ nhập:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    label_gio_nhap = tk.Label(info_frame, text="")
    label_gio_nhap.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(info_frame, text="Ngày nhập:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    label_ngay_nhap = tk.Label(info_frame, text="")
    label_ngay_nhap.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(info_frame, text="Nhà cung cấp:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    label_nha_cung_cap = tk.Label(info_frame, text="")
    label_nha_cung_cap.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Frame hiển thị danh sách sản phẩm
    product_frame = tk.LabelFrame(main_frame, text="Danh sách sản phẩm", font=("Arial", 12))
    product_frame.pack(pady=10, fill="both", expand=True)

    columns = ("Mã SP", "Tên", "Kích cỡ", "Giá nhập", "Số lượng")
    tree = ttk.Treeview(product_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    
    scrollbar = ttk.Scrollbar(product_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Hàm tra cứu phiếu nhập
    def tra_cuu_phieu_nhap():
        ma_phieu = entry_ma_phieu.get()
        if not ma_phieu:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã phiếu nhập!")
            return

        connection = connect_db()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            query = """
                SELECT gio_nhap, ngay_nhap, nha_cung_cap
                FROM phieu_nhap
                WHERE ma_phieu_nhap = %s
            """
            cursor.execute(query, (ma_phieu,))
            phieu_nhap = cursor.fetchone()

            if not phieu_nhap:
                messagebox.showwarning("Không tìm thấy", "Không tìm thấy phiếu nhập với mã này!")
                return

            label_gio_nhap.config(text=phieu_nhap[0])
            label_ngay_nhap.config(text=phieu_nhap[1])
            label_nha_cung_cap.config(text=phieu_nhap[2])

            # Lấy danh sách sản phẩm
            query_san_pham = """
                SELECT sp.ma_san_pham, sp.ten, sp.kich_co, pnsp.gia_nhap, pnsp.so_luong
                FROM phieu_nhap_san_pham pnsp
                JOIN san_pham sp ON pnsp.ma_san_pham = sp.ma_san_pham
                WHERE pnsp.ma_phieu_nhap = %s
            """
            cursor.execute(query_san_pham, (ma_phieu,))
            products = cursor.fetchall()

            for item in tree.get_children():
                tree.delete(item)
            for product in products:
                tree.insert("", tk.END, values=product)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tra cứu phiếu nhập: {e}")
        finally:
            cursor.close()
            connection.close()

    # Hàm hiển thị tất cả phiếu nhập
    def hien_thi_tat_ca_phieu_nhap():
        connection = connect_db()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            query = "SELECT ma_phieu_nhap, gio_nhap, ngay_nhap, nha_cung_cap FROM phieu_nhap"
            cursor.execute(query)
            phieu_nhaps = cursor.fetchall()

            if not phieu_nhaps:
                messagebox.showinfo("Thông báo", "Không có phiếu nhập nào!")
                return

            # Tạo cửa sổ mới để hiển thị tất cả phiếu
            new_window = tk.Toplevel(window)
            new_window.title("Danh sách tất cả phiếu nhập")
            new_window.geometry("600x400")

            # Frame cho danh sách phiếu
            phieu_frame = tk.LabelFrame(new_window, text="Danh sách phiếu nhập", font=("Arial", 12))
            phieu_frame.pack(pady=10, fill="both", expand=True)

            phieu_tree = ttk.Treeview(phieu_frame, columns=("Mã phiếu", "Giờ nhập", "Ngày nhập", "Nhà cung cấp"), show="headings")
            for col in ("Mã phiếu", "Giờ nhập", "Ngày nhập", "Nhà cung cấp"):
                phieu_tree.heading(col, text=col)
                phieu_tree.column(col, width=140, anchor="center")
            
            scrollbar = ttk.Scrollbar(phieu_frame, orient="vertical", command=phieu_tree.yview)
            phieu_tree.configure(yscroll=scrollbar.set)
            
            phieu_tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for phieu in phieu_nhaps:
                phieu_tree.insert("", tk.END, values=phieu)

            # Nút xem chi tiết
            def xem_chi_tiet(event):
                item = phieu_tree.selection()
                if not item:
                    return
                ma_phieu = phieu_tree.item(item[0], "values")[0]
                tra_cuu_phieu_nhap()  # Gọi lại hàm tra cứu với mã phiếu
                entry_ma_phieu.delete(0, tk.END)
                entry_ma_phieu.insert(0, ma_phieu)
                new_window.destroy()

            phieu_tree.bind("<Double-1>", xem_chi_tiet)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi hiển thị tất cả phiếu nhập: {e}")
        finally:
            cursor.close()
            connection.close()

    tk.Button(search_frame, text="Tra cứu", command=tra_cuu_phieu_nhap).grid(row=1, column=0, columnspan=2, pady=5)
    tk.Button(search_frame, text="Hiển thị tất cả", command=hien_thi_tat_ca_phieu_nhap).grid(row=2, column=0, columnspan=2, pady=5)
    tk.Button(main_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).pack(pady=5)