import tkinter as tk
from tkinter import ttk, messagebox
from connection import connect_db
from datetime import datetime

def show_ho_so_ca_nhan(window, current_user, current_user_role, back_callback):
    for widget in window.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    label_title = tk.Label(main_frame, text="Hồ sơ cá nhân", font=("Arial", 14))
    label_title.pack(pady=10)

    # Frame hiển thị thông tin
    info_frame = tk.LabelFrame(main_frame, text="Thông tin cá nhân", font=("Arial", 12))
    info_frame.pack(pady=10, fill="x")

    # Hàm lấy thông tin người dùng
    def lay_thong_tin_nguoi_dung():
        connection = connect_db()
        if connection is None:
            messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu!")
            return None
        try:
            cursor = connection.cursor()
            query = """
                SELECT ns.ho_ten, ns.ngay_sinh, ns.dia_chi, ns.sdt, ns.email, 
                       ns.cccd, ns.ngay_vao_lam, ns.chuc_vu, tk.ten_dang_nhap
                FROM nhan_su ns
                JOIN tai_khoan tk ON ns.id_tai_khoan = tk.id_tai_khoan
                WHERE tk.ten_dang_nhap = %s
            """
            cursor.execute(query, (current_user,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy thông tin người dùng: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    # Lấy thông tin người dùng
    thong_tin = lay_thong_tin_nguoi_dung()
    if thong_tin is None:
        tk.Label(info_frame, text="Không tìm thấy thông tin người dùng!", font=("Arial", 12), fg="red").pack(pady=10)
    else:
        ho_ten, ngay_sinh, dia_chi, sdt, email, cccd, ngay_vao_lam, chuc_vu, ten_dang_nhap = thong_tin
        
        # Hiển thị thông tin dưới dạng nhãn
        tk.Label(info_frame, text=f"Họ tên: {ho_ten}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(info_frame, text=f"Ngày sinh: {ngay_sinh}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(info_frame, text=f"Địa chỉ: {dia_chi}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(info_frame, text=f"Số điện thoại: {sdt}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(info_frame, text=f"Email: {email}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(info_frame, text=f"CCCD: {cccd}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(info_frame, text=f"Ngày vào làm: {ngay_vao_lam}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(info_frame, text=f"Chức vụ: {chuc_vu}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)
        tk.Label(info_frame, text=f"Tên đăng nhập: {ten_dang_nhap}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

    # Nút quay lại
    tk.Button(main_frame, text="Quay lại", command=lambda: back_callback(window, current_user, current_user_role)).pack(pady=10)