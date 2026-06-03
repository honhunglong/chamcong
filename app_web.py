import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CẤU HÌNH ---
FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"
PASSWORD_ADMIN = "888888" # ANH THAY ĐỔI MẬT KHẨU TẠI ĐÂY

def init_data():
    if not os.path.exists(FILE_CHAM_CONG):
        with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

init_data()

# --- GIAO DIỆN ---
st.set_page_config(page_title="Hệ thống Chấm công", layout="wide")
st.title("🕒 HỆ THỐNG CHẤM CÔNG")

# Đọc dữ liệu
df_nv = pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV")
df_nhat_ky = pd.read_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca")

# 1. KHU VỰC ADMIN
with st.sidebar:
    st.header("🔑 Quản trị Admin")
    pwd = st.text_input("Mật khẩu Admin:", type="password")
    
    if pwd == PASSWORD_ADMIN:
        st.success("Đã đăng nhập Admin")
        
        # Thêm nhân viên
        st.subheader("Thêm/Xóa nhân viên")
        new_name = st.text_input("Tên nhân viên mới:")
        new_salary = st.number_input("Lương/giờ:", value=20000)
        if st.button("Thêm nhân viên"):
            new_row = pd.DataFrame([{"Tên Nhân Viên": new_name, "Mức Lương / Giờ": new_salary, "Trạng Thái": "Đang ở ngoài"}])
            df_nv = pd.concat([df_nv, new_row], ignore_index=True)
            df_nv.to_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV", index=False, mode='a', if_sheet_exists='replace')
            st.rerun()
            
        # Xóa nhân viên
        del_name = st.selectbox("Chọn nhân viên xóa:", df_nv["Tên Nhân Viên"].tolist())
        if st.button("Xóa nhân viên"):
            df_nv = df_nv[df_nv["Tên Nhân Viên"] != del_name]
            df_nv.to_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV", index=False, mode='a', if_sheet_exists='replace')
            st.rerun()
            
        st.divider()
        st.subheader("Chỉnh sửa nhật ký chấm công")
        df_edited = st.data_editor(df_nhat_ky)
        if st.button("Lưu nhật ký"):
            df_edited.to_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca", index=False, mode='a', if_sheet_exists='replace')
            st.rerun()
    else:
        st.info("Nhập mật khẩu để quản lý.")

# 2. GIAO DIỆN NHÂN VIÊN
st.subheader("Danh sách nhân viên")
# Nhân viên không thấy cột lương
st.table(df_nv[["Tên Nhân Viên", "Trạng Thái"]])

selected_name = st.selectbox("Chọn tên của bạn:", df_nv["Tên Nhân Viên"].tolist())
if st.button("BẮT ĐẦU VÀO CA"):
    st.write(f"Đã ghi nhận vào lúc: {datetime.now().strftime('%H:%M:%S')}")
if st.button("KẾT THÚC RA CA"):
    st.write("Đã ghi nhận ra ca.")