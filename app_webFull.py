import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime

# Cấu hình
URL = "https://aqwkngqmnnikmhwyxysa.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFxd2tuZ3Ftbm5pa21od3l4eXNhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDU0MDA5MSwiZXhwIjoyMDk2MTE2MDkxfQ.u9888upVfSJCOWE8-fVR8lM4v8lmseImD1vTib54cPE"
supabase = create_client(URL, KEY)

if 'user' not in st.session_state: st.session_state.user = None

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
    
    if user['role'] == 'admin':
        st.title("Admin: Quản trị Nhân viên")
        
        # CHỨC NĂNG THÊM NHÂN VIÊN NGAY TRÊN WEB
        with st.form("them_nv"):
            u = st.text_input("Username mới")
            p = st.text_input("Password mới")
            l = st.number_input("Lương/giờ")
            if st.form_submit_button("Lưu nhân viên mới"):
                supabase.table("nhan_vien").insert({"username":u, "password":p, "role":"nhan_vien", "luong_gio":l}).execute()
                st.success("Đã thêm nhân viên!")

        # XEM VÀ XÓA NHÂN VIÊN
        st.write("---")
        data = supabase.table("nhan_vien").select("*").execute().data
        df = pd.DataFrame(data)
        st.table(df[['username', 'luong_gio']]) # Hiển thị danh sách
        
        del_user = st.text_input("Nhập username cần xóa")
        if st.button("Xóa nhân viên"):
            supabase.table("nhan_vien").delete().eq("username", del_user).execute()
            st.rerun()

    else:
        st.title(f"Chào {user['username']}")
        # Giao diện chấm công cho nhân viên
        if st.button("VÀO CA"):
            supabase.table("cham_cong").insert({"username": user['username'], "gio_vao": str(datetime.now())}).execute()
            st.success("Đã vào ca!")
        if st.button("RA CA"):
            # Tìm dòng đang làm và cập nhật
            d = supabase.table("cham_cong").select("*").eq("username", user['username']).is_("gio_ra", "null").execute().data
            if d:
                gio_ra = datetime.now()
                gio_vao = pd.to_datetime(d[0]['gio_vao'])
                tong_gio = (gio_ra - gio_vao).total_seconds() / 3600
                supabase.table("cham_cong").update({
                    "gio_ra": str(gio_ra),
                    "tong_gio": round(tong_gio, 2),
                    "tong_tien": round(tong_gio * user['luong_gio'], 2)
                }).eq("id", d[0]['id']).execute()
                st.success("Đã ra ca và tính lương!")