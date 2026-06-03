import streamlit as st
import pandas as pd
import os

FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"

# Hàm khởi tạo dữ liệu
def init_file():
    if not os.path.exists(FILE_CHAM_CONG):
        with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Mức Lương", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

# Gọi hàm khởi tạo ngay khi chạy
init_file()

@st.cache_data(ttl=1)
def load_data():
    # Đọc file (đã chắc chắn tồn tại nhờ hàm init_file ở trên)
    df_nv = pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV")
    df_nhat_ky = pd.read_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca")
    return df_nv, df_nhat_ky

# Sử dụng dữ liệu
df_nv, df_nhat_ky = load_data()

st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG")
st.write("Dữ liệu đã được tải thành công!")
st.dataframe(df_nv)