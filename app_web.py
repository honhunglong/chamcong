import streamlit as st
import pandas as pd
import os
from datetime import datetime
import io

# --- CẤU HÌNH ---
FILE_CHAM_CONG = "Data_Cham_Cong.xlsx"
FILE_PASS = "pass.txt"

def init_data():
    if not os.path.exists(FILE_PASS):
        with open(FILE_PASS, "w") as f: f.write("888888")
    if not os.path.exists(FILE_CHAM_CONG):
        with pd.ExcelWriter(FILE_CHAM_CONG, engine='openpyxl') as writer:
            pd.DataFrame(columns=["Tên Nhân Viên", "Mức Lương / Giờ", "Trạng Thái"]).to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            pd.DataFrame(columns=["Ngày", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra", "Tổng Giờ", "Thành Tiền"]).to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)

init_data()
st.set_page_config(page_title="Hệ thống Chấm công", layout="wide")
st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG & LƯƠNG")

# Load data
df_nv = pd.read_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV")
df_nhat_ky = pd.read_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca")
with open(FILE_PASS, "r") as f: current_pass = f.read().strip()

# --- ADMIN PANEL ---
with st.sidebar:
    st.header("🔑 Quản trị Admin")
    pwd = st.text_input("Mật khẩu Admin:", type="password")
    if pwd == current_pass:
        st.success("Đã đăng nhập Admin")
        # Đổi mật khẩu
        new_pass = st.text_input("Đổi mật khẩu:", type="password")
        if st.button("Xác nhận đổi mật khẩu"):
            with open(FILE_PASS, "w") as f: f.write(new_pass)
            st.rerun()
        # Thêm/Xóa NV
        n_name = st.text_input("Tên NV mới:")
        n_salary = st.number_input("Lương/giờ:", value=20000)
        if st.button("Thêm nhân viên"):
            df_nv = pd.concat([df_nv, pd.DataFrame([{"Tên Nhân Viên": n_name, "Mức Lương / Giờ": n_salary, "Trạng Thái": "Ngoài"}])], ignore_index=True)
            df_nv.to_excel(FILE_CHAM_CONG, sheet_name="Danh_Sach_NV", index=False, mode='a', if_sheet_exists='replace')
            st.rerun()
        # Sửa nhật ký
        st.subheader("Chỉnh sửa & Báo cáo")
        edited_log = st.data_editor(df_nhat_ky)
        if st.button("Lưu thay đổi nhật ký"):
            edited_log.to_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca", index=False, mode='a', if_sheet_exists='replace')
            st.rerun()
        
        # NÚT XUẤT FILE EXCEL
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_nv.to_excel(writer, sheet_name="Danh_Sach_NV", index=False)
            df_nhat_ky.to_excel(writer, sheet_name="Nhat_Ky_Ca", index=False)
        st.download_button(label="📥 Tải file Excel Báo cáo", data=buffer, file_name="Bao_Cao_Cham_Cong.xlsx", mime="application/vnd.ms-excel")
            
    else:
        st.info("Nhập mật khẩu Admin.")

# --- NHÂN VIÊN PANEL ---
st.subheader("Danh sách nhân viên")
st.table(df_nv[["Tên Nhân Viên", "Trạng Thái"]])

selected_name = st.selectbox("Chọn tên của bạn:", df_nv["Tên Nhân Viên"].tolist())
col1, col2 = st.columns(2)

if col1.button("BẮT ĐẦU VÀO CA"):
    new_row = pd.DataFrame([{"Ngày": datetime.now().strftime('%Y-%m-%d'), "Tên Nhân Viên": selected_name, "Giờ Vào": datetime.now().strftime('%H:%M:%S'), "Giờ Ra": "", "Tổng Giờ": 0, "Thành Tiền": 0}])
    df_nhat_ky = pd.concat([df_nhat_ky, new_row], ignore_index=True)
    df_nhat_ky.to_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca", index=False, mode='a', if_sheet_exists='replace')
    st.success("Đã ghi giờ vào!")

if col2.button("KẾT THÚC RA CA"):
    mask = (df_nhat_ky["Tên Nhân Viên"] == selected_name) & (df_nhat_ky["Giờ Ra"] == "")
    if mask.any():
        idx = df_nhat_ky[mask].index[-1]
        gio_vao = datetime.strptime(df_nhat_ky.at[idx, "Giờ Vào"], '%H:%M:%S')
        gio_ra = datetime.now()
        tong_gio = (gio_ra - datetime.combine(datetime.now().date(), gio_vao.time())).total_seconds() / 3600
        df_nhat_ky.at[idx, "Giờ Ra"] = gio_ra.strftime('%H:%M:%S')
        df_nhat_ky.at[idx, "Tổng Giờ"] = round(tong_gio, 2)
        df_nhat_ky.at[idx, "Thành Tiền"] = round(tong_gio * df_nv[df_nv["Tên Nhân Viên"] == selected_name]["Mức Lương / Giờ"].values[0], 0)
        df_nhat_ky.to_excel(FILE_CHAM_CONG, sheet_name="Nhat_Ky_Ca", index=False, mode='a', if_sheet_exists='replace')
        st.success(f"Đã ghi giờ ra! Lương: {int(df_nhat_ky.at[idx, 'Thành Tiền']):,}đ")
    else:
        st.warning("Không tìm thấy ca làm việc chưa kết thúc!")