import streamlit as st
import pandas as pd
import numpy as np

# Main app function
def main():
    st.set_page_config(
        page_title="Sistem Deteksi Stunting",
        page_icon="👶",
        layout="wide"
    )
    
    st.title("👶 SISTEM DETEKSI STUNTING BALITA")
    st.markdown("**Aplikasi Machine Learning untuk Deteksi Dini Stunting**")
    
    # Simple data generation
    data = {
        'Nama': ['Budi', 'Sari', 'Dimas', 'Rina'],
        'Usia': [24, 18, 30, 12],
        'Tinggi': [78, 75, 82, 70],
        'Status': ['Normal', 'Stunting', 'Normal', 'Stunting']
    }
    df = pd.DataFrame(data)
    
    st.dataframe(df)
    st.success("✅ Aplikasi berjalan di Vercel!")
    
    return st

# Create app instance
app = main()

# For local run
if __name__ == "__main__":
    app.run()