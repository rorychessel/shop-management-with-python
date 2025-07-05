import tkinter as tk
from tkinter import ttk, messagebox

from connection import connect_db
    
# Hàm thêm sản phẩm
def them_san_pham(ten, kich_co, gia_ban, so_luong_ton_kho, mo_ta):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()

        # Thêm sản phẩm vào bảng san_pham
        query_san_pham = """
            INSERT INTO san_pham (ten, kich_co, gia_ban, so_luong_ton_kho, mo_ta)
            VALUES (%s, %s, %s, %s, %s)
        """
        values_san_pham = (ten, kich_co, gia_ban, so_luong_ton_kho, mo_ta)
        cursor.execute(query_san_pham, values_san_pham)
        connection.commit()
        ma_san_pham_moi = cursor.lastrowid
        
        messagebox.showinfo("Thành công", 
                           f"Đã thêm sản phẩm {ten} với mã {ma_san_pham_moi} thành công!\n")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi thêm sản phẩm: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

# Hàm sửa sản phẩm
def sua_san_pham(ma_san_pham, **kwargs):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        updates = [f"{key} = %s" for key in kwargs.keys()]
        query = f"""
            UPDATE san_pham 
            SET {', '.join(updates)}
            WHERE ma_san_pham = %s
        """
        values = list(kwargs.values()) + [ma_san_pham]
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Thành công", f"Đã cập nhật thông tin sản phẩm có mã {ma_san_pham} thành công!")
        else:
            messagebox.showwarning("Không tìm thấy", f"Không tìm thấy sản phẩm với mã {ma_san_pham}.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi sửa sản phẩm: {e}")
    finally:
        cursor.close()
        connection.close()

# Hàm xóa sản phẩm
def xoa_san_pham(ma_san_pham):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        query = "DELETE FROM san_pham WHERE ma_san_pham = %s"
        cursor.execute(query, (ma_san_pham,))
        connection.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Thành công", f"Đã xóa sản phẩm có mã {ma_san_pham} thành công!")
        else:
            messagebox.showwarning("Không tìm thấy", f"Không tìm thấy sản phẩm với mã {ma_san_pham}.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi xóa sản phẩm: {e}")
    finally:
        cursor.close()
        connection.close()

