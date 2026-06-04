Để chạy ứng dụng trên web với Supabase, bạn cần một file app_webFull.py hoàn chỉnh. Dưới đây là đoạn code đã được thiết kế lại để hoạt động trơn tru với Database (thay vì file Excel cũ).

Mã nguồn app_webFull.py hoàn chỉnh:
Python
import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime

# 1. THIẾT LẬP KẾT NỐI (Dán URL và KEY của bạn vào đây)
SUPABASE_URL = "https://aqwkngqmnnikmhwyxysa.supabase.co"
SUPABASE_KEY = "DÁN_MÃ_ANON_PUBLIC_VÀO_ĐÂY" 
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("🕒 HỆ THỐNG QUẢN LÝ CHẤM CÔNG")

# 2. Lấy dữ liệu Nhân Viên từ Supabase
try:
    response_nv = supabase.table("nhan_vien").select("*").execute()
    # Chuyển dữ liệu thành DataFrame
    df_nv = pd.DataFrame(response_nv.data)
    
    # 3. Giao diện chọn nhân viên
    ten_chon = st.selectbox("Chọn tên nhân viên:", df_nv["ten_nv"].tolist())

    # 4. Nút bấm chấm công
    if st.button("VÀO CA"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Ghi dữ liệu vào bảng cham_cong trên Supabase
        data = {"ten_nv": ten_chon, "gio_vao": now}
        supabase.table("cham_cong").insert(data).execute()
        st.success(f"Đã ghi nhận VÀO CA cho {ten_chon} lúc {now}")

except Exception as e:
    st.error(f"Lỗi kết nối database: {e}")
    st.info("Hãy kiểm tra lại URL và API Key trong code.")

# Xem lịch sử chấm công
st.subheader("Lịch sử gần đây")
response_lichsu = supabase.table("cham_cong").select("*").order("gio_vao", desc=True).limit(5).execute()
df_lichsu = pd.DataFrame(response_lichsu.data)
st.table(df_lichsu)