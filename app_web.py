import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Hệ thống Chấm công", layout="wide")

FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"

# Hàm kiểm tra mật khẩu Admin
def check_password():
    password = st.sidebar.text_input("Mật khẩu Admin:", type="password")
    if password == "123456": # Đổi mật khẩu tại đây
        return True
    return False

# Đọc dữ liệu
@st.cache_data(ttl=1)
def load_data():
    return pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV"), pd.read_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca")

df_nv, df_nhat_ky = load_data()

st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG")

# --- GIAO DIỆN ADMIN ---
if check_password():
    st.sidebar.success("Đã đăng nhập quyền Admin")
    
    tabs = st.tabs(["Quản lý Nhân viên", "Chỉnh sửa Nhật ký", "Báo cáo Lương"])
    
    with tabs[0]:
        st.subheader("Thêm/Sửa/Xóa Nhân viên")
        # Thêm mới
        with st.form("add_nv"):
            ten = st.text_input("Tên nhân viên:")
            luong = st.number_input("Mức lương/giờ:", value=20000)
            if st.form_submit_button("Thêm nhân viên"):
                new_df = pd.concat([df_nv, pd.DataFrame([{"Tên Nhân Viên": ten, "Mức Lương / Giờ": luong, "Trạng Thái": "Đang ở ngoài"}])])
                new_df.to_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV", index=False)
                st.rerun()

        # Hiển thị và Xóa
        st.write(df_nv)
        if st.button("Xóa nhân viên cuối danh sách"):
            df_nv = df_nv.iloc[:-1]
            df_nv.to_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV", index=False)
            st.rerun()

    with tabs[1]:
        st.subheader("Chỉnh sửa Nhật ký chấm công")
        st.write("Sửa trực tiếp bên dưới (sau khi sửa hãy lưu file Excel hoặc dùng code cập nhật):")
        edited_log = st.data_editor(df_nhat_ky)
        if st.button("Lưu thay đổi nhật ký"):
            with pd.ExcelWriter(FILE_CHAM_CONG, mode='a', if_sheet_exists='replace') as writer:
                edited_log.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
                st.success("Đã lưu!")

    with tabs[2]:
        st.subheader("Bảng lương (Định dạng VNĐ)")
        # Định dạng tiền tệ
        df_display = df_nhat_ky.copy()
        df_display["Thành Tiền"] = df_display["Thành Tiền"].apply(lambda x: f"{x:,.0f}đ")
        st.table(df_display)

else:
    st.warning("Vui lòng nhập mật khẩu Admin ở thanh bên trái để thực hiện quyền quản lý.")

# --- GIAO DIỆN NHÂN VIÊN (Ai cũng thấy) ---
st.divider()
st.subheader("Chấm công hàng ngày")
ten_nv = st.selectbox("Chọn tên:", df_nv["Tên Nhân Viên"].tolist())
if st.button("BẮT ĐẦU VÀO CA"):
    st.write("Đã ghi nhận!")