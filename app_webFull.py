import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

FILE_DATA = "Data_Cham_Cong.xlsx"

# --- KHỞI TẠO DỮ LIỆU ---
def init_data():
    if not os.path.exists(FILE_DATA):
        with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Tên NV", "Lương/Giờ"]).to_excel(writer, sheet_name="NV", index=False)
            pd.DataFrame(columns=["Ngày", "Tên NV", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Tiền"]).to_excel(writer, sheet_name="Ky", index=False)
            # Lưu mật khẩu mặc định vào file ẩn hoặc biến môi trường (đơn giản hóa dùng biến session)
    if "admin_pass" not in st.session_state: st.session_state.admin_pass = "888888"

init_data()

# --- GIAO DIỆN CHÍNH ---
st.set_page_config(page_title="Hệ Thống Chấm Công", layout="wide")
st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG")

# 1. GIAO DIỆN ADMIN (BÊN PHẢI)
with st.sidebar:
    st.header("🔑 Cấu hình Admin")
    password = st.text_input("Nhập mật khẩu Admin:", type="password")
    
    if password == st.session_state.admin_pass:
        st.success("Đã đăng nhập Admin")
        # Đổi mật khẩu
        new_pass = st.text_input("Đổi mật khẩu mới:", type="password")
        if st.button("Cập nhật mật khẩu"):
            st.session_state.admin_pass = new_pass
            st.info("Mật khẩu đã đổi!")
            
        st.divider()
        st.subheader("Quản lý Nhân viên")
        df_nv = pd.read_excel(FILE_DATA, sheet_name="NV")
        ten_moi = st.text_input("Tên NV mới:")
        luong_moi = st.number_input("Lương/Giờ:", value=20000)
        
        if st.button("Thêm NV"):
            new_row = pd.DataFrame([{"Tên NV": ten_moi, "Lương/Giờ": luong_moi}])
            pd.concat([df_nv, new_row]).to_excel(FILE_DATA, sheet_name="NV", index=False)
            st.rerun()

# 2. GIAO DIỆN NHÂN VIÊN (CHÍNH)
df_nv = pd.read_excel(FILE_DATA, sheet_name="NV")
df_ky = pd.read_excel(FILE_DATA, sheet_name="Ky")

if not df_nv.empty:
    ten_chon = st.selectbox("Chọn tên của bạn:", df_nv["Tên NV"].tolist())
    
    c1, c2 = st.columns(2)
    if c1.button("VÀO CA"):
        now = datetime.now()
        new_row = pd.DataFrame([{"Ngày": now.strftime("%Y-%m-%d"), "Tên NV": ten_chon, "Giờ Vào": now.strftime("%H:%M:%S"), "Giờ Ra": "", "Tổng Giờ": 0, "Tiền": 0}])
        pd.concat([df_ky, new_row]).to_excel(FILE_DATA, sheet_name="Ky", index=False)
        st.success("Đã ghi VÀO CA!")
        st.rerun()

    if c2.button("RA CA"):
        mask = (df_ky["Tên NV"] == ten_chon) & (df_ky["Giờ Ra"] == "")
        if mask.any():
            idx = df_ky[mask].index[-1]
            gio_vao = datetime.strptime(df_ky.loc[idx, "Giờ Vào"], "%H:%M:%S")
            now = datetime.now()
            tong_gio = (now - gio_vao).total_seconds() / 3600
            luong_gio = df_nv.loc[df_nv["Tên NV"] == ten_chon, "Lương/Giờ"].values[0]
            
            df_ky.loc[idx, "Giờ Ra"] = now.strftime("%H:%M:%S")
            df_ky.loc[idx, "Tổng Giờ"] = round(tong_gio, 2)
            df_ky.loc[idx, "Tiền"] = round(tong_gio * luong_gio, 0)
            df_ky.to_excel(FILE_DATA, sheet_name="Ky", index=False)
            st.success(f"Đã RA CA. Tổng thời gian: {round(tong_gio, 2)} giờ.")
            st.rerun()

# 3. BÁO CÁO ADMIN (CHỈ XUẤT HIỆN KHI ĐĂNG NHẬP PASS)
if password == st.session_state.admin_pass:
    st.divider()
    st.subheader("📊 Bảng Lương Tổng Hợp")
    df_tong = df_ky.groupby("Tên NV").agg({"Tổng Giờ": "sum", "Tiền": "sum"}).reset_index()
    st.dataframe(df_tong)
    
    # Xuất Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_tong.to_excel(writer, index=False, sheet_name="Bang_Luong")
    st.download_button("📥 Tải Bảng Lương Excel", data=output.getvalue(), file_name="Bang_Luong.xlsx")