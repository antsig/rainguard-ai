import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import pydeck as pdk
from datetime import datetime, timedelta
import numpy as np

# API endpoint locally
API_URL = "http://localhost:8000/predict"

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.fetch_bmkg import BMKG_URLS
ALL_REGIONS = list(BMKG_URLS.keys())

# Coordinates for Map (with fallbacks for new provinces)
REGION_COORDS = {
    "DKI Jakarta": {"lat": -6.2088, "lon": 106.8456},
    "Jawa Barat": {"lat": -6.9175, "lon": 107.6191},
    "Jawa Timur": {"lat": -7.2504, "lon": 112.7688},
    "DI Yogyakarta": {"lat": -7.7956, "lon": 110.3695},
    "Jawa Tengah": {"lat": -6.9667, "lon": 110.4167},
    "Bali": {"lat": -8.4095, "lon": 115.1889},
    "Aceh": {"lat": 4.6951, "lon": 96.7494},
    "Sumatera Utara": {"lat": 2.1154, "lon": 99.5451},
    "Sumatera Barat": {"lat": -0.7390, "lon": 100.8000},
    "Riau": {"lat": 0.2933, "lon": 101.7068},
    "Papua": {"lat": -4.2699, "lon": 138.0803},
    "Sulawesi Selatan": {"lat": -4.1449, "lon": 119.9042},
    "Kalimantan Timur": {"lat": 0.5387, "lon": 116.4194}
}
# Fallback center of Indonesia for unspecified coords
DEFAULT_COORD = {"lat": -2.5489, "lon": 118.0149}

# API endpoint locally
API_URL = "http://localhost:8000/predict"

# Sub-districts simulation for richer tooltips
REGION_DISTRICTS = {
    "DKI Jakarta": ["Kebayoran Baru", "Setiabudi", "Cilandak", "Kemang", "Tebet", "Menteng", "Kelapa Gading", "Cengkareng", "Mampang", "Pancoran"],
    "Jawa Barat": ["Coblong", "Cidadap", "Sumur Bandung", "Cicendo", "Andir", "Astanaanyar", "Regol", "Lengkong", "Buahbatu", "Kiaracondong"],
    "Jawa Timur": ["Gubeng", "Wonokromo", "Sawahan", "Tegalsari", "Genteng", "Tambaksari", "Sukolilo", "Rungkut", "Wiyung", "Jambangan"],
    "DI Yogyakarta": ["Gondokusuman", "Jetis", "Danurejan", "Gedongtengen", "Kraton", "Mantrijeron", "Mergangsan", "Umbulharjo", "Kotagede", "Tegalrejo"],
    "Jawa Tengah": ["Semarang Tengah", "Semarang Selatan", "Semarang Barat", "Semarang Timur", "Semarang Utara", "Gajahmungkur", "Candisari", "Tembalang", "Pedurungan", "Banyumanik"]
}


st.set_page_config(page_title="RainGuard AI 🌧️", page_icon="🌧️", layout="wide")

