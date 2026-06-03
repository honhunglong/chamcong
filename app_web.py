import os
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import customtkinter as ctk

# Thiết lập giao diện hiện đại
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("green") 

FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"

# Tự động tạo file dữ liệu cấu trúc Excel nếu chưa có
if not os.path.exists(FILE_CHAM_CONG):
    df_nv = pd.DataFrame([
        {"Tên Nhân Viên": "Nguyễn Văn A", "Mức Lương / Giờ": 20000, "Trạng Thái": "Đang ở ngoài"},
        {"Tên Nhân Viên": "Trần Thị B", "Mức Lương / Giờ": 25000, "Trạng Thái": "Đang ở ngoài"},
    ])
    df_nhat_ky = pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ Lập Trình", "Mức Lương Lúc Đó", "Thành Tiền"])
    with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
        df_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
        df_nhat_ky.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

class AppChamCong(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("HỆ THỐNG CHẤM CÔNG & TÍNH LƯƠNG TỰ ĐỘNG")
        self.geometry("900x600")
        
        # Tiêu đề chính
        ctk.CTkLabel(self, text="MÀN HÌNH CHẤM CÔNG NHÂN VIÊN CA LÀM", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)
        
        # --- KHU VỰC 1: CHẤM CÔNG HÀNG NGÀY (CHO NHÂN VIÊN) ---
        self.worker_frame = ctk.CTkFrame(self)
        self.worker_frame.pack(pady=10, fill="x", padx=20)
        
        ctk.CTkLabel(self.worker_frame, text="--- DÀNH CHO NHÂN VIÊN ĐỨNG CA ---", font=ctk.CTkFont(weight="bold", size=14), text_color="#2ecc71").grid(row=0, column=0, columnspan=3, padx=15, pady=8, sticky="w")
        
        ctk.CTkLabel(self.worker_frame, text="Chọn tên của bạn:").grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.combo_nv = ctk.CTkComboBox(self.worker_frame, width=200, values=[])
        self.combo_nv.grid(row=1, column=1, padx=15, pady=10, sticky="w")
        
        self.btn_vao_ca = ctk.CTkButton(self.worker_frame, text="BẮT ĐẦU VÀO CA", fg_color="#2ecc71", hover_color="#27ae60", command=self.vao_ca)
        self.btn_vao_ca.grid(row=2, column=0, padx=15, pady=15, sticky="we")
        
        self.btn_ra_ca = ctk.CTkButton(self.worker_frame, text="KẾT THÚC RA CA", fg_color="#e74c3c", hover_color="#c0392b", command=self.ra_ca)
        self.btn_ra_ca.grid(row=2, column=1, padx=15, pady=15, sticky="we")
        
        # --- KHU VỰC 2: QUẢN LÝ & TÍNH LƯƠNG CUỐI THÁNG (CHO CHỦ) ---
        self.admin_frame = ctk.CTkFrame(self)
        self.admin_frame.pack(pady=10, fill="both", expand=True, padx=20)
        
        ctk.CTkLabel(self.admin_frame, text="--- QUẢN LÝ LƯƠNG & XUẤT BÁO CÁO CUỐI THÁNG (ADMIN) ---", font=ctk.CTkFont(weight="bold", size=14), text_color="#3498db").grid(row=0, column=0, columnspan=4, padx=15, pady=8, sticky="w")
        
        # Thêm/Sửa mức lương nhân viên
        ctk.CTkLabel(self.admin_frame, text="Tên NV mới/ NV đổi lương:").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        self.entry_ten_nv = ctk.CTkEntry(self.admin_frame, width=150, placeholder_text="Nguyễn Văn A")
        self.entry_ten_nv.grid(row=1, column=1, padx=15, pady=5, sticky="w")
        
        ctk.CTkLabel(self.admin_frame, text="Mức lương/Giờ (đ):").grid(row=1, column=2, padx=15, pady=5, sticky="w")
        self.entry_muc_luong = ctk.CTkEntry(self.admin_frame, width=120, placeholder_text="20000, 25000...")
        self.entry_muc_luong.grid(row=1, column=3, padx=15, pady=5, sticky="w")
        
        self.btn_save_nv = ctk.CTkButton(self.admin_frame, text="CẬP NHẬT MỨC LƯƠNG/NV", fg_color="#3498db", hover_color="#2980b9", command=self.cap_nhat_nhan_vien)
        self.btn_save_nv.grid(row=2, column=0, columnspan=2, padx=15, pady=10, sticky="we")
        
        # Bộ lọc tính lương cuối tháng
        ctk.CTkLabel(self.admin_frame, text="Nhập Tháng cần tính lương:").grid(row=3, column=0, padx=15, pady=5, sticky="w")
        self.entry_thang = ctk.CTkEntry(self.admin_frame, width=100, placeholder_text="Tháng (01-12)")
        self.entry_thang.grid(row=3, column=1, padx=15, pady=5, sticky="w")
        self.entry_thang.insert(0, pd.Timestamp.now().strftime("%m"))
        
        self.btn_tinh_luong = ctk.CTkButton(self.admin_frame, text="TÍNH TỔNG LƯƠNG CUỐI THÁNG", fg_color="#f39c12", hover_color="#d35400", command=self.tinh_luong_cuoi_thang)
        self.btn_tinh_luong.grid(row=4, column=0, columnspan=2, padx=15, pady=10, sticky="we")
        
        # Bảng hiển thị kết quả tính lương nhanh
        self.txt_ket_qua = tk.Text(self.admin_frame, height=8, font=("Courier New", 11))
        self.txt_ket_qua.grid(row=2, column=2, rowspan=3, columnspan=2, padx=15, pady=10, sticky="nsew")
        
        self.tai_du_lieu()
        
    def tai_du_lieu(self):
        self.df_nv = pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV")
        self.df_nhat_ky = pd.read_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca")
        
        # Cập nhật danh sách nhân viên vào ô chọn (Combobox)
        danh_sach_ten = self.df_nv["Tên Nhân Viên"].tolist()
        self.combo_nv.configure(values=danh_sach_ten)
        if danh_sach_ten:
            self.combo_nv.set(danh_sach_ten[0])

    def vao_ca(self):
        ten = self.combo_nv.get()
        if not ten: return
        
        idx = self.df_nv[self.df_nv["Tên Nhân Viên"] == ten].index[0]
        trang_thai = self.df_nv.loc[idx, "Trạng Thái"]
        
        if trang_thai == "Đang làm việc":
            messagebox.showwarning("Lỗi", f"Nhân viên {ten} đã bấm vào ca trước đó rồi và chưa bấm Ra ca!")
            return
            
        bây_giờ = pd.Timestamp.now()
        
        # Tạo một dòng nhật ký mới ghi nhận giờ vào ca
        dong_moi = pd.DataFrame([{
            "Ngày": bây_giờ.strftime("%Y-%m-%d"),
            "Tên Nhân Viên": ten,
            "Giờ Vào": bây_giờ.strftime("%H:%M:%S"),
            "Giờ Ra": "",
            "Tổng Giờ Lập Trình": 0.0,
            "Mức Lương Lúc Đó": self.df_nv.loc[idx, "Mức Lương / Giờ"],
            "Thành Tiền": 0
        }])
        
        self.df_nhat_ky = pd.concat([self.df_nhat_ky, dong_moi], ignore_index=True)
        self.df_nv.loc[idx, "Trạng Thái"] = "Đang làm việc"
        
        with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
            self.df_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            self.df_nhat_ky.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
            
        messagebox.showinfo("Thành Công", f" Chào {ten}! Đã ghi nhận VÀO CA lúc {bây_giờ.strftime('%H:%M:%S')}")
        self.tai_du_lieu()

    def ra_ca(self):
        ten = self.combo_nv.get()
        if not ten: return
        
        idx_nv = self.df_nv[self.df_nv["Tên Nhân Viên"] == ten].index[0]
        if self.df_nv.loc[idx_nv, "Trạng Thái"] != "Đang làm việc":
            messagebox.showwarning("Lỗi", f"Nhân viên {ten} hiện không ở trong ca làm việc để bấm Ra ca!")
            return
            
        bây_giờ = pd.Timestamp.now()
        ngay_hom_nay = bây_giờ.strftime("%Y-%m-%d")
        
        # Tìm dòng chấm công gần nhất của nhân viên này chưa có Giờ Ra
        idx_log = self.df_nhat_ky[(self.df_nhat_ky["Tên Nhân Viên"] == ten) & (self.df_nhat_ky["Giờ Ra"].isna() | (self.df_nhat_ky["Giờ Ra"] == ""))].index[-1]
        
        gio_vao_str = self.df_nhat_ky.loc[idx_log, "Giờ Vào"]
        thoi_gian_vao = pd.to_datetime(self.df_nhat_ky.loc[idx_log, "Ngày"] + " " + gio_vao_str)
        
        # Tính toán số giờ làm việc thực tế (bao gồm cả số phút lẻ quy ra số thập phân)
        khoang_cach_tg = bây_giờ - thoi_gian_vao
        tong_so_gio = round(khoang_cach_tg.total_seconds() / 3600, 2)
        
        muc_luong = self.df_nhat_ky.loc[idx_log, "Mức Lương Lúc Đó"]
        thanh_tien = round(tong_so_gio * muc_luong)
        
        # Cập nhật vào Nhật ký
        self.df_nhat_ky.loc[idx_log, "Giờ Ra"] = bây_giờ.strftime("%H:%M:%S")
        self.df_nhat_ky.loc[idx_log, "Tổng Giờ Lập Trình"] = tong_so_gio
        self.df_nhat_ky.loc[idx_log, "Thành Tiền"] = thanh_tien
        
        # Trả trạng thái nhân viên về bình thường
        self.df_nv.loc[idx_nv, "Trạng Thái"] = "Đang ở ngoài"
        
        with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
            self.df_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            self.df_nhat_ky.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
            
        messagebox.showinfo("Thành Công", f" Đã ghi nhận RA CA cho {ten}!\nThời gian làm: {tong_so_gio} tiếng.\nThành tiền ca này: {int(thanh_tien):,}đ")
        self.tai_du_lieu()

    def cap_nhat_nhan_vien(self):
        ten = self.entry_ten_nv.get().strip()
        try:
            luong = float(self.entry_muc_luong.get().strip())
            if luong < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Mức lương phải là một con số dương hợp lệ!")
            return
            
        if not ten:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên nhân viên!")
            return
            
        if ten in self.df_nv["Tên Nhân Viên"].values:
            idx = self.df_nv[self.df_nv["Tên Nhân Viên"] == ten].index[0]
            self.df_nv.loc[idx, "Mức Lương / Giờ"] = luong
            msg = f"Đã cập nhật mức lương mới cho {ten} thành {int(luong):,}đ/giờ!"
        else:
            new_row = pd.DataFrame([{"Tên Nhân Viên": ten, "Mức Lương / Giờ": luong, "Trạng Thái": "Đang ở ngoài"}])
            self.df_nv = pd.concat([self.df_nv, new_row], ignore_index=True)
            msg = f"Đã thêm mới nhân viên {ten} với mức lương {int(luong):,}đ/giờ!"
            
        with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
            self.df_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            self.df_nhat_ky.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
            
        messagebox.showinfo("Thành Công", msg)
        self.entry_ten_nv.delete(0, tk.END)
        self.entry_muc_luong.delete(0, tk.END)
        self.tai_du_lieu()

    def tinh_luong_cuoi_thang(self):
        thang_nhap = self.entry_thang.get().strip()
        if not thang_nhap:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tháng muốn tính toán!")
            return
            
        self.df_nhat_ky["Ngày"] = pd.to_datetime(self.df_nhat_ky["Ngày"])
        # Lọc toàn bộ các ca làm việc thuộc tháng được chọn
        df_loc = self.df_nhat_ky[self.df_nhat_ky["Ngày"].dt.strftime("%m") == thang_nhap]
        
        if df_loc.empty:
            self.txt_ket_qua.delete("1.0", tk.END)
            self.txt_ket_qua.insert(tk.END, f"Không có dữ liệu chấm công nào trong tháng {thang_nhap}!")
            return
            
        # Gom nhóm theo tên nhân viên để cộng dồn Tổng Số Giờ làm và Tổng Số Tiền
        bao_cao = df_loc.groupby("Tên Nhân Viên").agg({
            "Tổng Giờ Lập Trình": "sum",
            "Thành Tiền": "sum"
        }).reset_index()
        
        # Hiển thị lên màn hình phần mềm cho chủ xem nhanh
        self.txt_ket_qua.delete("1.0", tk.END)
        self.txt_ket_qua.insert(tk.END, f"--- BẢNG LƯƠNG THÁNG {thang_nhap} ---\n")
        self.txt_ket_qua.insert(tk.END, f"{'NHÂN VIÊN':<18} | {'TỔNG GIỜ':<9} | {'TỔNG LƯƠNG (đ)':<15}\n")
        self.txt_ket_qua.insert(tk.END, "-" * 48 + "\n")
        
        for idx, row in bao_cao.iterrows():
            line = f"{row['Tên Nhân Viên']:<18} | {row['Tổng Giờ Lập Trình']:<9} | {int(row['Thành Tiền']):<15,}\n"
            self.txt_ket_qua.insert(tk.END, line)
            
        # Đồng thời tự tạo thêm 1 sheet báo cáo chi tiết trong file Excel để bạn lưu trữ hoặc in ấn
        try:
            with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                bao_cao.to_excel(writer, sheet_name=f"Luong_Thang_{thang_nhap}", index=False)
            messagebox.showinfo("Xuất Excel Thành Công", f"Đã cập nhật bảng tổng hợp lương vào Sheet [Luong_Thang_{thang_nhap}] trong file Excel!")
        except Exception as e:
            pass

if __name__ == "__main__":
    app = AppChamCong()
    app.mainloop()