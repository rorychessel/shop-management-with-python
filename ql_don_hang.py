import tkinter as tk
from tkinter import ttk, messagebox
from connection import connect_db

# Hàm tìm kiếm khách hàng theo số điện thoại
def tim_kiem_khach_hang(window, sdt, callback):
    connection = connect_db()
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor()
        query = "SELECT ma_khach_hang, ho_ten, dia_chi, email FROM khach_hang WHERE sdt = %s"
        cursor.execute(query, (sdt,))
        result = cursor.fetchone()
        return result
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm khách hàng: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

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

# Form tạo đơn hàng mới với chọn sản phẩm
def show_tao_don_hang_form(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Tạo đơn hàng mới", font=("Arial", 14))
    label_title.pack(pady=10)

    # Lấy mã nhân viên hiện tại
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT ma_nhan_su FROM nhan_su WHERE id_tai_khoan = (SELECT id_tai_khoan FROM tai_khoan WHERE ten_dang_nhap = %s)"
            cursor.execute(query, (current_user,))
            ma_ns_tao_don = cursor.fetchone()[0]
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy mã nhân viên: {e}")
            ma_ns_tao_don = None
        finally:
            cursor.close()
            connection.close()

    # Các trường nhập liệu cho đơn hàng
    form_frame = tk.Frame(main_frame)
    form_frame.pack(pady=10)

    fields = ["Số điện thoại khách hàng", "Giờ đặt (HH:MM:SS)", "Ngày đặt (YYYY-MM-DD)", 
              "Phương thức thanh toán", "Trạng thái thanh toán", "Trạng thái vận đơn"]
    entries = {}

    for idx, field in enumerate(fields):
        tk.Label(form_frame, text=field + ":").grid(row=idx, column=0, padx=5, pady=5, sticky="e")
        if field == "Trạng thái thanh toán":
            entry = ttk.Combobox(form_frame, values=["Đã thanh toán", "Chưa thanh toán"], state="readonly")
            entry.set("Chưa thanh toán")  # Giá trị mặc định
        elif field == "Trạng thái vận đơn":
            entry = ttk.Combobox(form_frame, values=["Đang đóng gói", "Đang vận chuyển", "Đã giao", "Hủy đơn", "Trả hàng"], state="readonly")
            entry.set("Đang đóng gói")  # Giá trị mặc định
        else:
            entry = tk.Entry(form_frame)
            if field == "Số điện thoại khách hàng":
                entry.insert(0, "")  # Để trống
            elif field == "Giờ đặt (HH:MM:SS)":
                entry.insert(0, "")  # Để trống
            elif field == "Ngày đặt (YYYY-MM-DD)":
                entry.insert(0, "")  # Để trống
            elif field == "Phương thức thanh toán":
                entry.insert(0, "")  # Để trống
        entry.grid(row=idx, column=1, padx=5, pady=5, sticky="ew")
        entries[field] = entry

    form_frame.grid_columnconfigure(1, weight=1)

    # Frame chọn sản phẩm
    product_frame = tk.LabelFrame(main_frame, text="Chọn sản phẩm", font=("Arial", 12))
    product_frame.pack(pady=10, fill="both", expand=True)

    # Treeview để hiển thị danh sách sản phẩm
    columns = ("Mã SP", "Tên", "Kích cỡ", "Giá bán", "Số lượng tồn", "Số lượng chọn")
    tree = ttk.Treeview(product_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100 if col != "Số lượng chọn" else 80, anchor="center")
    
    scrollbar = ttk.Scrollbar(product_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Frame hiển thị sản phẩm đã chọn
    selected_frame = tk.LabelFrame(main_frame, text="Sản phẩm đã chọn", font=("Arial", 12))
    selected_frame.pack(pady=10, fill="both", expand=True)

    # Thêm cột checkbox
    columns_with_checkbox = ("",) + columns  # Thêm cột checkbox
    selected_tree = ttk.Treeview(selected_frame, columns=columns_with_checkbox, show="headings")
    
    for col in columns_with_checkbox:
        selected_tree.heading(col, text=col if col else "Chọn")
        selected_tree.column(col, width=30 if col == "" else 100 if col != "Số lượng chọn" else 80, anchor="center")
    
    selected_scrollbar = ttk.Scrollbar(selected_frame, orient="vertical", command=selected_tree.yview)
    selected_tree.configure(yscroll=selected_scrollbar.set)
    
    selected_tree.pack(side="left", fill="both", expand=True)
    selected_scrollbar.pack(side="right", fill="y")

    # Danh sách sản phẩm chọn và trạng thái checkbox
    selected_products = []
    checkbox_states = {}

    # Cập nhật danh sách sản phẩm
    def cap_nhat_danh_sach_san_pham():
        for item in tree.get_children():
            tree.delete(item)
        products = lay_danh_sach_san_pham()
        for product in products:
            tree.insert("", tk.END, values=product + (0,))  # Mặc định số lượng chọn là 0

    cap_nhat_danh_sach_san_pham()

    # Cập nhật danh sách sản phẩm đã chọn
    def cap_nhat_danh_sach_da_chon():
        for item in selected_tree.get_children():
            selected_tree.delete(item)
        for product in selected_products:
            item_id = selected_tree.insert("", tk.END, values=(0,) + tuple(product))  # Chuyển product thành tuple
            checkbox_states[item_id] = tk.BooleanVar(value=True)  # Mặc định checked
            # Thêm checkbox vào cột đầu tiên
            chk = ttk.Checkbutton(selected_frame, variable=checkbox_states[item_id])
            selected_tree.set(item_id, "#0", chk)

    # Hàm chọn số lượng sản phẩm
    def chon_so_luong(event):
        item = tree.selection()
        if not item:
            return
        item = item[0]
        ma_san_pham = tree.item(item, "values")[0]
        so_luong_hien_tai = tree.item(item, "values")[5] or 0
        if not isinstance(so_luong_hien_tai, int):
            so_luong_hien_tai = 0
        
        so_luong_ton = int(tree.item(item, "values")[4])
        new_window = tk.Toplevel(window)
        new_window.title("Chọn số lượng")
        new_window.geometry("300x150")

        label = tk.Label(new_window, text=f"Nhập số lượng cho sản phẩm mã {ma_san_pham} (Tồn: {so_luong_ton}):")
        label.pack(pady=10)

        entry = tk.Entry(new_window)
        entry.insert(0, str(so_luong_hien_tai))
        entry.pack(pady=5)

        def luu_so_luong():
            so_luong = entry.get()
            if not so_luong.isdigit() or int(so_luong) <= 0:
                messagebox.showwarning("Lỗi", "Số lượng phải là số nguyên dương!")
                return
            so_luong = int(so_luong)
            if so_luong > so_luong_ton:
                messagebox.showwarning("Lỗi", f"Số lượng chọn ({so_luong}) vượt quá tồn kho ({so_luong_ton})!")
                return
            
            # Cập nhật Treeview
            current_values = list(tree.item(item, "values"))
            current_values[5] = so_luong
            tree.item(item, values=tuple(current_values))
            
            # Cập nhật danh sách sản phẩm đã chọn
            product = list(tree.item(item, "values"))
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
            
            cap_nhat_danh_sach_da_chon()
            new_window.destroy()

        tk.Button(new_window, text="Lưu", command=luu_so_luong).pack(pady=5)
        tk.Button(new_window, text="Hủy", command=new_window.destroy).pack(pady=5)

    tree.bind("<Double-1>", chon_so_luong)

    # Hàm xóa sản phẩm đã chọn
    def xoa_san_pham():
        items_to_remove = [item for item in selected_tree.get_children() if checkbox_states[item].get()]
        if not items_to_remove:
            messagebox.showwarning("Cảnh báo", "Vui lòng đánh dấu ít nhất một sản phẩm để xóa!")
            return
        
        for item in items_to_remove:
            ma_san_pham = selected_tree.item(item, "values")[1]  # Cột 1 là Mã SP
            for product in selected_products:
                if product[0] == ma_san_pham:
                    selected_products.remove(product)
                    break
            selected_tree.delete(item)
            del checkbox_states[item]
        
        cap_nhat_danh_sach_da_chon()

    # Thêm nút Xóa
    delete_button = tk.Button(selected_frame, text="Xóa", command=xoa_san_pham)
    delete_button.pack(pady=5)

    # Hàm xử lý tạo đơn hàng
    def handle_tao_don_hang():
        sdt = entries["Số điện thoại khách hàng"].get()
        gio_dat = entries["Giờ đặt (HH:MM:SS)"].get()
        ngay_dat = entries["Ngày đặt (YYYY-MM-DD)"].get()
        pthuc_thanh_toan = entries["Phương thức thanh toán"].get()
        tthai_thanh_toan = entries["Trạng thái thanh toán"].get()
        tthai_van_don = entries["Trạng thái vận đơn"].get()

        if not all([sdt, gio_dat, ngay_dat, pthuc_thanh_toan, tthai_thanh_toan, tthai_van_don]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
            return

        khach_hang = tim_kiem_khach_hang(window, sdt, None)
        if not khach_hang:
            messagebox.showwarning("Lỗi", "Không tìm thấy khách hàng với số điện thoại này!")
            return
        ma_khach_hang = khach_hang[0]

        if not selected_products or all(p[5] == 0 for p in selected_products):
            messagebox.showwarning("Lỗi", "Vui lòng chọn ít nhất một sản phẩm với số lượng lớn hơn 0!")
            return

        if ma_ns_tao_don is None:
            messagebox.showerror("Lỗi", "Không thể xác định mã nhân viên!")
            return

        connection = connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                # Bắt đầu giao dịch
                cursor.execute("""
                    INSERT INTO don_hang (gio_dat, ngay_dat, pthuc_thanh_toan, tthai_thanh_toan, tthai_van_don, tong_tien, ma_khach_hang, ma_ns_tao_don)
                    VALUES (%s, %s, %s, %s, %s, 0, %s, %s)
                """, (gio_dat, ngay_dat, pthuc_thanh_toan, tthai_thanh_toan, tthai_van_don, ma_khach_hang, ma_ns_tao_don))
                ma_don_hang = cursor.lastrowid

                # Thêm chi tiết đơn hàng và cập nhật tồn kho
                for product in selected_products:
                    if product[5] and int(product[5]) > 0:  # Chỉ thêm nếu có số lượng
                        so_luong = int(product[5])
                        gia_ban = int(product[3])
                        thanh_tien = gia_ban * so_luong
                        cursor.execute("""
                            INSERT INTO don_hang_san_pham (ma_don_hang, ma_san_pham, gia_ban, so_luong, thanh_tien)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (ma_don_hang, product[0], gia_ban, so_luong, thanh_tien))

                        # Cập nhật số lượng tồn kho
                        cursor.execute("""
                            UPDATE san_pham 
                            SET so_luong_ton_kho = so_luong_ton_kho - %s 
                            WHERE ma_san_pham = %s AND so_luong_ton_kho >= %s
                        """, (so_luong, product[0], so_luong))
                        if cursor.rowcount == 0:
                            raise Exception(f"Số lượng tồn kho không đủ cho sản phẩm mã {product[0]}")

                # Cập nhật tổng tiền
                cursor.execute("""
                    UPDATE don_hang 
                    SET tong_tien = (SELECT SUM(thanh_tien) FROM don_hang_san_pham WHERE ma_don_hang = %s)
                    WHERE ma_don_hang = %s
                """, (ma_don_hang, ma_don_hang))

                connection.commit()
                messagebox.showinfo("Thành công", f"Đã tạo đơn hàng mã {ma_don_hang} thành công!")
                # Reset danh sách sản phẩm chọn
                selected_products.clear()
                cap_nhat_danh_sach_san_pham()
                cap_nhat_danh_sach_da_chon()
                for entry in entries.values():
                    if isinstance(entry, tk.Entry):
                        entry.delete(0, tk.END)
                    elif isinstance(entry, ttk.Combobox):
                        if entry.get() == "Chưa thanh toán" or entry.get() == "Đang đóng gói":
                            entry.set(entry.get())  # Giữ giá trị mặc định
                        else:
                            entry.set(entry['values'][0])  # Reset về giá trị mặc định đầu tiên
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi tạo đơn hàng: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()

    tk.Button(form_frame, text="Tạo đơn hàng", command=handle_tao_don_hang).grid(row=len(fields), column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)

# Form tra cứu đơn hàng
def show_tra_cuu_don_hang_form(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Tra cứu đơn hàng", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame cho các lựa chọn tra cứu
    search_frame = tk.Frame(main_frame)
    search_frame.pack(pady=10)

    # Các trường tìm kiếm
    search_fields = ["Mã đơn", "Ngày đặt (YYYY-MM-DD)", "Phương thức thanh toán", "Trạng thái thanh toán", "Trạng thái vận đơn", "Mã khách hàng", "Mã nhân sự tạo đơn"]
    search_entries = {}

    for idx, field in enumerate(search_fields):
        tk.Label(search_frame, text=field + ":").grid(row=idx, column=0, padx=5, pady=5, sticky="e")
        if field == "Trạng thái thanh toán":
            entry = ttk.Combobox(search_frame, values=["Đã thanh toán", "Chưa thanh toán"], state="readonly")
            entry.set("")  # Để trống mặc định
        elif field == "Trạng thái vận đơn":
            entry = ttk.Combobox(search_frame, values=["Đang đóng gói", "Đang vận chuyển", "Đã giao", "Hủy đơn", "Trả hàng"], state="readonly")
            entry.set("")  # Để trống mặc định
        else:
            entry = tk.Entry(search_frame)
            if field == "Ngày đặt (YYYY-MM-DD)":
                entry.insert(0, "")  # Để trống
            else:
                entry.insert(0, "")  # Để trống
        entry.grid(row=idx, column=1, padx=5, pady=5, sticky="ew")
        search_entries[field] = entry

    search_frame.grid_columnconfigure(1, weight=1)

    # Frame hiển thị kết quả
    result_frame = tk.LabelFrame(main_frame, text="Kết quả tra cứu", font=("Arial", 12))
    result_frame.pack(pady=10, fill="both", expand=True)

    # Treeview để hiển thị danh sách đơn hàng
    columns = ("Mã đơn", "Ngày đặt", "Phương thức thanh toán", "Trạng thái thanh toán", "Trạng thái vận đơn", "Mã khách hàng", "Mã nhân sự tạo đơn")
    result_tree = ttk.Treeview(result_frame, columns=columns, show="headings")
    
    for col in columns:
        result_tree.heading(col, text=col)
        result_tree.column(col, width=100, anchor="center")
    
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_tree.yview)
    result_tree.configure(yscroll=scrollbar.set)
    
    result_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Hàm tra cứu đơn hàng
    def tra_cuu_don_hang():
        for item in result_tree.get_children():
            result_tree.delete(item)

        ma_don = search_entries["Mã đơn"].get()
        ngay_dat = search_entries["Ngày đặt (YYYY-MM-DD)"].get()
        pthuc_thanh_toan = search_entries["Phương thức thanh toán"].get()
        tthai_thanh_toan = search_entries["Trạng thái thanh toán"].get()
        tthai_van_don = search_entries["Trạng thái vận đơn"].get()
        ma_khach_hang = search_entries["Mã khách hàng"].get()
        ma_ns_tao_don = search_entries["Mã nhân sự tạo đơn"].get()

        query = """
            SELECT ma_don_hang, ngay_dat, pthuc_thanh_toan, tthai_thanh_toan, tthai_van_don, ma_khach_hang, ma_ns_tao_don
            FROM don_hang
            WHERE 1=1
        """
        params = []

        if ma_don:
            query += " AND ma_don_hang = %s"
            params.append(ma_don)
        if ngay_dat:
            query += " AND ngay_dat = %s"
            params.append(ngay_dat)
        if pthuc_thanh_toan:
            query += " AND pthuc_thanh_toan = %s"
            params.append(pthuc_thanh_toan)
        if tthai_thanh_toan:
            query += " AND tthai_thanh_toan = %s"
            params.append(tthai_thanh_toan)
        if tthai_van_don:
            query += " AND tthai_van_don = %s"
            params.append(tthai_van_don)
        if ma_khach_hang:
            query += " AND ma_khach_hang = %s"
            params.append(ma_khach_hang)
        if ma_ns_tao_don:
            query += " AND ma_ns_tao_don = %s"
            params.append(ma_ns_tao_don)

        connection = connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, tuple(params))
                results = cursor.fetchall()
                for result in results:
                    result_tree.insert("", tk.END, values=result)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi tra cứu đơn hàng: {e}")
            finally:
                cursor.close()
                connection.close()

    # Hàm hiển thị tất cả đơn hàng
    def hien_thi_tat_ca_don_hang():
        for item in result_tree.get_children():
            result_tree.delete(item)

        connection = connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                    SELECT ma_don_hang, ngay_dat, pthuc_thanh_toan, tthai_thanh_toan, tthai_van_don, ma_khach_hang, ma_ns_tao_don
                    FROM don_hang
                """
                cursor.execute(query)
                results = cursor.fetchall()
                for result in results:
                    result_tree.insert("", tk.END, values=result)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi hiển thị tất cả đơn hàng: {e}")
            finally:
                cursor.close()
                connection.close()

    # Nút tra cứu và hiển thị tất cả
    tk.Button(search_frame, text="Tra cứu", command=tra_cuu_don_hang).grid(row=len(search_fields), column=0, columnspan=2, pady=5)
    tk.Button(search_frame, text="Hiển thị tất cả", command=hien_thi_tat_ca_don_hang).grid(row=len(search_fields)+1, column=0, columnspan=2, pady=5)
    tk.Button(search_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).grid(row=len(search_fields)+2, column=0, columnspan=2, pady=5)

# Form cập nhật đơn hàng
def show_cap_nhat_don_hang_form(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Cập nhật đơn hàng", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame tìm kiếm đơn hàng
    search_frame = tk.LabelFrame(main_frame, text="Tìm kiếm đơn hàng", font=("Arial", 12))
    search_frame.pack(pady=10, fill="x")

    tk.Label(search_frame, text="Mã đơn hàng:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_ma_don = tk.Entry(search_frame)
    entry_ma_don.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    search_frame.grid_columnconfigure(1, weight=1)

    # Frame thông tin đơn hàng
    form_frame = tk.LabelFrame(main_frame, text="Thông tin đơn hàng", font=("Arial", 12))
    form_frame.pack(pady=10, fill="x")

    fields = ["Số điện thoại khách hàng", "Giờ đặt (HH:MM:SS)", "Ngày đặt (YYYY-MM-DD)", 
              "Phương thức thanh toán", "Trạng thái thanh toán", "Trạng thái vận đơn"]
    entries = {}

    for idx, field in enumerate(fields):
        tk.Label(form_frame, text=field + ":").grid(row=idx, column=0, padx=5, pady=5, sticky="e")
        if field == "Trạng thái thanh toán":
            entry = ttk.Combobox(form_frame, values=["Đã thanh toán", "Chưa thanh toán"], state="readonly")
        elif field == "Trạng thái vận đơn":
            entry = ttk.Combobox(form_frame, values=["Đang đóng gói", "Đang vận chuyển", "Đã giao", "Hủy đơn", "Trả hàng"], state="readonly")
        else:
            entry = tk.Entry(form_frame)
        entry.grid(row=idx, column=1, padx=5, pady=5, sticky="ew")
        entries[field] = entry
    form_frame.grid_columnconfigure(1, weight=1)

    # Frame chọn sản phẩm
    product_frame = tk.LabelFrame(main_frame, text="Sản phẩm trong đơn hàng", font=("Arial", 12))
    product_frame.pack(pady=10, fill="both", expand=True)

    columns = ("Mã SP", "Tên", "Kích cỡ", "Giá bán", "Số lượng", "Thành tiền")
    tree = ttk.Treeview(product_frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    
    scrollbar = ttk.Scrollbar(product_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Frame danh sách sản phẩm có sẵn
    available_product_frame = tk.LabelFrame(main_frame, text="Sản phẩm có sẵn", font=("Arial", 12))
    available_product_frame.pack(pady=10, fill="both", expand=True)

    available_columns = ("Mã SP", "Tên", "Kích cỡ", "Giá bán", "Số lượng tồn", "Số lượng chọn")
    available_tree = ttk.Treeview(available_product_frame, columns=available_columns, show="headings")
    
    for col in available_columns:
        available_tree.heading(col, text=col)
        available_tree.column(col, width=100 if col != "Số lượng chọn" else 80, anchor="center")
    
    available_scrollbar = ttk.Scrollbar(available_product_frame, orient="vertical", command=available_tree.yview)
    available_tree.configure(yscroll=available_scrollbar.set)
    
    available_tree.pack(side="left", fill="both", expand=True)
    available_scrollbar.pack(side="right", fill="y")

    selected_products = []
    
    # Hàm tìm kiếm đơn hàng
    def tim_kiem_don_hang():
        ma_don = entry_ma_don.get()
        if not ma_don:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã đơn hàng!")
            return

        connection = connect_db()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            # Lấy thông tin đơn hàng
            query = """
                SELECT dh.ma_don_hang, dh.gio_dat, dh.ngay_dat, dh.pthuc_thanh_toan, 
                       dh.tthai_thanh_toan, dh.tthai_van_don, kh.sdt
                FROM don_hang dh
                JOIN khach_hang kh ON dh.ma_khach_hang = kh.ma_khach_hang
                WHERE dh.ma_don_hang = %s
            """
            cursor.execute(query, (ma_don,))
            don_hang = cursor.fetchone()

            if not don_hang:
                messagebox.showwarning("Không tìm thấy", "Không tìm thấy đơn hàng với mã này!")
                return

            # Hiển thị thông tin đơn hàng
            entries["Số điện thoại khách hàng"].delete(0, tk.END)
            entries["Số điện thoại khách hàng"].insert(0, don_hang[6])
            entries["Giờ đặt (HH:MM:SS)"].delete(0, tk.END)
            entries["Giờ đặt (HH:MM:SS)"].insert(0, don_hang[1])
            entries["Ngày đặt (YYYY-MM-DD)"].delete(0, tk.END)
            entries["Ngày đặt (YYYY-MM-DD)"].insert(0, don_hang[2])
            entries["Phương thức thanh toán"].delete(0, tk.END)
            entries["Phương thức thanh toán"].insert(0, don_hang[3])
            entries["Trạng thái thanh toán"].set(don_hang[4])
            entries["Trạng thái vận đơn"].set(don_hang[5])

            # Lấy danh sách sản phẩm trong đơn hàng
            query_san_pham = """
                SELECT sp.ma_san_pham, sp.ten, sp.kich_co, dhsp.gia_ban, dhsp.so_luong, dhsp.thanh_tien
                FROM don_hang_san_pham dhsp
                JOIN san_pham sp ON dhsp.ma_san_pham = sp.ma_san_pham
                WHERE dhsp.ma_don_hang = %s
            """
            cursor.execute(query_san_pham, (ma_don,))
            products = cursor.fetchall()

            for item in tree.get_children():
                tree.delete(item)
            selected_products.clear()
            for product in products:
                tree.insert("", tk.END, values=product)
                selected_products.append(list(product))

            # Cập nhật danh sách sản phẩm có sẵn
            cap_nhat_danh_sach_san_pham()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm đơn hàng: {e}")
        finally:
            cursor.close()
            connection.close()

    # Cập nhật danh sách sản phẩm có sẵn
    def cap_nhat_danh_sach_san_pham():
        for item in available_tree.get_children():
            available_tree.delete(item)
        products = lay_danh_sach_san_pham()
        for product in products:
            available_tree.insert("", tk.END, values=product + (0,))

    # Hàm chọn số lượng sản phẩm
    def chon_so_luong(event):
        item = available_tree.selection()
        if not item:
            return
        item = item[0]
        ma_san_pham = available_tree.item(item, "values")[0]
        so_luong_hien_tai = int(available_tree.item(item, "values")[5] or 0)
        so_luong_ton = int(available_tree.item(item, "values")[4])

        new_window = tk.Toplevel(window)
        new_window.title("Chọn số lượng")
        new_window.geometry("300x150")

        label = tk.Label(new_window, text=f"Nhập số lượng cho sản phẩm mã {ma_san_pham} (Tồn: {so_luong_ton}):")
        label.pack(pady=10)

        entry = tk.Entry(new_window)
        entry.insert(0, str(so_luong_hien_tai))
        entry.pack(pady=5)

        def luu_so_luong():
            so_luong = entry.get()
            if not so_luong.isdigit() or int(so_luong) < 0:
                messagebox.showwarning("Lỗi", "Số lượng phải là số nguyên không âm!")
                return
            so_luong = int(so_luong)
            if so_luong > so_luong_ton:
                messagebox.showwarning("Lỗi", f"Số lượng chọn ({so_luong}) vượt quá tồn kho ({so_luong_ton})!")
                return

            current_values = list(available_tree.item(item, "values"))
            current_values[5] = so_luong
            available_tree.item(item, values=tuple(current_values))

            product = current_values[:5] + [so_luong]
            found = False
            for i, p in enumerate(selected_products):
                if p[0] == ma_san_pham:
                    if so_luong > 0:
                        selected_products[i] = [p[0], p[1], p[2], p[3], so_luong, int(p[3]) * so_luong]
                    else:
                        selected_products.pop(i)
                    found = True
                    break
            if not found and so_luong > 0:
                selected_products.append([product[0], product[1], product[2], product[3], so_luong, int(product[3]) * so_luong])

            cap_nhat_danh_sach_san_pham_da_chon()
            new_window.destroy()

        tk.Button(new_window, text="Lưu", command=luu_so_luong).pack(pady=5)
        tk.Button(new_window, text="Hủy", command=new_window.destroy).pack(pady=5)

    available_tree.bind("<Double-1>", chon_so_luong)

    # Cập nhật danh sách sản phẩm đã chọn
    def cap_nhat_danh_sach_san_pham_da_chon():
        for item in tree.get_children():
            tree.delete(item)
        for product in selected_products:
            tree.insert("", tk.END, values=product)

    # Hàm cập nhật đơn hàng
    def handle_cap_nhat_don_hang():
        ma_don = entry_ma_don.get()
        if not ma_don:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã đơn hàng!")
            return

        sdt = entries["Số điện thoại khách hàng"].get()
        gio_dat = entries["Giờ đặt (HH:MM:SS)"].get()
        ngay_dat = entries["Ngày đặt (YYYY-MM-DD)"].get()
        pthuc_thanh_toan = entries["Phương thức thanh toán"].get()
        tthai_thanh_toan = entries["Trạng thái thanh toán"].get()
        tthai_van_don = entries["Trạng thái vận đơn"].get()

        if not all([sdt, gio_dat, ngay_dat, pthuc_thanh_toan, tthai_thanh_toan, tthai_van_don]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
            return

        connection = connect_db()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            # Kiểm tra khách hàng
            query_kh = "SELECT ma_khach_hang FROM khach_hang WHERE sdt = %s"
            cursor.execute(query_kh, (sdt,))
            khach_hang = cursor.fetchone()
            if not khach_hang:
                messagebox.showwarning("Lỗi", "Không tìm thấy khách hàng với số điện thoại này!")
                return
            ma_khach_hang = khach_hang[0]

            # Bắt đầu giao dịch
            cursor.execute("START TRANSACTION")

            # Cập nhật thông tin đơn hàng
            query_don_hang = """
                UPDATE don_hang 
                SET gio_dat = %s, ngay_dat = %s, pthuc_thanh_toan = %s, 
                    tthai_thanh_toan = %s, tthai_van_don = %s, ma_khach_hang = %s
                WHERE ma_don_hang = %s
            """
            cursor.execute(query_don_hang, (gio_dat, ngay_dat, pthuc_thanh_toan, tthai_thanh_toan, tthai_van_don, ma_khach_hang, ma_don))
            if cursor.rowcount == 0:
                raise Exception("Không tìm thấy đơn hàng để cập nhật!")

            # Lấy danh sách sản phẩm hiện tại trong đơn hàng
            query_old_products = """
                SELECT ma_san_pham, so_luong 
                FROM don_hang_san_pham 
                WHERE ma_don_hang = %s
            """
            cursor.execute(query_old_products, (ma_don,))
            old_products = {row[0]: row[1] for row in cursor.fetchall()}

            # Xóa các sản phẩm cũ
            cursor.execute("DELETE FROM don_hang_san_pham WHERE ma_don_hang = %s", (ma_don,))

            # Khôi phục số lượng tồn kho cho các sản phẩm cũ
            for ma_san_pham, so_luong in old_products.items():
                cursor.execute("""
                    UPDATE san_pham 
                    SET so_luong_ton_kho = so_luong_ton_kho + %s 
                    WHERE ma_san_pham = %s
                """, (so_luong, ma_san_pham))

            # Thêm sản phẩm mới và cập nhật tồn kho
            for product in selected_products:
                if product[4] and int(product[4]) > 0:  # Chỉ thêm nếu có số lượng
                    so_luong = int(product[4])
                    gia_ban = int(product[3])
                    thanh_tien = gia_ban * so_luong
                    cursor.execute("""
                        INSERT INTO don_hang_san_pham (ma_don_hang, ma_san_pham, gia_ban, so_luong, thanh_tien)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (ma_don, product[0], gia_ban, so_luong, thanh_tien))

                    cursor.execute("""
                        UPDATE san_pham 
                        SET so_luong_ton_kho = so_luong_ton_kho - %s 
                        WHERE ma_san_pham = %s AND so_luong_ton_kho >= %s
                    """, (so_luong, product[0], so_luong))
                    if cursor.rowcount == 0:
                        raise Exception(f"Số lượng tồn kho không đủ cho sản phẩm mã {product[0]}")

            # Cập nhật tổng tiền đơn hàng
            cursor.execute("""
                UPDATE don_hang 
                SET tong_tien = (SELECT SUM(thanh_tien) FROM don_hang_san_pham WHERE ma_don_hang = %s)
                WHERE ma_don_hang = %s
            """, (ma_don, ma_don))

            connection.commit()
            messagebox.showinfo("Thành công", f"Đã cập nhật đơn hàng mã {ma_don} thành công!")
            for entry in entries.values():
                if isinstance(entry, tk.Entry):
                    entry.delete(0, tk.END)
                elif isinstance(entry, ttk.Combobox):
                    entry.set("")
            entry_ma_don.delete(0, tk.END)
            selected_products.clear()
            for item in tree.get_children():
                tree.delete(item)
            cap_nhat_danh_sach_san_pham()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật đơn hàng: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    tk.Button(search_frame, text="Tìm kiếm", command=tim_kiem_don_hang).grid(row=1, column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Cập nhật đơn hàng", command=handle_cap_nhat_don_hang).grid(row=len(fields), column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)

# Form ghi nhận thanh toán
def show_ghi_nhan_thanh_toan_form(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Ghi nhận thanh toán", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame tìm kiếm đơn hàng
    search_frame = tk.LabelFrame(main_frame, text="Tìm kiếm đơn hàng", font=("Arial", 12))
    search_frame.pack(pady=10, fill="x")

    tk.Label(search_frame, text="Mã đơn hàng:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_ma_don = tk.Entry(search_frame)
    entry_ma_don.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    search_frame.grid_columnconfigure(1, weight=1)

    # Frame thông tin thanh toán
    form_frame = tk.LabelFrame(main_frame, text="Thông tin thanh toán", font=("Arial", 12))
    form_frame.pack(pady=10, fill="x")

    fields = ["Phương thức thanh toán", "Trạng thái thanh toán"]
    entries = {}

    for idx, field in enumerate(fields):
        tk.Label(form_frame, text=field + ":").grid(row=idx, column=0, padx=5, pady=5, sticky="e")
        if field == "Trạng thái thanh toán":
            entry = ttk.Combobox(form_frame, values=["Đã thanh toán", "Chưa thanh toán"], state="readonly")
            entry.set("Chưa thanh toán")
        else:
            entry = tk.Entry(form_frame)
            if field == "Phương thức thanh toán":
                entry.insert(0, "")
        entry.grid(row=idx, column=1, padx=5, pady=5, sticky="ew")
        entries[field] = entry
    form_frame.grid_columnconfigure(1, weight=1)

    # Hàm tìm kiếm đơn hàng
    def tim_kiem_don_hang():
        ma_don = entry_ma_don.get()
        if not ma_don:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã đơn hàng!")
            return

        connection = connect_db()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            query = """
                SELECT pthuc_thanh_toan, tthai_thanh_toan
                FROM don_hang 
                WHERE ma_don_hang = %s
            """
            cursor.execute(query, (ma_don,))
            don_hang = cursor.fetchone()

            if not don_hang:
                messagebox.showwarning("Không tìm thấy", "Không tìm thấy đơn hàng với mã này!")
                return

            entries["Phương thức thanh toán"].delete(0, tk.END)
            entries["Phương thức thanh toán"].insert(0, don_hang[0] or "")
            entries["Trạng thái thanh toán"].set(don_hang[1])

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm đơn hàng: {e}")
        finally:
            cursor.close()
            connection.close()

    # Hàm ghi nhận thanh toán
    def handle_ghi_nhan_thanh_toan():
        ma_don = entry_ma_don.get()
        if not ma_don:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã đơn hàng!")
            return

        pthuc_thanh_toan = entries["Phương thức thanh toán"].get()
        tthai_thanh_toan = entries["Trạng thái thanh toán"].get()

        if not pthuc_thanh_toan:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập phương thức thanh toán!")
            return

        connection = connect_db()
        if not connection:
            return

        try:
            cursor = connection.cursor()
            query = """
                UPDATE don_hang 
                SET pthuc_thanh_toan = %s, tthai_thanh_toan = %s
                WHERE ma_don_hang = %s
            """
            cursor.execute(query, (pthuc_thanh_toan, tthai_thanh_toan, ma_don))
            if cursor.rowcount == 0:
                raise Exception("Không tìm thấy đơn hàng để cập nhật!")

            connection.commit()
            messagebox.showinfo("Thành công", f"Đã ghi nhận thanh toán cho đơn hàng mã {ma_don}!")
            entry_ma_don.delete(0, tk.END)
            for entry in entries.values():
                if isinstance(entry, tk.Entry):
                    entry.delete(0, tk.END)
                elif isinstance(entry, ttk.Combobox):
                    entry.set("Chưa thanh toán")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi ghi nhận thanh toán: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    tk.Button(search_frame, text="Tìm kiếm", command=tim_kiem_don_hang).grid(row=1, column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Ghi nhận thanh toán", command=handle_ghi_nhan_thanh_toan).grid(row=len(fields), column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)