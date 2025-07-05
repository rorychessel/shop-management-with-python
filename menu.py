import tkinter as tk
from tkinter import ttk, messagebox

import ql_danh_muc_nhan_vien
import ql_danh_muc_ng_quan_ly
import ql_danh_muc_khach_hang
import ql_danh_muc_san_pham
import ql_don_hang
import ql_phieu_nhap_hang
import ql_bao_cao
import ql_ho_so_ca_nhan
import doi_mk

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
        
        btn_ho_so = tk.Button(main_frame, text="Quản lý hồ sơ", command=lambda: ql_ho_so_ca_nhan.show_ho_so_ca_nhan(window, current_user, current_user_role, show_main_menu))
        btn_ho_so.pack(pady=5)

        btn_doi_mk = tk.Button(main_frame, text="Đổi mật khẩu", command=lambda: doi_mk.show_doi_mat_khau(window, current_user, current_user_role, show_main_menu))
        btn_doi_mk.pack(pady=5)
    
        btn_dang_xuat = tk.Button(main_frame, text="Đăng xuất", command=lambda: thoat_app(window))
        btn_dang_xuat.pack(pady=10)

    if current_user_role.strip().lower() == "nhân viên":
        btn_danh_muc = tk.Button(main_frame, text="Quản lý danh mục", command=lambda: ql_danh_muc2(window, current_user, current_user_role))
        btn_danh_muc.pack(pady=5)
        
        btn_dat_hang = tk.Button(main_frame, text="Quản lý quy trình đặt hàng", command=lambda: ql_quy_trinh_dat_hang(window, current_user, current_user_role))
        btn_dat_hang.pack(pady=5)
        
        btn_nhap_hang = tk.Button(main_frame, text="Quản lý nhập hàng", command=lambda: ql_nhap_hang(window, current_user, current_user_role))
        btn_nhap_hang.pack(pady=5)
        
        btn_bao_cao = tk.Button(main_frame, text="Báo cáo & thống kê", command=lambda: bao_cao(window, current_user, current_user_role))
        btn_bao_cao.pack(pady=5)
        
        btn_ho_so = tk.Button(main_frame, text="Hồ sơ cá nhân", command=lambda: ql_ho_so_ca_nhan.show_ho_so_ca_nhan(window, current_user, current_user_role, show_main_menu))
        btn_ho_so.pack(pady=5)
    
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

