import streamlit as st
import pandas as pd
import os

FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"

@st.cache_data(ttl=60)
def load_data():
    # XÓA FILE CŨ ĐỂ KHÔNG BỊ XUNG ĐỘT DỮ LIỆU
    if os.path.exists(FILE_CHAM_CONG):
        os.remove(FILE_CHAM_CONG)
    
    # TẠO FILE MỚI TINH
    with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
        pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
        pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Mức Lương", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
    
    return pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV"), pd.read_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca")

st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG")
df_nv, df_nhat_ky = load_data()
st.success("Dữ liệu đã được làm mới hoàn toàn!")
st.dataframe(df_nv)