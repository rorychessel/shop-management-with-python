import tkinter as tk
from tkinter import ttk, messagebox
from connection import connect_db

def show_doi_mat_khau(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Đổi mật khẩu", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame nhập liệu
    input_frame = tk.LabelFrame(main_frame, text="Thông tin đổi mật khẩu", font=("Arial", 12))
    input_frame.pack(pady=10, fill="x")

    # Nhập tên đăng nhập
    tk.Label(input_frame, text="Tên đăng nhập:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_ten_dang_nhap = tk.Entry(input_frame, font=("Arial", 12))
    entry_ten_dang_nhap.grid(row=0, column=1, padx=5, pady=5)

    # Nhập mật khẩu mới
    tk.Label(input_frame, text="Mật khẩu mới:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_mat_khau_moi = tk.Entry(input_frame, show="*", font=("Arial", 12))
    entry_mat_khau_moi.grid(row=1, column=1, padx=5, pady=5)

    # Nhập xác nhận mật khẩu mới
    tk.Label(input_frame, text="Xác nhận mật khẩu:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_xac_nhan_mat_khau = tk.Entry(input_frame, show="*", font=("Arial", 12))
    entry_xac_nhan_mat_khau.grid(row=2, column=1, padx=5, pady=5)

    # Hàm kiểm tra tên đăng nhập tồn tại
    def kiem_tra_ten_dang_nhap(ten_dang_nhap):
        connection = connect_db()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            query = "SELECT COUNT(*) FROM tai_khoan WHERE ten_dang_nhap = %s"
            cursor.execute(query, (ten_dang_nhap,))
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi kiểm tra tên đăng nhập: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    # Hàm đổi mật khẩu
    def doi_mat_khau():
        ten_dang_nhap = entry_ten_dang_nhap.get().strip()
        mat_khau_moi = entry_mat_khau_moi.get()
        xac_nhan_mat_khau = entry_xac_nhan_mat_khau.get()

        # Kiểm tra đầu vào
        if not ten_dang_nhap:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập!")
            return
        if mat_khau_moi != xac_nhan_mat_khau:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return
        if not kiem_tra_ten_dang_nhap(ten_dang_nhap):
            messagebox.showerror("Lỗi", f"Tên đăng nhập {ten_dang_nhap} không tồn tại!")
            return

        # Cập nhật mật khẩu
        connection = connect_db()
        if connection is None:
            messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu!")
            return
        try:
            cursor = connection.cursor()
            query1 = "SELECT mat_khau FROM tai_khoan WHERE ten_dang_nhap = %s"
            cursor.execute(query1, (ten_dang_nhap,))
            mat_khau_cu = cursor.fetchone()
            if mat_khau_cu is None:
                messagebox.showerror("Lỗi", f"Tên đăng nhập {ten_dang_nhap} không tồn tại!")
                return
            if mat_khau_cu[0] == mat_khau_moi:
                messagebox.showerror("Lỗi", "Mật khẩu mới không được trùng với mật khẩu cũ!")
                return
            else:
                query2 = "UPDATE tai_khoan SET mat_khau = %s WHERE ten_dang_nhap = %s"
                cursor.execute(query2, (mat_khau_moi, ten_dang_nhap))
                connection.commit()
                messagebox.showinfo("Thành công", "Đổi mật khẩu thành công!")
            # Xóa các trường nhập sau khi thành công
            entry_ten_dang_nhap.delete(0, tk.END)
            entry_mat_khau_moi.delete(0, tk.END)
            entry_xac_nhan_mat_khau.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đổi mật khẩu: {e}")
        finally:
            cursor.close()
            connection.close()

    # Nút thực hiện đổi mật khẩu
    tk.Button(main_frame, text="Đổi mật khẩu", command=doi_mat_khau, font=("Arial", 12)).pack(pady=5)
    # Nút quay lại
    tk.Button(main_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role), font=("Arial", 12)).pack(pady=5)