# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime

# Cấu hình
URL = "https://aqwkngqmnnikmhwyxysa.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFxd2tuZ3Ftbm5pa21od3l4eXNhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDU0MDA5MSwiZXhwIjoyMDk2MTE2MDkxfQ.u9888upVfSJCOWE8-fVR8lM4v8lmseImD1vTib54cPE"
supabase = create_client(URL, KEY)

if 'user' not in st.session_state: st.session_state.user = None

# GIAO DIỆN ĐĂNG NHẬP
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
    
    # GIAO DIỆN ADMIN
    if user['role'] == 'admin':
        st.title("Admin Panel")
        
        # 1. Quản lý nhân viên
        with st.expander("Thêm/Sửa/Xóa Nhân Viên"):
            new_u = st.text_input("Username mới")
            new_p = st.text_input("Password mới")
            new_l = st.number_input("Lương/giờ")
            if st.button("Thêm NV"):
                supabase.table("nhan_vien").insert({"username": new_u, "password": new_p, "role": "nhan_vien", "luong_gio": new_l}).execute()
        
        # 2. Đổi mật khẩu Admin
        with st.expander("Đổi mật khẩu Admin"):
            new_pass = st.text_input("Mật khẩu mới", type="password")
            if st.button("Lưu mật khẩu mới"):
                supabase.table("nhan_vien").update({"password": new_pass}).eq("username", user['username']).execute()
        
        # 3. Xuất báo cáo
        if st.button("Xuất Excel chấm công"):
            data = supabase.table("cham_cong").select("*").execute().data
            st.download_button("Tải file CSV", pd.DataFrame(data).to_csv(index=False), "bang_luong.csv")

    # GIAO DIỆN NHÂN VIÊN
    else:
        st.title(f"Chào {user['username']}")
        if st.button("VÀO CA"):
            supabase.table("cham_cong").insert({"username": user['username'], "gio_vao": datetime.now().isoformat()}).execute()
        if st.button("RA CA"):
            d = supabase.table("cham_cong").select("*").eq("username", user['username']).is_("gio_ra", "null").execute().data
            if d:
                vao = pd.to_datetime(d[0]['gio_vao'])
                ra = datetime.now()
                gio = (ra - vao).total_seconds() / 3600
                supabase.table("cham_cong").update({
                    "gio_ra": ra.isoformat(),
                    "tong_gio": round(gio, 2),
                    "tong_tien": round(gio * user['luong_gio'], 2)
                }).eq("id", d[0]['id']).execute()
                st.success("Đã ghi nhận!")