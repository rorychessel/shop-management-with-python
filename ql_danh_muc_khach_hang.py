import tkinter as tk
from tkinter import ttk, messagebox

from connection import connect_db

# Hàm thêm khách hàng
def them_khach_hang(ho_ten, dia_chi, sdt, email):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()

        # Thêm khách hàng vào bảng khach_hang
        query_khach_hang = """
            INSERT INTO khach_hang (ho_ten, dia_chi, sdt, email)
            VALUES (%s, %s, %s, %s)
        """
        values_khach_hang = (ho_ten, dia_chi, sdt, email)
        cursor.execute(query_khach_hang, values_khach_hang)
        connection.commit()
        ma_khach_hang_moi = cursor.lastrowid
        
        messagebox.showinfo("Thành công", 
                           f"Đã thêm khách hàng {ho_ten} với mã {ma_khach_hang_moi} thành công!\n")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi thêm khách hàng: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

# Hàm sửa khách hàng
def sua_khach_hang(ma_khach_hang, **kwargs):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        updates = [f"{key} = %s" for key in kwargs.keys()]
        query = f"""
            UPDATE khach_hang 
            SET {', '.join(updates)}
            WHERE ma_khach_hang = %s
        """
        values = list(kwargs.values()) + [ma_khach_hang]
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Thành công", f"Đã cập nhật thông tin khách hàng có mã {ma_khach_hang} thành công!")
        else:
            messagebox.showwarning("Không tìm thấy", f"Không tìm thấy khách hàng với mã {ma_khach_hang}.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi sửa khách hàng: {e}")
    finally:
        cursor.close()
        connection.close()

# Hàm xóa khách hàng
def xoa_khach_hang(ma_khach_hang):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        query = "DELETE FROM khach_hang WHERE ma_khach_hang = %s"
        cursor.execute(query, (ma_khach_hang,))
        connection.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Thành công", f"Đã xóa khách hàng có mã {ma_khach_hang} thành công!")
        else:
            messagebox.showwarning("Không tìm thấy", f"Không tìm thấy khách hàng với mã {ma_khach_hang}.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi xóa khách hàng: {e}")
    finally:
        cursor.close()
        connection.close()

