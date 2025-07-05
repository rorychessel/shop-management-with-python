import tkinter as tk
from tkinter import ttk, messagebox

from connection import connect_db

# Hàm thêm quản lý
def them_quan_ly(ho_ten, ngay_sinh, dia_chi, sdt, email, cccd, ngay_vao_lam, ten_tai_khoan, mat_khau):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        
        # Tạo tài khoản trong bảng tai_khoan
        chuc_vu = "Quản lý"
        query_tai_khoan = """
            INSERT INTO tai_khoan (ten_dang_nhap, mat_khau)
            VALUES (%s, %s)
        """
        values_tai_khoan = (ten_tai_khoan, mat_khau)
        cursor.execute(query_tai_khoan, values_tai_khoan)
        connection.commit()
        id_tai_khoan = cursor.lastrowid

        # Thêm quản lý vào bảng nhan_su
        query_nhan_su = """
            INSERT INTO nhan_su (ho_ten, ngay_sinh, dia_chi, sdt, email, cccd, ngay_vao_lam, chuc_vu, id_tai_khoan)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values_nhan_su = (ho_ten, ngay_sinh, dia_chi, sdt, email, cccd, ngay_vao_lam, chuc_vu, id_tai_khoan)
        cursor.execute(query_nhan_su, values_nhan_su)
        connection.commit()
        ma_nhan_su_moi = cursor.lastrowid
        
        messagebox.showinfo("Thành công", 
                           f"Đã thêm quản lý {ho_ten} với mã {ma_nhan_su_moi} thành công!\n"
                           f"Tài khoản: Tên đăng nhập = {ten_tai_khoan}, Mật khẩu = {mat_khau}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi thêm quản lý: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

# Hàm sửa quản lý
def sua_quan_ly(ma_nhan_su, **kwargs):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        updates = [f"{key} = %s" for key in kwargs.keys()]
        query = f"""
            UPDATE nhan_su 
            SET {', '.join(updates)}
            WHERE chuc_vu = 'Quản lý' AND ma_nhan_su = %s
        """
        values = list(kwargs.values()) + [ma_nhan_su]
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Thành công", f"Đã cập nhật thông tin quản lý có mã {ma_nhan_su} thành công!")
        else:
            messagebox.showwarning("Không tìm thấy", f"Không tìm thấy quản lý với mã {ma_nhan_su}.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi sửa quản lý: {e}")
    finally:
        cursor.close()
        connection.close()

# Hàm xóa quản lý
def xoa_quan_ly(ma_nhan_su):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        query = "DELETE FROM nhan_su WHERE chuc_vu = 'Quản lý' AND ma_nhan_su = %s"
        cursor.execute(query, (ma_nhan_su,))
        connection.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Thành công", f"Đã xóa quản lý có mã {ma_nhan_su} thành công! (Tài khoản cũng đã bị xóa.)")
        else:
            messagebox.showwarning("Không tìm thấy", f"Không tìm thấy quản lý với mã {ma_nhan_su}.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi xóa quản lý: {e}")
    finally:
        cursor.close()
        connection.close()

# Hàm xem danh sách quản lý
def xem_danh_sach_quan_ly(window, current_user, current_user_role, back_callback):
    connection = connect_db()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT ma_nhan_su, ho_ten, ngay_sinh, dia_chi, sdt, email, cccd, ngay_vao_lam, chuc_vu, id_tai_khoan 
            FROM nhan_su
            WHERE chuc_vu = 'Quản lý'
            ORDER BY ma_nhan_su
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Xóa giao diện hiện tại
        for widget in window.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(window)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        label_title = tk.Label(main_frame, text="Danh sách quản lý", font=("Arial", 14))
        label_title.pack(pady=10)
        
        columns = ("Mã NS", "Họ tên", "Ngày sinh", "Địa chỉ", "SĐT", "Email", "CCCD", "Ngày vào làm", "Chức vụ", "ID TK")
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
        
        btn_back = tk.Button(main_frame, text="Quay lại", command=lambda: show_quan_ly_form(window, current_user, current_user_role, back_callback) if current_user_role.strip().lower() == "quản lý" else back_callback(window, current_user, current_user_role))
        btn_back.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách quản lý: {e}")
    finally:
        cursor.close()
        connection.close()

# Form quản lý người quản lý
def show_quan_ly_form(window, current_user, current_user_role, back_callback):
    # Xóa giao diện hiện tại
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Quản lý người quản lý", font=("Arial", 14))
    label_title.pack(pady=10)

    form_frame = tk.Frame(main_frame)
    form_frame.pack(pady=10)

    fields = ["Họ tên", "Ngày sinh (YYYY-MM-DD)", "Địa chỉ", "Số điện thoại", "Email", 
              "CCCD", "Ngày vào làm (YYYY-MM-DD)", "Mã nhân sự (để sửa/xóa)", "Tên tài khoản", "Mật khẩu"]
    entries = {}

    for idx, field in enumerate(fields):
        tk.Label(form_frame, text=field + ":").grid(row=idx, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(form_frame)
        entry.grid(row=idx, column=1, padx=5, pady=5, sticky="ew")
        entries[field] = entry

    form_frame.grid_columnconfigure(1, weight=1)

    def handle_them_quan_ly():
        ho_ten = entries["Họ tên"].get()
        ngay_sinh = entries["Ngày sinh (YYYY-MM-DD)"].get()
        dia_chi = entries["Địa chỉ"].get()
        sdt = entries["Số điện thoại"].get()
        email = entries["Email"].get()
        cccd = entries["CCCD"].get()
        ngay_vao_lam = entries["Ngày vào làm (YYYY-MM-DD)"].get()
        ten_tai_khoan = entries["Tên tài khoản"].get()
        mat_khau = entries["Mật khẩu"].get()

        if not all([ho_ten, ngay_sinh, dia_chi, sdt, email, cccd, ngay_vao_lam, ten_tai_khoan, mat_khau]):
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
            return

        them_quan_ly(ho_ten, ngay_sinh, dia_chi, sdt, email, cccd, ngay_vao_lam, ten_tai_khoan, mat_khau)

    def handle_sua_quan_ly():
        ma_nhan_su = entries["Mã nhân sự (để sửa/xóa)"].get()
        if not ma_nhan_su:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã nhân sự!")
            return

        kwargs = {}
        if entries["Họ tên"].get():
            kwargs["ho_ten"] = entries["Họ tên"].get()
        if entries["Ngày sinh (YYYY-MM-DD)"].get():
            kwargs["ngay_sinh"] = entries["Ngày sinh (YYYY-MM-DD)"].get()
        if entries["Địa chỉ"].get():
            kwargs["dia_chi"] = entries["Địa chỉ"].get()
        if entries["Số điện thoại"].get():
            kwargs["sdt"] = entries["Số điện thoại"].get()
        if entries["Email"].get():
            kwargs["email"] = entries["Email"].get()
        if entries["CCCD"].get():
            kwargs["cccd"] = entries["CCCD"].get()
        if entries["Ngày vào làm (YYYY-MM-DD)"].get():
            kwargs["ngay_vao_lam"] = entries["Ngày vào làm (YYYY-MM-DD)"].get()

        if not kwargs:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập ít nhất một trường để sửa!")
            return

        sua_quan_ly(int(ma_nhan_su), **kwargs)

    def handle_xoa_quan_ly():
        ma_nhan_su = entries["Mã nhân sự (để sửa/xóa)"].get()
        if not ma_nhan_su:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã nhân sự!")
            return

        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa quản lý có mã {ma_nhan_su}?"):
            xoa_quan_ly(int(ma_nhan_su))

    tk.Button(form_frame, text="Thêm quản lý", command=handle_them_quan_ly).grid(row=len(fields), column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Sửa quản lý", command=handle_sua_quan_ly).grid(row=len(fields)+1, column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Xóa quản lý", command=handle_xoa_quan_ly).grid(row=len(fields)+2, column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Xem danh sách", command=lambda: xem_danh_sach_quan_ly(window, current_user, current_user_role, back_callback)).grid(row=len(fields)+3, column=0, columnspan=2, pady=5)
    tk.Button(form_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).grid(row=len(fields)+4, column=0, columnspan=2, pady=5)