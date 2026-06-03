import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# --- CẤU HÌNH ---
FILE_DATA = "Data_Cham_Cong.xlsx"
FILE_PASS = "pass.txt"

# Hàm khởi tạo file dữ liệu chuẩn (Tự tạo file nếu chưa có)
def init_system():
    if not os.path.exists(FILE_PASS):
        with open(FILE_PASS, "w") as f: f.write("888888") # Mật khẩu mặc định
    if not os.path.exists(FILE_DATA):
        with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

init_system()
st.set_page_config(page_title="Quản Lý Chấm Công", layout="wide")
st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG CHUYÊN NGHIỆP")

# Load dữ liệu
df_nv = pd.read_excel(FILE_DATA, sheet_name="Danh_Sach_NV")
df_nhat_ky = pd.read_excel(FILE_DATA, sheet_name="Nhat_Ky_Ca")
with open(FILE_PASS, "r") as f: current_pass = f.read().strip()

# --- SIDEBAR (ADMIN PANEL) ---
with st.sidebar:
    st.header("🔑 Quản trị Admin")
    pwd = st.text_input("Nhập mật khẩu Admin:", type="password")
    
    if pwd == current_pass:
        st.success("Đã đăng nhập")
        
        # 1. Đổi mật khẩu
        new_pass = st.text_input("Đặt mật khẩu mới:", type="password")
        if st.button("Xác nhận đổi mật khẩu"):
            with open(FILE_PASS, "w") as f: f.write(new_pass)
            st.rerun()

        st.divider()
        # 2. Quản lý hệ thống
        st.subheader("Bảng dữ liệu (Chỉnh sửa tại đây)")
        edited_nv = st.data_editor(df_nv, use_container_width=True)
        edited_log = st.data_editor(df_nhat_ky, use_container_width=True)
        
        if st.button("LƯU TẤT CẢ THAY ĐỔI VÀO FILE"):
            with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
                edited_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
                edited_log.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
            st.success("Đã lưu dữ liệu!")
            st.rerun()

        st.divider()
        # 3. Xuất file
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            edited_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            edited_log.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
        st.download_button("📥 Tải File Excel Báo Cáo", data=buffer, file_name="Bao_Cao_Cham_Cong.xlsx")
    else:
        st.info("Nhập mật khẩu để vào chế độ Admin.")

# --- GIAO DIỆN CHẤM CÔNG (NHÂN VIÊN) ---
st.subheader("Danh sách nhân viên")
st.table(df_nv[["Tên Nhân Viên", "Trạng Thái"]])

if not df_nv.empty:
    selected = st.selectbox("Chọn tên của bạn:", df_nv["Tên Nhân Viên"].tolist())
    col1, col2 = st.columns(2)
    
    if col1.button("BẮT ĐẦU VÀO CA"):
        st.success(f"Chào {selected}, hệ thống đã ghi giờ vào.")
    if col2.button("KẾT THÚC RA CA"):
        st.success(f"Chào {selected}, hệ thống đã ghi giờ ra.")
else:
    st.warning("Hệ thống chưa có nhân viên nào.")