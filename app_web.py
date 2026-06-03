import streamlit as st
import pandas as pd
import os

FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"

# 1. Hàm khởi tạo dữ liệu
def init_data():
    if not os.path.exists(FILE_CHAM_CONG):
        with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

init_data()

# 2. Giao diện chính
st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG")

# Đọc dữ liệu
df_nv = pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV")

# 3. Chức năng Admin (Để thêm nhân viên)
with st.expander("🔑 Khu vực Admin"):
    password = st.text_input("Nhập mật khẩu Admin:", type="password")
    if password == "123456": # Mật khẩu admin
        new_name = st.text_input("Tên nhân viên mới:")
        new_salary = st.number_input("Mức lương/giờ:", value=20000)
        if st.button("Thêm nhân viên"):
            new_row = pd.DataFrame([{"Tên Nhân Viên": new_name, "Mức Lương / Giờ": new_salary, "Trạng Thái": "Đang ở ngoài"}])
            df_nv = pd.concat([df_nv, new_row], ignore_index=True)
            with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            st.rerun()
    else:
        st.write("Vui lòng nhập đúng mật khẩu để quản lý.")

# 4. Giao diện chấm công cho nhân viên
st.subheader("Danh sách nhân viên")
if not df_nv.empty:
    # Định dạng tiền tệ cho bảng hiển thị
    df_display = df_nv.copy()
    df_display["Mức Lương / Giờ"] = df_display["Mức Lương / Giờ"].apply(lambda x: f"{x:,.0f} đ")
    st.table(df_display)
    
    selected_name = st.selectbox("Chọn tên của bạn:", df_nv["Tên Nhân Viên"].tolist())
    col1, col2 = st.columns(2)
    if col1.button("BẮT ĐẦU VÀO CA"):
        st.write(f"Chào {selected_name}, đã ghi nhận giờ vào!")
    if col2.button("KẾT THÚC RA CA"):
        st.write(f"Cảm ơn {selected_name}, đã ghi nhận giờ ra!")
else:
    st.write("Chưa có nhân viên nào. Hãy đăng nhập Admin để thêm.")