import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime
import io

# Kết nối
URL = "https://aqwkngqmnnikmhwyxysa.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFxd2tuZ3Ftbm5pa21od3l4eXNhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDU0MDA5MSwiZXhwIjoyMDk2MTE2MDkxfQ.u9888upVfSJCOWE8-fVR8lM4v8lmseImD1vTib54cPE"
supabase = create_client(URL, KEY)

if 'user' not in st.session_state: st.session_state.user = None

if not st.session_state.user:
    st.title("ĐĂNG NHẬP")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Đăng nhập"):
        res = supabase.table("nhan_vien").select("*").eq("username", u).eq("password", p).execute()
        if res.data:
            st.session_state.user = res.data[0]
            st.rerun()
        else: st.error("Sai thông tin!")
else:
    user = st.session_state.user
    if user['role'] == 'admin':
        st.title("⚙️ QUẢN TRỊ")
        # Tính năng xuất file Excel
        data = supabase.table("cham_cong").select("*").execute().data
        if data:
            df = pd.DataFrame(data)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            st.download_button("📥 Tải lịch sử chấm công (Excel)", data=output.getvalue(), file_name="cham_cong.xlsx", mime="application/vnd.ms-excel")
    else:
        st.title(f"👋 Chào {user['username']}")         
        
        # VÀO CA - Dùng ID tự sinh từ thời gian để tránh lỗi NOT NULL
        if st.button("✅ VÀO CA"):
            try:
                data = {
                    "ID": int(datetime.now().timestamp() * 1000), 
                    "username": str(user['username']), 
                    "gio_vao": str(datetime.now().astimezone()) # Giờ chuẩn Việt Nam
                }
                supabase.table("cham_cong").insert(data).execute()
                st.success("Đã vào ca!")
                st.rerun()
            except Exception as e: st.error(f"Lỗi: {e}")

        # RA CA
        if st.button("❌ RA CA"):
            try:
                res = supabase.table("cham_cong").select("ID, gio_vao").eq("username", user['username']).is_("gio_ra", "null").execute()
                if res.data:
                    d = res.data[0]
                    ra = datetime.now().astimezone()
                    vao = pd.to_datetime(d['gio_vao']).astimezone()
                    gio = (ra - vao).total_seconds() / 3600
                    supabase.table("cham_cong").update({
                        "gio_ra": str(ra),
                        "tong_gio": round(gio, 2),
                        "tong_tien": round(gio * user['luong_gio'], 2)
                    }).eq("ID", d['ID']).execute()
                    st.success("Đã ra ca!")
                    st.rerun()
                else: st.warning("Không tìm thấy ca mở!")
            except Exception as e: st.error(f"Lỗi: {e}")