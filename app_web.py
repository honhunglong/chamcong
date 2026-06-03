import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CẤU HÌNH ---
FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"
FILE_PASS = "pass.txt"

# Khởi tạo dữ liệu nếu chưa có
if not os.path.exists(FILE_PASS):
    with open(FILE_PASS, "w") as f: f.write("888888")
if not os.path.exists(FILE_CHAM_CONG):
    with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
        pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
        pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

st.set_page_config(page_title="Hệ thống Chấm công", layout="wide")
st.title("🕒 HỆ THỐNG QUẢN LÝ")

# --- ADMIN PANEL ---
with st.sidebar:
    st.header("🔑 Admin")
    with open(FILE_PASS, "r") as f: current_pass = f.read().strip()
    pwd = st.text_input("Mật khẩu:", type="password")
    
    if pwd == current_pass:
        st.success("Đã đăng nhập")
        df_nv = pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV")
        df_nhat_ky = pd.read_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca")
        
        st.subheader("Chỉnh sửa nhật ký")
        # Dùng st.data_editor để sửa trực tiếp
        edited_df = st.data_editor(df_nhat_ky, num_rows="dynamic")
        
        if st.button("Lưu thay đổi vào Excel"):
            # Cách lưu an toàn: tạo writer mới và ghi đè
            with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
                df_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
                edited_df.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
            st.success("Đã lưu thành công!")
            st.rerun()
    else:
        st.info("Nhập mật khẩu Admin.")

# --- NHÂN VIÊN PANEL ---
df_nv = pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV")
st.subheader("Danh sách nhân viên")
st.table(df_nv[["Tên Nhân Viên", "Trạng Thái"]])

selected = st.selectbox("Chọn tên:", df_nv["Tên Nhân Viên"].tolist())
if st.button("BẮT ĐẦU VÀO CA"):
    st.info(f"Đã ghi nhận vào ca lúc {datetime.now().strftime('%H:%M:%S')}")
if st.button("KẾT THÚC RA CA"):
    st.info("Đã ghi nhận ra ca.")