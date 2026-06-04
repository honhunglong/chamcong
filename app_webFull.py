import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime

# Kết nối (Điền KEY service_role của bạn vào đây)
URL = "https://aqwkngqmnnikmhwyxysa.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFxd2tuZ3Ftbm5pa21od3l4eXNhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MDU0MDA5MSwiZXhwIjoyMDk2MTE2MDkxfQ.u9888upVfSJCOWE8-fVR8lM4v8lmseImD1vTib54cPE"
supabase = create_client(URL, KEY)

if 'user' not in st.session_state: st.session_state.user = None

# GIAO DIỆN ĐĂNG NHẬP
if not st.session_state.user:
    st.title("ĐĂNG NHẬP HỆ THỐNG")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Đăng nhập"):
        res = supabase.table("nhan_vien").select("*").eq("username", u).eq("password", p).execute()
        if res.data:
            st.session_state.user = res.data[0]
            st.rerun()
        else:
            st.error("Sai thông tin!")
else:
    user = st.session_state.user
    
    # GIAO DIỆN ADMIN
    if user['role'] == 'admin':
        st.title("⚙️ QUẢN TRỊ NHÂN VIÊN")
        
        # Thêm nhân viên
        with st.expander("➕ Thêm nhân viên mới"):
            with st.form("them_moi"):
                new_u = st.text_input("Username")
                new_p = st.text_input("Password")
                new_l = st.number_input("Lương/giờ", value=0.0)
                if st.form_submit_button("Lưu"):
                    supabase.table("nhan_vien").insert({"username": new_u, "password": new_p, "role": "nhan_vien", "luong_gio": new_l}).execute()
                    st.success("Đã thêm!")
        
        # Danh sách & Xóa
        data = supabase.table("nhan_vien").select("*").execute().data
        df = pd.DataFrame(data)
        st.table(df[['username', 'luong_gio']])
        
        target_del = st.text_input("Nhập username muốn xóa")
        if st.button("🗑️ Xóa nhân viên này"):
            supabase.table("nhan_vien").delete().eq("username", target_del).execute()
            st.rerun()

        if st.button("📥 Xuất dữ liệu chấm công"):
            cc = supabase.table("cham_cong").select("*").execute().data
            st.download_button("Tải File", pd.DataFrame(cc).to_csv(), "cham_cong.csv")

    # GIAO DIỆN NHÂN VIÊN
    else:
        st.title(f"👋 Chào {user['username']}")
       if st.button("✅ VÀO CA"):
     try:
        data = {"username": str(user['username']), "gio_vao": str(datetime.now())}
        supabase.table("cham_cong").insert(data).execute()
        st.success("Đã vào ca!")
        st.rerun()
    except Exception as e:
        st.error(f"Lỗi vào ca: {e}")

# --- XỬ LÝ RA CA ---
if st.button("❌ RA CA"):
    try:
        # 1. Tìm dòng mới nhất của user chưa có 'gio_ra'
        d = supabase.table("cham_cong").select("*").eq("username", user['username']).is_("gio_ra", "null").execute()
        
        if d.data:
            # 2. Lấy ID của dòng đó
            record_id = d.data[0]['ID']
            gio_vao_dt = pd.to_datetime(d.data[0]['gio_vao'])
            gio_ra_dt = datetime.now()
            
            # 3. Tính toán
            gio_lam = (gio_ra_dt - gio_vao_dt).total_seconds() / 3600
            
            # 4. Cập nhật vào đúng ID đó
            supabase.table("cham_cong").update({
                "gio_ra": str(gio_ra_dt),
                "tong_gio": round(gio_lam, 2)
            }).eq("ID", record_id).execute()
            
            st.success("Đã ra ca!")
            st.rerun()
        else:
            st.warning("Không tìm thấy ca làm việc đang mở!")
    except Exception as e:
        st.error(f"Lỗi ra ca: {e}")
                # Nếu có lỗi, nó sẽ in ra màn hình để bạn biết nguyên nhân
                st.error(f"Lỗi Database: {e}")
        if st.button("❌ RA CA"):
            d = supabase.table("cham_cong").select("*").eq("username", user['username']).is_("gio_ra", "null").execute().data
            if d:
                ra = datetime.now()
                vao = pd.to_datetime(d[0]['gio_vao'])
                gio = (ra - vao).total_seconds() / 3600
                supabase.table("cham_cong").update({
                    "gio_ra": str(ra),
                    "tong_gio": round(gio, 2),
                    "tong_tien": round(gio * user['luong_gio'], 2)
                }).eq("id", d[0]['id']).execute()
                st.success("Đã lưu!")