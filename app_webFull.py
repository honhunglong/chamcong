import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime, timezone

# 1. Kết nối (giữ nguyên)
URL = "https://aqwkngqmnnikmhwyxysa.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFxd2tuZ3Ftbm5pa21od3l4eXNhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDU0MDA5MSwiZXhwIjoyMDk2MTE2MDkxfQ.u9888upVfSJCOWE8-fVR8lM4v8lmseImD1vTib54cPE"
supabase = create_client(URL, KEY)

if 'user' not in st.session_state: st.session_state.user = None

# 2. Đăng nhập
if not st.session_state.user:
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Đăng nhập"):
        res = supabase.table("nhan_vien").select("*").eq("username", u).eq("password", p).execute()
        if res.data:
            st.session_state.user = res.data[0]
            st.rerun()
else:
    user = st.session_state.user
    st.title(f"👋 Chào {user['username']}")

    # 3. XỬ LÝ VÀO CA
    if st.button("✅ VÀO CA"):
        try:
            # Tạo ID an toàn, không phụ thuộc Database
            data = {
                "ID": int(datetime.now().timestamp()),
                "username": user['username'],
                "gio_vao": datetime.now(timezone.utc).isoformat()
            }
            supabase.table("cham_cong").insert(data).execute()
            st.success("Đã vào ca!")
            st.rerun()
        except Exception as e:
            st.error(f"Lỗi vào ca: {e}")

    # 4. XỬ LÝ RA CA (Đã sửa lỗi tz-aware)
    if st.button("❌ RA CA"):
        try:
            res = supabase.table("cham_cong").select("ID, gio_vao").eq("username", user['username']).is_("gio_ra", "null").execute()
            if res.data:
                d = res.data[0]
                ra = datetime.now(timezone.utc)
                # Chuyển giờ vào từ DB sang định dạng có múi giờ
                vao = pd.to_datetime(d['gio_vao'])
                
                gio = (ra - vao).total_seconds() / 3600
                
                supabase.table("cham_cong").update({
                    "gio_ra": ra.isoformat(),
                    "tong_gio": round(gio, 2),
                    "tong_tien": round(gio * user['luong_gio'], 2)
                }).eq("ID", d['ID']).execute()
                st.success("Đã ra ca thành công!")
                st.rerun()
            else:
                st.warning("Không tìm thấy ca đang mở.")
        except Exception as e:
            st.error(f"Lỗi ra ca: {e}")