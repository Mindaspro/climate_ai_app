# 📄 1_🌾_Farmer_Input.py
import streamlit as st
import sqlite3
import datetime
from fpdf import FPDF
import tempfile
import pandas as pd

# ====== LOCATION COORDINATE MAP ======
location_coords = {
    "Iyunga, Mbeya": (-8.9391, 33.3953),
    "Inyala, Mbeya": (-8.9662, 33.5590),
    "Mbalizi, Mbeya": (-8.9640, 33.4110),
    "Kyela, Mbeya": (-9.5623, 33.5789),
    "Usangu, Mbeya": (-8.6000, 33.7000),
    "Uyole, Mbeya": (-8.9422, 33.4563),
    "Tukuyu, Mbeya": (-9.2590, 33.6408),
    "Rungwe, Mbeya": (-8.9894, 33.7419)
}

# ====== PDF GENERATION FUNCTION ======
def generate_pdf_report(name, location, crop, prediction):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, "AI Climate Yield Prediction Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Mkulima: {name}", ln=True)
    pdf.cell(200, 10, f"Eneo: {location}", ln=True)
    pdf.cell(200, 10, f"Mzao: {crop}", ln=True)
    pdf.cell(200, 10, f"Mavuno Yanayotarajiwa: {prediction:.2f} kg", ln=True)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_file.name)
    return tmp_file.name

# ====== STREAMLIT FORM ======
st.title("🧑‍🌾 Ingiza Taarifa za Mkulima")

conn = sqlite3.connect("database/climate_yield.db", check_same_thread=False)
c = conn.cursor()

with st.form("farmer_form"):
    name = st.text_input("Jina lako")
    phone = st.text_input("Namba ya simu")
    location = st.selectbox("Chagua eneo lako", list(location_coords.keys()))
    latitude, longitude = location_coords[location]

    st.map(pd.DataFrame({"lat": [latitude], "lon": [longitude]}))

    crop = st.selectbox("Mazao unayolima", ["Mahindi", "Maharage", "Mpunga"])
    size = st.number_input("Ukubwa wa shamba (hekta)", 0.1)
    soil = st.selectbox("Aina ya udongo", ["Tifutifu", "Kichanga", "Mfinyanzi"])
    irrigation = st.radio("Unatumia umwagiliaji?", ["Ndio", "Hapana"]) == "Ndio"
    seed = st.selectbox("Aina ya mbegu", ["Local", "Hybrid"])

    season = st.number_input("Msimu wa kilimo (mwaka)", min_value=2000, max_value=2025)
    plant_date = st.date_input("Tarehe ya kupanda")
    harvest_date = st.date_input("Tarehe ya kuvuna")
    yield_amt = st.number_input("Kiasi cha mazao (kg)", min_value=0.0)

    submitted = st.form_submit_button("👉 Hifadhi Taarifa")

    if submitted:
        # Hifadhi mkulima
        c.execute("""
            INSERT INTO farmers (name, phone, location, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone, location, latitude, longitude))
        farmer_id = c.lastrowid

        # Hifadhi taarifa za kilimo
        c.execute("""
            INSERT INTO farm_data (farmer_id, crop_type, farm_size, soil_type, irrigation,
                        seed_type, season_year, planting_date, harvest_date, yield_obtained)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (farmer_id, crop, size, soil, irrigation, seed, season, plant_date, harvest_date, yield_amt))
        conn.commit()
        st.success("✅ Taarifa zimehifadhiwa kikamilifu!")
