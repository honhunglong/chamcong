import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

FILE_DATA = "Data_Cham_Cong.xlsx"
FILE_PASS = "pass.txt"

# 1. Khởi tạo hệ thống
def init_system():
    if not os.path.exists(FILE_PASS):
        with open(FILE_PASS, "w") as f: f.write("888888")
    if not os.path.exists(FILE_DATA):
        with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

init_system()
st.set_page_config(layout="wide")
st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG & LƯƠNG")

# 2. Đọc dữ liệu
df_nv = pd.read_excel(FILE_DATA, sheet_name="Danh_Sach_NV")
df_nhat_ky = pd.read_excel(FILE_DATA, sheet_name="Nhat_Ky_Ca")
with open(FILE_PASS, "r") as f: current_pass = f.read().strip()

# 3. SIDEBAR ADMIN (Gộp chung để không bị dư bảng)
with st.sidebar:
    st.header("🔑 Quản trị Admin")
    pwd = st.text_input("Mật khẩu:", type="password")
    if pwd == current_pass:
        st.success("Đã đăng nhập Admin")
        
        # Thêm nhân viên
        st.subheader("Thêm NV")
        ten_moi = st.text_input("Tên:")
        luong_moi = st.number_input("Lương/giờ:", value=20000)
        if st.button("Thêm nhân viên"):
            df_nv = pd.concat([df_nv, pd.DataFrame([{"Tên Nhân Viên": ten_moi, "Mức Lương / Giờ": luong_moi, "Trạng Thái": "Ngoài"}])], ignore_index=True)
            with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
                df_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
                df_nhat_ky.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
            st.rerun()

        # Chỉnh sửa dữ liệu
        st.subheader("Chỉnh sửa dữ liệu")
        edited_nv = st.data_editor(df_nv, use_container_width=True)
        edited_log = st.data_editor(df_nhat_ky, use_container_width=True)
        
        if st.button("LƯU TẤT CẢ THAY ĐỔI"):
            with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
                edited_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
                edited_log.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
            st.success("Đã lưu!")
            st.rerun()
            
        # Xuất file
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            edited_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            edited_log.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
        st.download_button("📥 Tải File Excel Báo Cáo", data=buffer, file_name="Bao_Cao.xlsx")

# 4. GIAO DIỆN NHÂN VIÊN
if not df_nv.empty:
    selected = st.selectbox("Chọn tên của bạn:", df_nv["Tên Nhân Viên"].tolist())
    c1, c2 = st.columns(2)
    if c1.button("BẮT ĐẦU VÀO CA"): st.info(f"Đã ghi vào cho {selected}")
    if c2.button("KẾT THÚC RA CA"): st.info(f"Đã ghi ra cho {selected}")
else:
    st.warning("Admin chưa thêm nhân viên.")