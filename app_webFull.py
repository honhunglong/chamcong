# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from supabase import create_client

# Dùng đúng URL dự án của bạn
SUPABASE_URL = "https://aqwkngqmnnikmhwyxysa.supabase.co"

# Dán khóa 'service_role' bạn vừa copy ở Bước 1 vào đây
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFxd2tuZ3Ftbm5pa21od3l4eXNhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDU0MDA5MSwiZXhwIjoyMDk2MTE2MDkxfQ.u9888upVfSJCOWE8-fVR8lM4v8lmseImD1vTib54cPE"

# Khởi tạo client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("QUAN LY CHAM CONG")

try:
    # Lấy dữ liệu từ bảng 'nhan_vien'
    response = supabase.table("nhan_vien").select("*").execute()
    data = response.data
    
    if data:
        df_nv = pd.DataFrame(data)
        ten_chon = st.selectbox("Chon nhan vien:", df_nv["ten_nv"].tolist())
        
        if st.button("VAO CA"):
            supabase.table("cham_cong").insert({"ten_nv": ten_chon}).execute()
            st.success("Da cham cong!")
    else:
        st.warning("Khong tim thay du lieu nhan vien trong bang.")

except Exception as e:
    st.error(f"Loi ket noi: {str(e)}")