# Hàm tìm kiếm khách hàng
def tim_kiem_khach_hang(window, current_user, current_user_role, back_callback, **kwargs):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        conditions = []
        values = []
        
        if kwargs.get("ma_khach_hang"):
            conditions.append("ma_khach_hang = %s")
            values.append(int(kwargs["ma_khach_hang"]))
        if kwargs.get("ho_ten"):
            conditions.append("ho_ten LIKE %s")
            values.append(f"%{kwargs['ho_ten']}%")
        if kwargs.get("dia_chi"):
            conditions.append("dia_chi LIKE %s")
            values.append(f"%{kwargs['dia_chi']}%")
        if kwargs.get("sdt"):
            conditions.append("sdt LIKE %s")
            values.append(f"%{kwargs['sdt']}%")
        if kwargs.get("email"):
            conditions.append("email LIKE %s")
            values.append(f"%{kwargs['email']}%")

        if not conditions:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập ít nhất một tiêu chí tìm kiếm!")
            return

        query = f"""
            SELECT *
            FROM khach_hang
            WHERE {' AND '.join(conditions)}
        """
        cursor.execute(query, values)
        rows = cursor.fetchall()
        
        for widget in window.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(window)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        label_title = tk.Label(main_frame, text="Kết quả tìm kiếm khách hàng", font=("Arial", 14))
        label_title.pack(pady=10)
        
        columns = ("Mã KH", "Họ tên", "Địa chỉ", "SĐT", "Email")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        
        if rows:
            for row in rows:
                tree.insert("", tk.END, values=row)
        else:
            messagebox.showinfo("Kết quả", "Không tìm thấy khách hàng nào phù hợp!")
        
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.pack(pady=10, fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        btn_back = tk.Button(main_frame, text="Quay lại", command=lambda: show_khach_hang_form(window, current_user, current_user_role, back_callback))
        btn_back.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm khách hàng: {e}")
    finally:
        cursor.close()
        connection.close()

# Hàm xem danh sách khách hàng
def xem_danh_sach_khach_hang(window, current_user, current_user_role, back_callback):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT *
            FROM khach_hang
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for widget in window.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(window)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        label_title = tk.Label(main_frame, text="Danh sách khách hàng", font=("Arial", 14))
        label_title.pack(pady=10)
        
        columns = ("Mã KH", "Họ tên", "Địa chỉ", "SĐT", "Email")
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
        
        btn_back = tk.Button(main_frame, text="Quay lại", command=lambda: show_khach_hang_form(window, current_user, current_user_role, back_callback))
        btn_back.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách khách hàng: {e}")
    finally:
        cursor.close()
        connection.close()

# Form quản lý khách hàng
def show_khach_hang_form(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Quản lý khách hàng", font=("Arial", 14))
    label_title.pack(pady=10)

    form_frame = tk.Frame(main_frame)
    form_frame.pack(pady=10)

    fields = ["Họ tên", "Địa chỉ", "Số điện thoại", "Email"]
    entries = {}

    for idx, field in enumerate(fields):
        tk.Label(form_frame, text=field + ":").grid(row=idx, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(form_frame)
        entry.grid(row=idx, column=1, padx=5, pady=5, sticky="ew")
        entries[field] = entry

    form_frame.grid_columnconfigure(1, weight=1)

    def handle_them_khach_hang():
        ho_ten = entries["Họ tên"].get()
        dia_chi = entries["Địa chỉ"].get()
        sdt = entries["Số điện thoại"].get()
        email = entries["Email"].get()

        if not all([ho_ten, dia_chi, sdt, email]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
            return

        them_khach_hang(ho_ten, dia_chi, sdt, email)

    def handle_sua_khach_hang():
        ma_khach_hang = entries["Mã khách hàng (để sửa/xóa)"].get()
        if not ma_khach_hang:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã khách hàng!")
            return

        kwargs = {}
        if entries["Họ tên"].get():
            kwargs["ho_ten"] = entries["Họ tên"].get()
        if entries["Địa chỉ"].get():
            kwargs["dia_chi"] = entries["Địa chỉ"].get()
        if entries["Số điện thoại"].get():
            kwargs["sdt"] = entries["Số điện thoại"].get()
        if entries["Email"].get():
            kwargs["email"] = entries["Email"].get()

        if not kwargs:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập ít nhất một trường để sửa!")
            return

        sua_khach_hang(int(ma_khach_hang), **kwargs)

    def handle_xoa_khach_hang():
        ma_khach_hang = entries["Mã khách hàng (để sửa/xóa)"].get()
        if not ma_khach_hang:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã khách hàng!")
            return

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa khách hàng có mã {ma_khach_hang}?"):
            xoa_khach_hang(int(ma_khach_hang))

    search_frame = tk.LabelFrame(main_frame, text="Tìm kiếm khách hàng", font=("Arial", 12))
    search_frame.pack(pady=10, fill="x")

    search_fields = ["Mã khách hàng", "Họ tên", "Địa chỉ", "Số điện thoại", "Email"]
    search_entries = {}

    for idx, field in enumerate(search_fields):
        tk.Label(search_frame, text=field + ":").grid(row=0, column=idx*2, padx=5, pady=5, sticky="e")
        entry = tk.Entry(search_frame, width=15)
        entry.grid(row=0, column=idx*2+1, padx=5, pady=5, sticky="ew")
        search_entries[field] = entry

    search_frame.grid_columnconfigure((1, 3, 5, 7, 11), weight=1)

    def handle_tim_kiem():
        kwargs = {}
        if search_entries["Mã khách hàng"].get():
            kwargs["ma_khach_hang"] = search_entries["Mã khách hàng"].get()
        if search_entries["Họ tên"].get():
            kwargs["ho_ten"] = search_entries["Họ tên"].get()
        if search_entries["Địa chỉ"].get():
            kwargs["dia_chi"] = search_entries["Địa chỉ"].get()
        if search_entries["Số điện thoại"].get():
            kwargs["sdt"] = search_entries["Số điện thoại"].get()
        if search_entries["Email"].get():
            kwargs["email"] = search_entries["Email"].get()

        tim_kiem_khach_hang(window, current_user, current_user_role, back_callback, **kwargs)

    tk.Button(form_frame, text="Thêm khách hàng", command=handle_them_khach_hang).grid(row=len(fields), column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Sửa khách hàng", command=handle_sua_khach_hang).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Xóa khách hàng", command=handle_xoa_khach_hang).grid(row=len(fields)+2, column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Xem danh sách", command=lambda: xem_danh_sach_khach_hang(window, current_user, current_user_role, back_callback)).grid(row=len(fields)+3, column=0, columnspan=2, pady=5)
    tk.Button(search_frame, text="Tìm kiếm", command=handle_tim_kiem).grid(row=1, column=0, columnspan=len(search_fields)*2, pady=5)
    tk.Button(form_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).grid(row=len(fields)+4, column=0, columnspan=2, pady=5)