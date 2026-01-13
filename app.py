import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Tampilan
st.set_page_config(page_title="Bank Sampah RT", layout="wide", page_icon="♻️")

# Inisialisasi Database Sementara di Browser
if "db_sampah" not in st.session_state:
    st.session_state.db_sampah = pd.DataFrame(columns=["Waktu", "Nama Warga", "Jenis Sampah", "Berat (kg)", "Poin"])

# --- HEADER ---
st.title("♻️ Catatan Bank Sampah RT")
st.markdown("Silakan input data. **Penting:** Segera unduh laporan sebelum menutup browser agar data tidak hilang.")
st.divider()

# --- LAYOUT ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📝 Input Data")
    with st.form("form_input", clear_on_submit=True):
        nama = st.text_input("Nama Warga", placeholder="Masukkan nama...")
        jenis = st.selectbox("Jenis Sampah", ["Basah", "Kering", "Campuran"])
        berat = st.number_input("Berat (kg)", min_value=0.0, step=0.1)
        
        btn_simpan = st.form_submit_button("Simpan Catatan")
        
        if btn_simpan:
            if nama and berat > 0:
                waktu_sekarang = datetime.now().strftime("%d/%m/%Y %H:%M")
                poin = berat
                data_baru = pd.DataFrame([[waktu_sekarang, nama, jenis, berat, poin]], 
                                        columns=st.session_state.db_sampah.columns)
                st.session_state.db_sampah = pd.concat([st.session_state.db_sampah, data_baru], ignore_index=True)
                st.success(f"Berhasil mencatat data {nama}!")
            else:
                st.error("Nama dan berat harus diisi!")

with col2:
    st.subheader("📊 Catatan Setoran")
    if not st.session_state.db_sampah.empty:
        st.dataframe(st.session_state.db_sampah, use_container_width=True)
        
        # Fitur Download (Sangat Penting karena data tidak disimpan permanen di server)
        csv = st.session_state.db_sampah.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Unduh Laporan (CSV/Excel)", csv, "laporan_bank_sampah.csv", "text/csv")
        
        if st.button("🗑️ Reset Tabel", type="primary"):
            st.session_state.db_sampah = pd.DataFrame(columns=["Waktu", "Nama Warga", "Jenis Sampah", "Berat (kg)", "Poin"])
            st.rerun()
    else:
        st.info("Belum ada data yang tercatat di sesi ini.")
