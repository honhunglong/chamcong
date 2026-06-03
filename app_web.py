import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

FILE_DATA = "Data_Cham_Cong.xlsx"
FILE_PASS = "pass.txt"

# Hàm khởi tạo hệ thống
def init_system():
    if not os.path.exists(FILE_PASS):
        with open(FILE_PASS, "w") as f:
            f.write("888888")
    if not os.path.exists(FILE_DATA):
        with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

init_system()
st.set_page_config(page_title="Hệ thống Quản lý", layout="wide")
st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG")

# Load dữ liệu
df_nv = pd.read_excel(FILE_DATA, sheet_name="Danh_Sach_NV")
df_nhat_ky = pd.read_excel(FILE_DATA, sheet_name="Nhat_Ky_Ca")
with open(FILE_PASS, "r") as f:
    current_pass = f.read().strip()

# --- SIDEBAR ADMIN ---
with st.sidebar:
    st.header("🔑 Admin")
    pwd = st.text_input("Mật khẩu:", type="password")
    
    if pwd == current_pass:
        st.success("Đã đăng nhập")
        
        # Thêm nhân viên
        st.subheader("Nhân viên")
        new_name = st.text_input("Tên NV:")
        if st.button("Thêm"):
            df_nv = pd.concat([df_nv, pd.DataFrame([{"Tên Nhân Viên": new_name, "Mức Lương / Giờ": 20000, "Trạng Thái": "Ngoài"}])], ignore_index=True)
            df_nv.to_excel(FILE_DATA, sheet_name="Danh_Sach_NV", index=False, mode='a', if_sheet_exists='replace')
            st.rerun()
            
        # Chỉnh sửa dữ liệu
        st.subheader("Chỉnh sửa dữ liệu")
        edited_nv = st.data_editor(df_nv)
        edited_log = st.data_editor(df_nhat_ky)
        
        if st.button("LƯU TẤT CẢ"):
            with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
                edited_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
                edited_log.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
            st.success("Đã lưu!")
            st.rerun()
    else:
        st.info("Nhập mật khẩu Admin.")

# --- NHÂN VIÊN ---
if not df_nv.empty:
    selected = st.selectbox("Chọn tên:", df_nv["Tên Nhân Viên"].tolist())
    if st.button("BẮT ĐẦU VÀO CA"): st.success(f"Đã ghi vào: {selected}")
    if st.button("KẾT THÚC RA CA"): st.success(f"Đã ghi ra: {selected}")