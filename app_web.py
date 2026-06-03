import streamlit as st
import pandas as pd
import os

# Cấu hình trang web
st.set_page_config(page_title="Hệ thống Chấm công", layout="centered")

FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"

# Tạo file Excel nếu chưa tồn tại
if not os.path.exists(FILE_CHAM_CONG):
    df_nv = pd.DataFrame([
        {"Tên Nhân Viên": "Nguyễn Văn A", "Mức Lương / Giờ": 20000, "Trạng Thái": "Đang ở ngoài"},
        {"Tên Nhân Viên": "Trần Thị B", "Mức Lương / Giờ": 25000, "Trạng Thái": "Đang ở ngoài"},
    ])
    df_nhat_ky = pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ Lập Trình", "Mức Lương Lúc Đó", "Thành Tiền"])
    with pd.ExcelWriter(FILE_CHAM_CONG) as writer:
        df_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
        df_nhat_ky.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

# Hàm đọc dữ liệu
@st.cache_data
def load_data():
    return pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV"), pd.read_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca")

df_nv, df_nhat_ky = load_data()

st.title("🕒 HỆ THỐNG CHẤM CÔNG")

# Khu vực nhân viên
st.subheader("Dành cho nhân viên")
ten_nv = st.selectbox("Chọn tên của bạn:", df_nv["Tên Nhân Viên"].tolist())

col1, col2 = st.columns(2)
if col1.button("BẮT ĐẦU VÀO CA"):
    # Xử lý logic vào ca tương tự như code cũ của bạn
    st.success(f"Chào {ten_nv}, đã ghi nhận vào ca!")

if col2.button("KẾT THÚC RA CA"):
    # Xử lý logic ra ca
    st.info(f"Đã ghi nhận ra ca cho {ten_nv}")

# Khu vực Admin
st.divider()
st.subheader("Khu vực quản lý (Admin)")
password = st.text_input("Nhập mật khẩu Admin:", type="password")

if password == "admin123":
    tab1, tab2 = st.tabs(["Cập nhật lương", "Tính lương cuối tháng"])
    
    with tab1:
        new_name = st.text_input("Tên nhân viên:")
        new_salary = st.number_input("Mức lương/giờ:", min_value=0)
        if st.button("Cập nhật"):
            st.write("Đã cập nhật!")
            
    with tab2:
        month = st.selectbox("Chọn tháng:", range(1, 13))
        if st.button("Tính lương"):
            st.write(f"Bảng lương tháng {month}")
else:
    st.warning("Vui lòng nhập đúng mật khẩu để truy cập quản trị.")