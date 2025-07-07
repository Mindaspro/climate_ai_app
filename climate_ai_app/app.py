# 📁 File: app.py
import streamlit as st
from utils import set_background

st.set_page_config(page_title="AI Crop Yield App", page_icon="🌾", layout="wide")
set_background("https://images.unsplash.com/photo-1598511726255-e6f0490f3c5e")

st.title("🌾 Karibu kwenye Mfumo wa AI wa Utabiri wa Mavuno")

col1, col2 = st.columns(2)

with col1:
    st.image("images/ads_banner.jpg", use_container_width=True)
    st.markdown("""
    #### 🤖 Mradi huu unasaidia:
    - Wakulima kupata utabiri wa mavuno
    - Tathmini ya mabadiliko ya tabianchi
    - Ushauri wa aina ya mazao na mbegu
    
    """)

with col2:
    st.image("images/farmer_banner.jpg", use_container_width=True)

st.markdown("---")

st.markdown("### 🔗 Tembelea kurasa zingine")

card1, card2, card3 = st.columns(3)

with card1:
    st.markdown("""
    <div style='padding: 20px; border-radius: 12px; background-color: #f0f8ff; text-align: center; box-shadow: 2px 2px 6px rgba(0,0,0,0.1);'>
        <h2>🧑‍🌾</h2>
        <p><strong>Ingiza Taarifa</strong></p>
        <a href="/pages/1_🌾_Farmer_Input" target="_self"><button style='padding: 8px 16px; border-radius: 8px; background-color: #4CAF50; color: white; border: none;'>Fungua</button></a>
    </div>
    """, unsafe_allow_html=True)

with card2:
    st.markdown("""
    <div style='padding: 20px; border-radius: 12px; background-color: #f0fff0; text-align: center; box-shadow: 2px 2px 6px rgba(0,0,0,0.1);'>
        <h2>📈</h2>
        <p><strong>Tathmini ya Tabianchi</strong></p>
        <a href="/pages/2_📈_Assessment_Report" target="_self"><button style='padding: 8px 16px; border-radius: 8px; background-color: #2196F3; color: white; border: none;'>Fungua</button></a>
    </div>
    """, unsafe_allow_html=True)

with card3:
    st.markdown("""
    <div style='padding: 20px; border-radius: 12px; background-color: #fff5ee; text-align: center; box-shadow: 2px 2px 6px rgba(0,0,0,0.1);'>
        <h2>🤖</h2>
        <p><strong>Utabiri wa Mavuno</strong></p>
        <a href="/pages/3_🤖_Prediction" target="_self"><button style='padding: 8px 16px; border-radius: 8px; background-color: #FF9800; color: white; border: none;'>Fungua</button></a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### 🔗 Tembelea kurasa zingine")
st.page_link("pages/1_🌾_Farmer_Input.py", label="🧑‍🌾 Ingiza Taarifa za Mkulima")
st.page_link("pages/2_📈_Assessment_Report.py", label="📈 Tathmini ya Tabianchi")
st.page_link("pages/3_🤖_Prediction.py", label="🤖 Utabiri wa Mavuno")

with st.sidebar:
    st.image("images/min_agri_logo.png", width=120)
    st.image("images/uyole_logo.png", width=120)
    st.markdown("""
    #### 📞 Mawasiliano:
    - Simu: +255 753 109 181
    - Email: josephmindas98@gmail.com
    """)
