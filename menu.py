import tkinter as tk
from tkinter import ttk, messagebox

import ql_danh_muc_nhan_vien
import ql_danh_muc_ng_quan_ly
import ql_danh_muc_khach_hang
import ql_danh_muc_san_pham
import ql_don_hang

from connection import connect_db

# Menu chính
def show_main_menu(window, current_user, current_user_role):
    for widget in window.winfo_children():
        widget.destroy()
    
    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    label_welcome = tk.Label(main_frame, text=f"Chào mừng {current_user} ({current_user_role})", font=("Arial", 14))
    label_welcome.pack(pady=10)
    
    if current_user_role.strip().lower() == "quản lý":
        btn_danh_muc = tk.Button(main_frame, text="Quản lý danh mục", command=lambda: ql_danh_muc(window, current_user, current_user_role))
        btn_danh_muc.pack(pady=5)
        
        btn_dat_hang = tk.Button(main_frame, text="Quản lý quy trình đặt hàng", command=lambda: ql_quy_trinh_dat_hang(window, current_user, current_user_role))
        btn_dat_hang.pack(pady=5)
        
        btn_nhap_hang = tk.Button(main_frame, text="Quản lý nhập hàng", command=lambda: ql_nhap_hang(window, current_user, current_user_role))
        btn_nhap_hang.pack(pady=5)
        
        btn_bao_cao = tk.Button(main_frame, text="Báo cáo & thống kê", command=lambda: bao_cao(window, current_user, current_user_role))
        btn_bao_cao.pack(pady=5)
        
        btn_ho_so = tk.Button(main_frame, text="Quản lý hồ sơ", command=lambda: ql_ho_so(window))
        btn_ho_so.pack(pady=5)

        btn_doi_mk = tk.Button(main_frame, text="Đổi mật khẩu", command=lambda: doi_mat_khau(window))
        btn_doi_mk.pack(pady=5)
    
        btn_dang_xuat = tk.Button(main_frame, text="Đăng xuất", command=lambda: thoat_app(window))
        btn_dang_xuat.pack(pady=10)

# Submenu Quản lý danh mục
def show_option1_menu(window, current_user, current_user_role):
    for widget in window.winfo_children():
        widget.destroy()
    
    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    label_title = tk.Label(main_frame, text="Quản lý danh mục", font=("Arial", 14))
    label_title.pack(pady=10)
    
    btn_nhan_vien = tk.Button(main_frame, text="Nhân viên", command=lambda: ql_danh_muc_nhan_vien.show_nhan_vien_form(window, current_user, current_user_role, show_option1_menu))
    btn_nhan_vien.pack(pady=5)
    
    btn_quan_ly = tk.Button(main_frame, text="Quản lý", command=lambda: ql_danh_muc_ng_quan_ly.show_quan_ly_form(window, current_user, current_user_role, show_option1_menu))
    btn_quan_ly.pack(pady=5)
    
    btn_khach_hang = tk.Button(main_frame, text="Khách hàng", command=lambda: ql_danh_muc_khach_hang.show_khach_hang_form(window, current_user, current_user_role, show_option1_menu))
    btn_khach_hang.pack(pady=5)
    
    btn_san_pham = tk.Button(main_frame, text="Sản phẩm", command=lambda: ql_danh_muc_san_pham.show_san_pham_form(window, current_user, current_user_role, show_option1_menu))
    btn_san_pham.pack(pady=5)
    
    btn_back = tk.Button(main_frame, text="Quay lại", command=lambda: show_main_menu(window, current_user, current_user_role))
    btn_back.pack(pady=10)

# Submenu Quản lý quy trình đặt hàng
def show_option2_menu(window, current_user, current_user_role):
    for widget in window.winfo_children():
        widget.destroy()
    
    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    label_title = tk.Label(main_frame, text="Quản lý quy trình đặt hàng", font=("Arial", 14))
    label_title.pack(pady=10)
    
    btn_tao_don_hang_moi = tk.Button(main_frame, text="Tạo đơn hàng mới", command=lambda: ql_don_hang.show_tao_don_hang_form(window, current_user, current_user_role, show_option2_menu))
    btn_tao_don_hang_moi.pack(pady=5)
    
    btn_cap_nhat_don_hang = tk.Button(main_frame, text="Cập nhật đơn hàng", command=lambda: messagebox.showinfo("Cập nhật đơn hàng", "Chức năng: Chỉnh sửa đơn hàng"))
    btn_cap_nhat_don_hang.pack(pady=5)
    
    btn_ghi_nhan_thanh_toan = tk.Button(main_frame, text="Ghi nhận thanh toán", command=lambda: messagebox.showinfo("Ghi nhận thanh toán", "Chức năng: Ghi nhận thanh toán"))
    btn_ghi_nhan_thanh_toan.pack(pady=5)
    
    btn_tra_cuu_don_hang = tk.Button(main_frame, text="Tra cứu đơn hàng", command=lambda: ql_don_hang.show_tra_cuu_don_hang_form(window, current_user, current_user_role, show_option2_menu))
    btn_tra_cuu_don_hang.pack(pady=5)
    
    btn_back = tk.Button(main_frame, text="Quay lại", command=lambda: show_main_menu(window, current_user, current_user_role))
    btn_back.pack(pady=10)