# Custom CSS for aesthetics (glassmorphism & clean UI)
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        /* Let Streamlit handle the main background color automatically */
    }
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #1E88E5, #00ACC1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
        padding-top: 2rem;
    }
    .subtitle {
        text-align: center;
        color: var(--text-color);
        opacity: 0.8;
        font-size: 1.3rem;
        font-weight: 500;
        margin-bottom: 40px;
    }
    
    /* Risk Cards with better contrast and glassmorphism subtle vibes */
    .risk-card {
        padding: 25px; 
        border-radius: 12px; 
        box-shadow: 0 8px 16px rgba(0,0,0,0.1); 
        margin-bottom: 25px;
        text-align: center;
        color: var(--text-color);
    }
    /* Adapting to any theme using transparency */
    .risk-high { background-color: rgba(211, 47, 47, 0.15); border: 1px solid rgba(211, 47, 47, 0.3); border-top: 5px solid #d32f2f; }
    .risk-medium { background-color: rgba(255, 160, 0, 0.15); border: 1px solid rgba(255, 160, 0, 0.3); border-top: 5px solid #ffa000; }
    .risk-low { background-color: rgba(56, 142, 60, 0.15); border: 1px solid rgba(56, 142, 60, 0.3); border-top: 5px solid #388e3c; }
    
    /* Recommendation Cards */
    .recommendation-card { 
        background-color: var(--secondary-background-color); 
        padding: 16px 20px; 
        border-radius: 8px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
        border: 1px solid rgba(128,128,128, 0.2); 
        margin-bottom: 12px; 
        color: var(--text-color);
        font-size: 1.05rem;
        transition: all 0.2s ease-in-out;
    }
    .recommendation-card:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        border-color: #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">RainGuard AI 🌧️</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sistem Peringatan Dini Risiko Banjir Berbasis AI</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Konfigurasi")
region = st.sidebar.selectbox("Pilih Wilayah", ALL_REGIONS)
daysToPredict = st.sidebar.slider("Hari Prediksi", 3, 14, 7)

if st.sidebar.button("Prediksi Risiko Banjir"):
    with st.spinner(f"Mengambil prediksi AI untuk {region}..."):
        try:
            response = requests.post(API_URL, json={"region": region, "days": daysToPredict}, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Top section: status
                risk_today = data['overall_risk_today']
                
                if risk_today == "High":
                    st.markdown(f'<div class="risk-card risk-high"><h2 style="margin:0; padding-bottom:5px;">⚠️ Risiko Banjir Hari Ini: TINGGI</h2><h4 style="margin:0; font-weight:400;">Sistem mendeteksi kemungkinan curah hujan ekstrem. Diperlukan tindakan segera.</h4></div>', unsafe_allow_html=True)
                elif risk_today == "Medium":
                    st.markdown(f'<div class="risk-card risk-medium"><h2 style="margin:0; padding-bottom:5px;">⚠️ Risiko Banjir Hari Ini: SEDANG</h2><h4 style="margin:0; font-weight:400;">Curah hujan sedang diperkirakan. Tetap waspada.</h4></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="risk-card risk-low"><h2 style="margin:0; padding-bottom:5px;">✅ Risiko Banjir Hari Ini: RENDAH</h2><h4 style="margin:0; font-weight:400;">Curah hujan normal. Tidak ada ancaman langsung.</h4></div>', unsafe_allow_html=True)
                
                # Fetch BMKG Output
                bmkg = data.get('bmkg_realtime', {})
                if bmkg and 'error' not in bmkg:
                    st.markdown("### 🌤️ Laporan Cuaca BMKG Terkini")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Cuaca", bmkg.get('weather_desc', 'N/A'))
                    c2.metric("Suhu", f"{bmkg.get('temperature_c', 'N/A')} °C")
                    c3.metric("Kelembapan", f"{bmkg.get('humidity_percent', 'N/A')} %")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Split layout
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader(f"Prakiraan Curah Hujan {daysToPredict} Hari ke Depan")
                    
                    # Prepare dataframe for plotting
                    dates = [datetime.now().date() + timedelta(days=i) for i in range(daysToPredict)]
                    rainfalls = [item['rainfall_mm'] for item in data['forecast']]
                    risks = [item['risk_level'] for item in data['forecast']]
                    
                    df = pd.DataFrame({
                        "Tanggal": dates,
                        "Prediksi Curah Hujan (mm)": rainfalls,
                        "Tingkat Risiko": risks
                    })
                    
                    color_map = {"Low": "green", "Medium": "orange", "High": "red"}
                    fig = px.bar(df, x="Tanggal", y="Prediksi Curah Hujan (mm)", color="Tingkat Risiko", 
                                 color_discrete_map=color_map,
                                 title=f"Prediksi Curah Hujan untuk {region}",
                                 text_auto='.1f')
                    
                    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                                      margin=dict(l=20, r=20, t=40, b=20),
                                      hovermode="x unified")
                                      
                    fig.update_traces(marker_line_width=1.5, opacity=0.8)
                    st.plotly_chart(fig)
                
                with col2:
                    st.subheader("Rekomendasi Tindakan")
                    st.markdown("<br>", unsafe_allow_html=True)
                    for rec in data['recommendations']:
                        st.markdown(f'''
                        <div class="recommendation-card">
                            <span style="color: #00ACC1;">✔</span> <strong>{rec}</strong>
                        </div>
                        ''', unsafe_allow_html=True)

                st.markdown("---")
                st.subheader(f"📍 Peta Genangan Banjir 3D Detail: {region}")
                coords = REGION_COORDS.get(region, DEFAULT_COORD)
                
                # V2 Advanced Map: Setup Topological Spread simulation
                num_points = 800
                spread = 0.04 if risk_today == "High" else (0.02 if risk_today == "Medium" else 0.01)
                
                lats = np.random.normal(coords["lat"], spread, num_points)
                lons = np.random.normal(coords["lon"], spread, num_points)
                districts_pool = REGION_DISTRICTS.get(region, ["Pusat Kota", "Pinggiran", "Barat", "Timur", "Selatan", "Utara"])
                point_districts = np.random.choice(districts_pool, num_points)
                
                map_df = pd.DataFrame({
                    "lat": lats,
                    "lon": lons,
                    "district": point_districts,
                    "weight": np.random.randint(1, 10, num_points)
                })

                # Basic color assignment based on severity
                if risk_today == "High":
                    point_color = [204, 0, 0, 180]
                elif risk_today == "Medium":
                    point_color = [255, 153, 0, 180]
                else:
                    point_color = [0, 153, 0, 180]

                st.pydeck_chart(pdk.Deck(
                    map_style='road',
                    initial_view_state=pdk.ViewState(
                        latitude=coords["lat"],
                        longitude=coords["lon"],
                        zoom=11 if risk_today == "High" else 12,
                        pitch=0,
                    ),
                    layers=[
                        pdk.Layer(
                            'ScatterplotLayer',
                            data=map_df,
                            get_position='[lon, lat]',
                            get_color=point_color,
                            get_radius=250,
                            pickable=True,
                            opacity=0.8
                        )
                    ],
                    tooltip={"html": "<b>Lokasi Genangan:</b> Kecamatan {district} <br/> <b>Koordinat:</b> {lon}, {lat}", "style": {"color": "white"}}
                ))
                        
            else:
                st.error(f"Kesalahan dari API: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("Tidak dapat terhubung ke Backend API. Pastikan server FastAPI sedang berjalan (`uvicorn app.api:app --reload`)")

else:
    # Initial state
    st.info("👈 Pilih wilayah pada panel kiri dan klik 'Prediksi Risiko Banjir' untuk melihat prakiraan cerdas klasifikasi AI.")
    
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>Dibangun menggunakan PyTorch, FastAPI, dan Streamlit untuk tantangan <b>Small Apps for Big Preparedness</b>.</p>", unsafe_allow_html=True)
