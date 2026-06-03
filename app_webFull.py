import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Tên file ổn định
FILE_DATA = "Data_Cham_Cong_Final.xlsx"
FILE_PASS = "pass.txt"

# Hàm khởi tạo hoặc phục hồi dữ liệu nếu file lỗi
def get_data():
    try:
        # Nếu file tồn tại và đọc được, lấy dữ liệu
        nv = pd.read_excel(FILE_DATA, sheet_name="NV")
        ky = pd.read_excel(FILE_DATA, sheet_name="Ky")
    except:
        # Nếu file bị lỗi hoặc chưa có, tạo cấu trúc sạch
        nv = pd.DataFrame(columns=["Tên NV", "Lương/Giờ", "Trạng Thái"])
        ky = pd.DataFrame(columns=["Ngày", "Tên NV", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Tiền"])
        with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
            nv.to_excel(writer, sheet_name="NV", index=False)
            ky.to_excel(writer, sheet_name="Ky", index=False)
    return nv, ky

# Load dữ liệu vào app
df_nv, df_ky = get_data()

st.set_page_config(layout="wide")
st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG")

# --- ADMIN ---
with st.sidebar:
    st.header("🔑 Admin")
    if st.text_input("Mật khẩu:", type="password") == "888888":
        st.success("Đã đăng nhập")
        ten = st.text_input("Thêm nhân viên mới:")
        if st.button("Thêm"):
            new_nv = pd.concat([df_nv, pd.DataFrame([{"Tên NV": ten, "Lương/Giờ": 20000, "Trạng Thái": "Ngoài"}])], ignore_index=True)
            with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
                new_nv.to_excel(writer, sheet_name="NV", index=False)
                df_ky.to_excel(writer, sheet_name="Ky", index=False)
            st.rerun()
    else:
        st.info("Nhập mật khẩu Admin.")

# --- CHẤM CÔNG ---
if not df_nv.empty:
    ten_chon = st.selectbox("Chọn tên:", df_nv["Tên NV"].tolist())
    c1, c2 = st.columns(2)
    
    if c1.button("VÀO CA"):
        now = datetime.now().strftime("%H:%M:%S")
        new_row = pd.DataFrame([{"Ngày": datetime.now().strftime("%Y-%m-%d"), "Tên NV": ten_chon, "Giờ Vào": now, "Giờ Ra": "", "Tổng Giờ": 0, "Tiền": 0}])
        df_ky = pd.concat([df_ky, new_row], ignore_index=True)
        with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
            df_nv.to_excel(writer, sheet_name="NV", index=False)
            df_ky.to_excel(writer, sheet_name="Ky", index=False)
        st.success(f"Đã ghi VÀO lúc {now}")
        st.rerun()

    if c2.button("RA CA"):
        now = datetime.now().strftime("%H:%M:%S")
        # Tìm dòng của nhân viên đang trống giờ ra
        mask = (df_ky["Tên NV"] == ten_chon) & (df_ky["Giờ Ra"] == "")
        if mask.any():
            df_ky.loc[df_ky[mask].index[-1], "Giờ Ra"] = now
            with pd.ExcelWriter(FILE_DATA, engine='openpyxl') as writer:
                df_nv.to_excel(writer, sheet_name="NV", index=False)
                df_ky.to_excel(writer, sheet_name="Ky", index=False)
            st.success(f"Đã ghi RA lúc {now}")
            st.rerun()
        else:
            st.warning("Không tìm thấy ca vào!")