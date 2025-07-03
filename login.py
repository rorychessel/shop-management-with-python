import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import menu  # Import menu module

from connection import connect_db

# Biến toàn cục để lưu thông tin người dùng
current_user = None
current_user_role = None
window = None  # Khai báo window để sử dụng chung

def login():
    global current_user, current_user_role
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
        return
    
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT tk.id_tai_khoan, tk.ten_dang_nhap, ns.chuc_vu FROM tai_khoan tk " \
                    "JOIN nhan_su ns ON tk.id_tai_khoan = ns.id_tai_khoan " \
                    "WHERE tk.ten_dang_nhap = %s AND tk.mat_khau = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            
            if result:
                global current_user, current_user_role
                current_user = result[1]  # ten_dang_nhap
                current_user_role = result[2]  # chuc_vu
                print(f"current_user: '{current_user}'")
                print(f"current_user_role: '{current_user_role}'")
                messagebox.showinfo("Thành công", f"Đăng nhập thành công! Xin chào {current_user} ({current_user_role})")
                # Chuyển sang giao diện menu ngay trong cùng cửa sổ
                menu.show_main_menu(window, current_user, current_user_role)
            else:
                messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
                
        except Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi truy vấn cơ sở dữ liệu: {e}")
        finally:
            cursor.close()
            connection.close()

# Tạo và chạy ứng dụng
window = tk.Tk()
window.title("Hệ thống quản lý cửa hàng")
window.state("zoomed")  # Mở toàn màn hình

# Frame chính
main_frame = tk.Frame(window)
main_frame.pack(expand=True)

# Frame chứa form đăng nhập
login_frame = tk.Frame(main_frame)
login_frame.pack(pady=50)

label_username = tk.Label(login_frame, text="Tên đăng nhập:")
label_username.pack(pady=5)
entry_username = tk.Entry(login_frame)
entry_username.pack(pady=5)

label_password = tk.Label(login_frame, text="Mật khẩu:")
label_password.pack(pady=5)
entry_password = tk.Entry(login_frame, show="*")
entry_password.pack(pady=5)

button_login = tk.Button(login_frame, text="Đăng nhập", command=login)
button_login.pack(pady=10)

window.mainloop()