# Submenu Quản lý nhập hàng
def show_option3_menu(window, current_user, current_user_role):
    for widget in window.winfo_children():
        widget.destroy()
    
    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    label_title = tk.Label(main_frame, text="Quản lý nhập hàng", font=("Arial", 14))
    label_title.pack(pady=10)
    
    btn_tra_cuu_ton_kho = tk.Button(main_frame, text="Tra cứu số lượng hàng tồn kho", command=lambda: messagebox.showinfo("Tra cứu số lượng tồn kho", "Chức năng: Tra cứu số lượng hàng tồn kho"))
    btn_tra_cuu_ton_kho.pack(pady=5)
    
    btn_ql_nhap_kho = tk.Button(main_frame, text="Quản lý nhập kho", command=lambda: messagebox.showinfo("Quản lý nhập kho", "Chức năng: Quản lý nhập kho"))
    btn_ql_nhap_kho.pack(pady=5)
    
    btn_canh_bao = tk.Button(main_frame, text="Cảnh báo hàng sắp hết", command=lambda: messagebox.showinfo("Cảnh báo hàng sắp hết", "Chức năng: Cảnh báo hàng sắp hết"))
    btn_canh_bao.pack(pady=5)
    
    btn_back = tk.Button(main_frame, text="Quay lại", command=lambda: show_main_menu(window, current_user, current_user_role))
    btn_back.pack(pady=10)

# Submenu Báo cáo & thống kê
def show_option4_menu(window, current_user, current_user_role):
    for widget in window.winfo_children():
        widget.destroy()
    
    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    label_title = tk.Label(main_frame, text="Báo cáo & thống kê", font=("Arial", 14))
    label_title.pack(pady=10)
    
    btn_doanh_thu = tk.Button(main_frame, text="Báo cáo doanh thu", command=lambda: messagebox.showinfo("Báo cáo doanh thu", "Chức năng: Báo cáo doanh thu"))
    btn_doanh_thu.pack(pady=5)
    
    btn_chi_phi_nhap_hang = tk.Button(main_frame, text="Báo cáo chi phí nhập hàng", command=lambda: messagebox.showinfo("Báo cáo chi phí nhập hàng", "Chức năng: Báo cáo chi phí nhập hàng"))
    btn_chi_phi_nhap_hang.pack(pady=5)
    
    btn_bc_khach_hang = tk.Button(main_frame, text="Báo cáo khách hàng", command=lambda: messagebox.showinfo("Báo cáo khách hàng", "Chức năng: Báo cáo khách hàng"))
    btn_bc_khach_hang.pack(pady=5)
    
    btn_back = tk.Button(main_frame, text="Quay lại", command=lambda: show_main_menu(window, current_user, current_user_role))
    btn_back.pack(pady=10)

# Các hàm điều hướng
def ql_danh_muc(window, current_user, current_user_role):
    show_option1_menu(window, current_user, current_user_role)

def ql_quy_trinh_dat_hang(window, current_user, current_user_role):
    show_option2_menu(window, current_user, current_user_role)

def ql_nhap_hang(window, current_user, current_user_role):
    show_option3_menu(window, current_user, current_user_role)

def bao_cao(window, current_user, current_user_role):
    show_option4_menu(window, current_user, current_user_role)

def thoat_app(window):
    window.destroy()

def ql_ho_so(window):
    messagebox.showinfo("Quản lý hồ sơ", "Chức năng: Quản lý hồ sơ nhân viên")

def doi_mat_khau(window):
    messagebox.showinfo("Đổi mật khẩu", "Chức năng: Đổi mật khẩu")

# Chạy chương trình
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Online Sales Management System")
    window.state("zoomed")  # Mở toàn màn hình
    show_main_menu(window, "abc", "Quản lý")
    window.mainloop()