# Hàm tìm kiếm sản phẩm
def tim_kiem_san_pham(window, current_user, current_user_role, back_callback, **kwargs):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        conditions = []
        values = []
        
        if kwargs.get("ma_san_pham"):
            conditions.append("ma_san_pham = %s")
            values.append(int(kwargs["ma_san_pham"]))
        if kwargs.get("ten"):
            conditions.append("ten LIKE %s")
            values.append(f"%{kwargs['ten']}%")
        if kwargs.get("kich_co"):
            conditions.append("kich_co LIKE %s")
            values.append(f"%{kwargs['kich_co']}%")
        if kwargs.get("gia_ban"):
            conditions.append("gia_ban <= %s")
            values.append(float(kwargs["gia_ban"]))  # Chuyển sang float, bỏ dấu %
        if kwargs.get("so_luong_ton_kho"):
            conditions.append("so_luong_ton_kho <= %s")
            values.append(int(kwargs["so_luong_ton_kho"]))  # Chuyển sang int, bỏ dấu %
        if kwargs.get("mo_ta"):
            conditions.append("mo_ta LIKE %s")
            values.append(f"%{kwargs['mo_ta']}%")

        if not conditions:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập ít nhất một tiêu chí tìm kiếm!")
            return

        query = f"""
            SELECT ma_san_pham, ten, kich_co, gia_ban, so_luong_ton_kho, mo_ta
            FROM san_pham
            WHERE {' AND '.join(conditions)}
        """
        cursor.execute(query, values)
        rows = cursor.fetchall()
        
        for widget in window.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(window)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        label_title = tk.Label(main_frame, text="Kết quả tìm kiếm sản phẩm", font=("Arial", 14))
        label_title.pack(pady=10)
        
        columns = ("Mã SP", "Tên", "Kích cỡ", "Giá bán", "Số lượng tồn kho", "Mô tả")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        if rows:
            for row in rows:
                tree.insert("", tk.END, values=row)
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy sản phẩm nào phù hợp!")
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(pady=10, fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        btn_back = tk.Button(main_frame, text="Quay lại", command=lambda: show_san_pham_form(window, current_user, current_user_role, back_callback))
        btn_back.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm sản phẩm: {e}")
    finally:
        cursor.close()
        connection.close()

# Hàm xem danh sách sản phẩm
def xem_danh_sach_san_pham(window, current_user, current_user_role, back_callback):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT ma_san_pham, ten, kich_co, gia_ban, so_luong_ton_kho, mo_ta 
            FROM san_pham
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for widget in window.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(window)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        label_title = tk.Label(main_frame, text="Danh sách sản phẩm", font=("Arial", 14))
        label_title.pack(pady=10)
        
        columns = ("Mã SP", "Tên", "Kích cỡ", "Giá bán", "Số lượng tồn kho", "Mô tả")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        for row in rows:
            tree.insert("", tk.END, values=row)
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(pady=10, fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        btn_back = tk.Button(main_frame, text="Quay lại", command=lambda: show_san_pham_form(window, current_user, current_user_role, back_callback) if current_user_role.strip().lower() == "quản lý" else back_callback(window, current_user, current_user_role))
        btn_back.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách sản phẩm: {e}")
    finally:
        cursor.close()
        connection.close()

# Form quản lý sản phẩm
def show_san_pham_form(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Quản lý sản phẩm", font=("Arial", 14))
    label_title.pack(pady=10)

    form_frame = tk.Frame(main_frame)
    form_frame.pack(pady=10)

    fields = ["Tên sản phẩm", "Kích cỡ", "Giá bán", "Số lượng tồn kho", "Mô tả", 
              "Mã sản phẩm (để sửa/xóa)"]
    entries = {}

    for idx, field in enumerate(fields):
        tk.Label(form_frame, text=field + ":").grid(row=idx, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(form_frame)
        entry.grid(row=idx, column=1, padx=5, pady=5, sticky="ew")
        entries[field] = entry

    form_frame.grid_columnconfigure(1, weight=1)

    def handle_them_san_pham():
        ten = entries["Tên sản phẩm"].get()
        kich_co = entries["Kích cỡ"].get()
        gia_ban = entries["Giá bán"].get()
        so_luong_ton_kho = entries["Số lượng tồn kho"].get()
        mo_ta = entries["Mô tả"].get()

        if not all([ten, kich_co, gia_ban, so_luong_ton_kho, mo_ta]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
            return

        them_san_pham(ten, kich_co, gia_ban, so_luong_ton_kho, mo_ta)

    def handle_sua_san_pham():
        ma_san_pham = entries["Mã sản phẩm (để sửa/xóa)"].get()
        if not ma_san_pham:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã sản phẩm!")
            return

        kwargs = {}
        if entries["Tên sản phẩm"].get():
            kwargs["ten"] = entries["Tên sản phẩm"].get()
        if entries["Kích cỡ"].get():
            kwargs["kich_co"] = entries["Kích cỡ"].get()
        if entries["Giá bán"].get():
            kwargs["gia_ban"] = entries["Giá bán"].get()
        if entries["Số lượng tồn kho"].get():
            kwargs["so_luong_ton_kho"] = entries["Số lượng tồn kho"].get()
        if entries["Mô tả"].get():
            kwargs["mo_ta"] = entries["Mô tả"].get()

        if not kwargs:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập ít nhất một trường để sửa!")
            return

        sua_san_pham(int(ma_san_pham), **kwargs)

    def handle_xoa_san_pham():
        ma_san_pham = entries["Mã sản phẩm (để sửa/xóa)"].get()
        if not ma_san_pham:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã sản phẩm!")
            return

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sản phẩm có mã {ma_san_pham}?"):
            xoa_san_pham(int(ma_san_pham))

    search_frame = tk.LabelFrame(main_frame, text="Tìm kiếm sản phẩm", font=("Arial", 12))
    search_frame.pack(pady=10, fill="x")

    search_fields = ["Mã sản phẩm", "Tên", "Kích cỡ", "Giá bán", "Số lượng tồn kho", "Mô tả"]
    search_entries = {}

    for idx, field in enumerate(search_fields):
        tk.Label(search_frame, text=field + ":").grid(row=0, column=idx*2, padx=5, pady=5, sticky="e")
        entry = tk.Entry(search_frame, width=15)
        entry.grid(row=0, column=idx*2+1, padx=5, pady=5, sticky="ew")
        search_entries[field] = entry

    search_frame.grid_columnconfigure((1, 3, 5, 7, 9, 11), weight=1)

    def handle_tim_kiem():
        kwargs = {}
        try:
            if search_entries["Mã sản phẩm"].get():
                kwargs["ma_san_pham"] = search_entries["Mã sản phẩm"].get()
            if search_entries["Tên"].get():
                kwargs["ten"] = search_entries["Tên"].get()
            if search_entries["Kích cỡ"].get():
                kwargs["kich_co"] = search_entries["Kích cỡ"].get()
            if search_entries["Giá bán"].get():
                kwargs["gia_ban"] = float(search_entries["Giá bán"].get())  # Kiểm tra giá bán là số
            if search_entries["Số lượng tồn kho"].get():
                kwargs["so_luong_ton_kho"] = int(search_entries["Số lượng tồn kho"].get())  # Kiểm tra số lượng là số nguyên
            if search_entries["Mô tả"].get():
                kwargs["mo_ta"] = search_entries["Mô tả"].get()

            if not kwargs:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập ít nhất một tiêu chí tìm kiếm!")
                return

            tim_kiem_san_pham(window, current_user, current_user_role, back_callback, **kwargs)
        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Giá bán phải là số thực, số lượng tồn kho phải là số nguyên!")

    tk.Button(form_frame, text="Thêm sản phẩm", command=handle_them_san_pham).grid(row=len(fields), column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Sửa sản phẩm", command=handle_sua_san_pham).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Xóa sản phẩm", command=handle_xoa_san_pham).grid(row=len(fields)+2, column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Xem danh sách", command=lambda: xem_danh_sach_san_pham(window, current_user, current_user_role, back_callback)).grid(row=len(fields)+3, column=0, columnspan=2, pady=5)
    tk.Button(search_frame, text="Tìm kiếm", command=handle_tim_kiem).grid(row=1, column=0, columnspan=len(search_fields)*2, pady=5)
    tk.Button(form_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).grid(row=len(fields)+4, column=0, columnspan=2, pady=5)