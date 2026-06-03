import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# --- CẤU HÌNH ---
FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"
FILE_PASS = "pass.txt"

# Hàm khởi tạo file dữ liệu
def init_data():
    if not os.path.exists(FILE_PASS):
        with open(FILE_PASS, "w") as f: f.write("888888")
    if not os.path.exists(FILE_CHAM_CONG):
        with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

init_data()
st.set_page_config(page_title="Hệ thống Chấm công", layout="wide")
st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG")

# Load dữ liệu
df_nv = pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV")
df_nhat_ky = pd.read_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca")
with open(FILE_PASS, "r") as f: current_pass = f.read().strip()

# --- SIDEBAR ADMIN ---
with st.sidebar:
    st.header("🔑 Admin")
    pwd = st.text_input("Mật khẩu:", type="password")
    
    if pwd == current_pass:
        st.success("Đã đăng nhập")
        
        # 1. ĐỔI MẬT KHẨU
        st.subheader("Bảo mật")
        new_pass = st.text_input("Mật khẩu mới:", type="password")
        if st.button("Xác nhận đổi mật khẩu"):
            with open(FILE_PASS, "w") as f: f.write(new_pass)
            st.rerun()
            
        # 2. QUẢN LÝ NHÂN VIÊN
        st.subheader("Nhân viên")
        new_n = st.text_input("Thêm tên NV:")
        if st.button("Thêm NV"):
            df_nv = pd.concat([df_nv, pd.DataFrame([{"Tên Nhân Viên": new_n, "Mức Lương / Giờ": 20000, "Trạng Thái": "Ngoài"}])], ignore_index=True)
            df_nv.to_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV", index=False, mode='a', if_sheet_exists='replace')
            st.rerun()

        # 3. CHỈNH SỬA NHẬT KÝ
        st.subheader("Chỉnh sửa nhật ký")
        edited_df = st.data_editor(df_nhat_ky, use_container_width=True)
        if st.button("Lưu thay đổi"):
            with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
                df_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
                edited_df.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
            st.success("Đã lưu!")
            st.rerun()
            
        # 4. TẢI EXCEL
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            edited_df.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
        st.download_button("📥 Tải file Excel", data=buffer, file_name="Bao_Cao.xlsx")
    else:
        st.info("Nhập mật khẩu Admin.")

# --- GIAO DIỆN CHẤM CÔNG ---
if not df_nv.empty:
    selected = st.selectbox("Chọn tên nhân viên:", df_nv["Tên Nhân Viên"].tolist())
    col1, col2 = st.columns(2)
    if col1.button("BẮT ĐẦU VÀO CA"):
        st.info(f"Đã ghi vào lúc: {datetime.now().strftime('%H:%M:%S')}")
    if col2.button("KẾT THÚC RA CA"):
        st.info("Đã ghi ra ca.")
else:
    st.warning("Admin chưa thêm nhân viên!")