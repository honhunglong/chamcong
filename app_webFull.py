# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime

# 1. THIẾT LẬP KẾT NỐI - Đảm bảo chỉ dùng ký tự ASCII tiêu chuẩn
SUPABASE_URL = "https://aqwkngqmnnikmhwyxysa.supabase.co"
SUPABASE_KEY = "DÁN_MÃ_ANON_PUBLIC_CỦA_BẠN_VÀO_ĐÂY" 

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("HE THONG QUAN LY CHAM CONG") # Tạm thời bỏ dấu tiếng Việt ở tiêu đề để loại trừ lỗi encoding

try:
    # 2. Lấy dữ liệu Nhân Viên
    response_nv = supabase.table("nhan_vien").select("*").execute()
    df_nv = pd.DataFrame(response_nv.data)
    
    ten_chon = st.selectbox("Chon ten nhan vien:", df_nv["ten_nv"].tolist())

    if st.button("VAO CA"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {"ten_nv": ten_chon, "gio_vao": now}
        supabase.table("cham_cong").insert(data).execute()
        st.success("Da ghi nhan!")

except Exception as e:
    st.error(f"Loi ket noi: {e}")

# 3. Hiển thị lịch sử (Không dùng dấu tiếng Việt ở tiêu đề)
st.subheader("Lich su gan day")
response_lichsu = supabase.table("cham_cong").select("*").order("gio_vao", desc=True).limit(5).execute()
df_lichsu = pd.DataFrame(response_lichsu.data)
st.table(df_lichsu)