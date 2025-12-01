import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# ===============================
# DATA GENERATOR - BUAT DATA OTOMATIS
# ===============================
def generate_stunting_data():
    np.random.seed(42)
    n_samples = 300
    
    data = {
        'id_balita': [f'B2025_{i:03d}' for i in range(1, n_samples+1)],
        'usia_balita_bulan': np.random.randint(6, 61, n_samples),
        'jenis_kelamin': np.random.choice(['Laki-laki', 'Perempuan'], n_samples),
        'berat_badan_kg': np.round(np.random.uniform(6.0, 18.0, n_samples), 2),
        'tinggi_badan_cm': np.round(np.random.uniform(65.0, 110.0, n_samples), 2),
        'berat_lahir_kg': np.round(np.random.uniform(2.5, 4.0, n_samples), 2),
        'asi_eksklusif': np.random.choice(['Ya', 'Tidak'], n_samples, p=[0.6, 0.4]),
        'pendidikan_ibu': np.random.choice(['SD', 'SMP', 'SMA', 'Perguruan Tinggi'], n_samples),
        'penghasilan_keluarga': np.random.choice([1500000, 3500000, 7500000, 15000000], n_samples),
        'status_imunisasi': np.random.choice(['Lengkap', 'Tidak Lengkap'], n_samples, p=[0.8, 0.2]),
    }
    
    df = pd.DataFrame(data)
    
    # Generate stunting status
    conditions = (
        (df['tinggi_badan_cm'] < 70) | 
        (df['asi_eksklusif'] == 'Tidak') |
        (df['pendidikan_ibu'] == 'SD') |
        (df['penghasilan_keluarga'] == 1500000)
    )
    
    df['stunting'] = np.where(conditions, 1, 0)
    # Add some randomness
    mask = np.random.random(n_samples) < 0.1
    df.loc[mask, 'stunting'] = 1 - df.loc[mask, 'stunting']
    
    return df

# ===============================
# STREAMLIT APP
# ===============================
def create_app():
    st.set_page_config(
        page_title="Sistem Deteksi Stunting",
        page_icon="👶",
        layout="wide"
    )

    st.title("👶 SISTEM DETEKSI STUNTING BALITA")
    st.markdown("**Aplikasi Machine Learning untuk Deteksi Dini Stunting**")

    # Generate data
    df = generate_stunting_data()

    # Sidebar
    st.sidebar.title("🎯 NAVIGASI")
    menu = st.sidebar.selectbox("Pilih Menu", [
        "🏠 DASHBOARD", 
        "🔍 PREDIKSI STUNTING"
    ])

    if menu == "🏠 DASHBOARD":
        st.header("📊 Dashboard Overview")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Data Balita", len(df))
        with col2:
            stunting_count = df['stunting'].sum()
            st.metric("Kasus Stunting", stunting_count)
        with col3:
            st.metric("Persentase Stunting", f"{(stunting_count/len(df))*100:.1f}%")
        with col4:
            st.metric("Rata-rata Usia", f"{df['usia_balita_bulan'].mean():.1f} bulan")
        
        # Data Preview
        st.subheader("📋 Preview Data")
        st.dataframe(df.head(10))

    elif menu == "🔍 PREDIKSI STUNTING":
        st.header("🔍 Prediksi Status Stunting")
        
        with st.form("prediction_form"):
            st.subheader("📝 Data Balita")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nama_balita = st.text_input("Nama Balita", "Budi Santoso")
                usia = st.slider("Usia (bulan)", 6, 60, 24)
                berat_badan = st.number_input("Berat Badan (kg)", 5.0, 20.0, 10.0, 0.1)
                tinggi_badan = st.number_input("Tinggi Badan (cm)", 60.0, 120.0, 80.0, 0.1)
                
            with col2:
                jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
                asi_eksklusif = st.selectbox("ASI Eksklusif", ["Ya", "Tidak"])
                pendidikan_ibu = st.selectbox("Pendidikan Ibu", ["SD", "SMP", "SMA", "Perguruan Tinggi"])
                penghasilan = st.selectbox("Penghasilan Keluarga", 
                                         ["Rendah (< 2jt)", "Menengah (2-5jt)", "Tinggi (> 5jt)"])
            
            submitted = st.form_submit_button("🎯 PREDIKSI SEKARANG")
            
            if submitted:
                # Simple prediction logic
                risk_score = 0
                
                if tinggi_badan < 75 and usia > 12:
                    risk_score += 2
                if asi_eksklusif == "Tidak":
                    risk_score += 1
                if pendidikan_ibu == "SD":
                    risk_score += 1
                if penghasilan == "Rendah (< 2jt)":
                    risk_score += 1
                
                # Result
                st.subheader("🎯 HASIL PREDIKSI")
                
                if risk_score >= 3:
                    st.error("🚨 **STATUS: RISIKO STUNTING TINGGI**")
                    st.info("Rekomendasi: Periksa ke puskesmas terdekat")
                elif risk_score >= 1:
                    st.warning("⚠️ **STATUS: RISIKO SEDANG**")
                    st.info("Rekomendasi: Pantau pertumbuhan rutin")
                else:
                    st.success("✅ **STATUS: NORMAL**")
                    st.info("Rekomendasi: Lanjutkan pola asuh baik")

    st.markdown("---")
    st.caption("🔬 Sistem Deteksi Stunting Balita - © 2024")
    
    return st

# Create app instance
app = create_app()

# Untuk Vercel deployment
if __name__ == "__main__":
    # This runs when executed locally
    app.run()