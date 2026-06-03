import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Hệ thống Chấm công", layout="wide")

FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"

# Hàm khởi tạo dữ liệu chuẩn
def init_data():
    if not os.path.exists(FILE_CHAM_CONG):
        with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

init_data()

# Hàm tải dữ liệu
@st.cache_data(ttl=60)
def load_data():
    df_nv = pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV")
    df_nhat_ky = pd.read_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca")
    return df_nv, df_nhat_ky

df_nv, df_nhat_ky = load_data()

st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG")

# 1. GIAO DIỆN ADMIN
with st.sidebar:
    st.header("🔑 Quản trị Admin")
    pwd = st.text_input("Mật khẩu:", type="password")
    if pwd == "123456":
        st.success("Đã đăng nhập Admin")
        new_name = st.text_input("Tên nhân viên mới:")
        new_salary = st.number_input("Lương/giờ:", value=20000)
        if st.button("Thêm nhân viên"):
            new_row = pd.DataFrame([{"Tên Nhân Viên": new_name, "Mức Lương / Giờ": new_salary, "Trạng Thái": "Đang ở ngoài"}])
            df_nv = pd.concat([df_nv, new_row], ignore_index=True)
            with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            st.rerun()
    else:
        st.info("Nhập mật khẩu để quản lý nhân viên.")

# 2. GIAO DIỆN CHẤM CÔNG
st.subheader("Bảng chấm công")
if not df_nv.empty:
    st.table(df_nv)
    name = st.selectbox("Chọn tên của bạn:", df_nv["Tên Nhân Viên"].tolist())
    
    col1, col2 = st.columns(2)
    if col1.button("BẮT ĐẦU VÀO CA"):
        st.write(f"Chào {name}, đã lưu giờ vào: {datetime.now().strftime('%H:%M:%S')}")
    if col2.button("KẾT THÚC RA CA"):
        st.write(f"Chào {name}, đã lưu giờ ra: {datetime.now().strftime('%H:%M:%S')}")
else:
    st.warning("Admin chưa thêm nhân viên nào!")