# Submenu Quản lý danh mục 2
def show_option11_menu(window, current_user, current_user_role):
    for widget in window.winfo_children():
        widget.destroy()
    
    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    label_title = tk.Label(main_frame, text="Quản lý danh mục", font=("Arial", 14))
    label_title.pack(pady=10)
    
    btn_nv = tk.Button(main_frame, text="Xem danh sách nhân viên", command=lambda: ql_danh_muc_nhan_vien.xem_danh_sach_nhan_vien(window, current_user, current_user_role, show_option11_menu))
    btn_nv.pack(pady=5)
    
    btn_ql = tk.Button(main_frame, text="Xem danh sách quản lý", command=lambda: ql_danh_muc_ng_quan_ly.xem_danh_sach_quan_ly(window, current_user, current_user_role, show_option11_menu))
    btn_ql.pack(pady=5)

    btn_kh = tk.Button(main_frame, text="Khách hàng", command=lambda: ql_danh_muc_khach_hang.show_khach_hang_form(window, current_user, current_user_role, show_option11_menu))
    btn_kh.pack(pady=5)
    
    btn_sp = tk.Button(main_frame, text="Xem danh sách sản phẩm", command=lambda: ql_danh_muc_san_pham.xem_danh_sach_san_pham(window, current_user, current_user_role, show_option11_menu))
    btn_sp.pack(pady=5)
    
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
    
    btn_cap_nhat_don_hang = tk.Button(main_frame, text="Cập nhật đơn hàng", command=lambda: ql_don_hang.show_cap_nhat_don_hang_form(window, current_user, current_user_role, show_option2_menu))
    btn_cap_nhat_don_hang.pack(pady=5)
    
    btn_ghi_nhan_thanh_toan = tk.Button(main_frame, text="Ghi nhận thanh toán", command=lambda: ql_don_hang.show_ghi_nhan_thanh_toan_form(window, current_user, current_user_role, show_option2_menu))
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
    
    btn_tra_cuu_ton_kho = tk.Button(main_frame, text="Tra cứu số lượng hàng tồn kho", command=lambda: ql_phieu_nhap_hang.show_tra_cuu_ton_kho_form(window, current_user, current_user_role, show_option3_menu))
    btn_tra_cuu_ton_kho.pack(pady=5)
    
    btn_them_phieu_nhap = tk.Button(main_frame, text="Thêm phiếu nhập", command=lambda: ql_phieu_nhap_hang.show_them_phieu_nhap_form(window, current_user, current_user_role, show_option3_menu))
    btn_them_phieu_nhap.pack(pady=5)

    btn_sua_phieu_nhap = tk.Button(main_frame, text="Sửa phiếu nhập", command=lambda: ql_phieu_nhap_hang.show_sua_phieu_nhap_form(window, current_user, current_user_role, show_option3_menu))
    btn_sua_phieu_nhap.pack(pady=5)

    btn_xoa_phieu_nhap = tk.Button(main_frame, text="Xóa phiếu nhập", command=lambda: ql_phieu_nhap_hang.show_xoa_phieu_nhap_form(window, current_user, current_user_role, show_option3_menu))
    btn_xoa_phieu_nhap.pack(pady=5)

    btn_tra_cuu_phieu_nhap = tk.Button(main_frame, text="Tra cứu phiếu nhập", command=lambda: ql_phieu_nhap_hang.show_tra_cuu_phieu_nhap_form(window, current_user, current_user_role, show_option3_menu))
    btn_tra_cuu_phieu_nhap.pack(pady=5)
    
    btn_canh_bao = tk.Button(main_frame, text="Cảnh báo hàng sắp hết", command=lambda: ql_phieu_nhap_hang.show_canh_bao_hang_sap_het_form(window, current_user, current_user_role, show_option3_menu))
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
    
    btn_doanh_thu = tk.Button(main_frame, text="Báo cáo doanh thu", command=lambda: ql_bao_cao.show_bao_cao_doanh_thu(window, current_user, current_user_role, show_option4_menu))
    btn_doanh_thu.pack(pady=5)
    
    btn_chi_phi_nhap_hang = tk.Button(main_frame, text="Báo cáo chi phí nhập hàng", command=lambda: ql_bao_cao.show_bao_cao_chi_phi_nhap_hang(window, current_user, current_user_role, show_option4_menu))
    btn_chi_phi_nhap_hang.pack(pady=5)
    
    btn_bc_khach_hang = tk.Button(main_frame, text="Báo cáo khách hàng", command=lambda: ql_bao_cao.show_bao_cao_khach_hang(window, current_user, current_user_role, show_option4_menu))
    btn_bc_khach_hang.pack(pady=5)
    
    btn_back = tk.Button(main_frame, text="Quay lại", command=lambda: show_main_menu(window, current_user, current_user_role))
    btn_back.pack(pady=10)

# Các hàm điều hướng
def ql_danh_muc(window, current_user, current_user_role):
    show_option1_menu(window, current_user, current_user_role)

def ql_danh_muc2(window, current_user, current_user_role):
    show_option11_menu(window, current_user, current_user_role)

def ql_quy_trinh_dat_hang(window, current_user, current_user_role):
    show_option2_menu(window, current_user, current_user_role)

def ql_nhap_hang(window, current_user, current_user_role):
    show_option3_menu(window, current_user, current_user_role)

def bao_cao(window, current_user, current_user_role):
    show_option4_menu(window, current_user, current_user_role)

def thoat_app(window):
    window.destroy()

# Chạy chương trình
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Online Sales Management System")
    window.state("zoomed")  # Mở toàn màn hình
    show_main_menu(window, "abc", "Quản lý")
    window.mainloop()