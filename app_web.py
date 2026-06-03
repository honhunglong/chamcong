import streamlit as st
import pandas as pd
import os

FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"

@st.cache_data(ttl=60)
def load_data():
    # Kiểm tra nếu file không tồn tại, tạo mới hoàn toàn
    if not os.path.exists(FILE_CHAM_CONG):
        with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
            # Tạo Sheet 1: Danh_Sach_NV
            pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            # Tạo Sheet 2: Nhat_Ky_Ca
            pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Mức Lương", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
    
    # Đọc dữ liệu sau khi đảm bảo file đã tồn tại
    try:
        df_nv = pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV")
        df_nhat_ky = pd.read_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca")
        return df_nv, df_nhat_ky
    except Exception as e:
        st.error(f"Lỗi khi đọc file: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Giao diện
st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG")
df_nv, df_nhat_ky = load_data()
st.write("Dữ liệu đã sẵn sàng!")
st.dataframe(df_nv)