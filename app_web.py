import streamlit as st
import pandas as pd
import os

FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"

@st.cache_data(ttl=1)
def load_data():
    if not os.path.exists(FILE_CHAM_CONG):
        # Tạo file mới với 2 sheet đúng tên
        with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Mức Lương", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

    # Sau khi đảm bảo file đã tồn tại, mới đọc vào
    return pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV"), pd.read_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca")