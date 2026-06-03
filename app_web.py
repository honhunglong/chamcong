import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

FILE_DATA = "Data_Cham_Cong.xlsx"
FILE_PASS = "pass.txt"

def init_system():
    if not os.path.exists(FILE_PASS): with open(FILE_PASS, "w") as f: f.write("888888")
    if not os.path.exists(FILE_DATA):
        with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

init_system()
st.set_page_config(page_title="Quản Lý Chấm Công", layout="wide")
st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG")

df_nv = pd.read_excel(FILE_DATA, sheet_name="Danh_Sach_NV")
df_nhat_ky = pd.read_excel(FILE_DATA, sheet_name="Nhat_Ky_Ca")
with open(FILE_PASS, "r") as f: current_pass = f.read().strip()

with st.sidebar:
    st.header("🔑 Quản trị Admin")
    pwd = st.text_input("Nhập mật khẩu:", type="password")
    
    if pwd == current_pass:
        st.success("Đã đăng nhập")
        # 1. Thêm nhân viên
        st.subheader("Thêm nhân viên mới")
        new_name = st.text_input("Tên:")
        new_luong = st.number_input("Lương/giờ:", value=20000)
        if st.button("Thêm nhân viên"):
            df_nv = pd.concat([df_nv, pd.DataFrame([{"Tên Nhân Viên": new_name, "Mức Lương / Giờ": new_luong, "Trạng Thái": "Ngoài"}])], ignore_index=True)
            df_nv.to_excel(FILE_DATA, sheet_name="Danh_Sach_NV", index=False, mode='a', if_sheet_exists='replace')
            st.rerun()

        st.divider()
        # 2. Chỉnh sửa tất cả trong 1 bảng
        st.subheader("Chỉnh sửa dữ liệu")
        edited_nv = st.data_editor(df_nv, use_container_width=True)
        edited_log = st.data_editor(df_nhat_ky, use_container_width=True)
        
        if st.button("LƯU TẤT CẢ THAY ĐỔI"):
            with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
                edited_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
                edited_log.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
            st.rerun()

        # 3. Xuất file
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            edited_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            edited_log.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
        st.download_button("📥 Tải Báo Cáo Excel", data=buffer, file_name="Bao_Cao.xlsx")
    else:
        st.info("Nhập mật khẩu để quản lý.")

# --- GIAO DIỆN CHẤM CÔNG ---
if not df_nv.empty:
    selected = st.selectbox("Chọn tên của bạn:", df_nv["Tên Nhân Viên"].tolist())
    col1, col2 = st.columns(2)
    if col1.button("BẮT ĐẦU VÀO CA"): st.success(f"Đã ghi vào cho {selected}")
    if col2.button("KẾT THÚC RA CA"): st.success(f"Đã ghi ra cho {selected}")
else:
    st.warning("Chưa có nhân viên.")