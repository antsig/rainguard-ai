import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import pydeck as pdk
from datetime import datetime, timedelta

# API endpoint locally
API_URL = "http://localhost:8000/predict"

# Coordinates for Map
REGION_COORDS = {
    "Jakarta": {"lat": -6.2088, "lon": 106.8456},
    "Bandung": {"lat": -6.9175, "lon": 107.6191},
    "Surabaya": {"lat": -7.2504, "lon": 112.7688},
    "Yogyakarta": {"lat": -7.7956, "lon": 110.3695},
    "Semarang": {"lat": -6.9667, "lon": 110.4167}
}

# API endpoint locally
API_URL = "http://localhost:8000/predict"

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
region = st.sidebar.selectbox("Pilih Wilayah", ["Jakarta", "Bandung", "Surabaya", "Yogyakarta", "Semarang"])
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
                st.subheader(f"📍 Peta Risiko Banjir Interaktif: {region}")
                coords = REGION_COORDS[region]
                
                # Assign color based on exact risk level
                if risk_today == "High":
                    map_color = [204, 0, 0, 200]
                elif risk_today == "Medium":
                    map_color = [255, 193, 7, 200]
                else:
                    map_color = [40, 167, 69, 200]
                    
                map_df = pd.DataFrame([{
                    "lat": coords["lat"],
                    "lon": coords["lon"],
                    "risk": risk_today
                }])

                st.pydeck_chart(pdk.Deck(
                    map_style=None,
                    initial_view_state=pdk.ViewState(
                        latitude=coords["lat"],
                        longitude=coords["lon"],
                        zoom=10,
                        pitch=45,
                    ),
                    layers=[
                        pdk.Layer(
                            'ScatterplotLayer',
                            data=map_df,
                            get_position='[lon, lat]',
                            get_color=map_color,
                            get_radius=4000,
                            pickable=True
                        )
                    ]
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
