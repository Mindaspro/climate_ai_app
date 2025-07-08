# 📄 3_🤖_Prediction.py
import streamlit as st
import sqlite3
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import os  # For safe path handling

st.title("🤖 Utabiri wa Mavuno kwa Kutumia AI")

# ====== Define base directory and model paths ======
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "yield_predictor.pkl")
COLUMNS_PATH = os.path.join(BASE_DIR, "models", "model_columns.pkl")
DB_PATH = os.path.join(BASE_DIR, "database", "climate_yield.db")

# ====== Load model and columns safely ======
try:
    model = joblib.load(MODEL_PATH)
    model_cols = joblib.load(COLUMNS_PATH)
except FileNotFoundError:
    st.error(
        "⚠️ Hakuna faili la modeli (`yield_predictor.pkl`) au safu (`model_columns.pkl`). "
        "Tafadhali hakikisha yapo kwenye `models/` folder."
    )
    st.stop()

# ====== Connect to SQLite database ======
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()

# ====== Fetch farmers ======
c.execute("SELECT id, name FROM farmers")
farmers = c.fetchall()

if farmers:
    selected = st.selectbox("Chagua mkulima", farmers, format_func=lambda x: x[1])
    farmer_id = selected[0]

    # ====== Fetch latest farm data for the selected farmer ======
    query = """
        SELECT crop_type, farm_size, soil_type, irrigation, seed_type
        FROM farm_data
        WHERE farmer_id = ?
        ORDER BY season_year DESC
        LIMIT 1
    """
    c.execute(query, (farmer_id,))
    farm_info = c.fetchone()

    if farm_info:
        crop, size, soil, irrigation, seed = farm_info

        # ====== Get farmer location ======
        c.execute("SELECT location FROM farmers WHERE id = ?", (farmer_id,))
        location = c.fetchone()[0]

        # ====== Fetch average climate data for current year ======
        climate = pd.read_sql_query(
            """
            SELECT AVG(rainfall) AS rainfall, AVG(temperature) AS temperature
            FROM climate_data
            WHERE location = ? AND year = ?
            """,
            conn,
            params=(location, date.today().year),
        )

        rainfall = climate['rainfall'].values[0] or 600
        temperature = climate['temperature'].values[0] or 25.0

        # ====== Prepare input data for prediction ======
        input_data = pd.DataFrame({
            "crop_type": [crop],
            "farm_size": [size],
            "soil_type": [soil],
            "irrigation": [int(irrigation)],
            "seed_type": [seed],
            "rainfall": [rainfall],
            "temperature": [temperature],
        })

        input_encoded = pd.get_dummies(input_data)
        # Ensure all expected model columns exist in the input, fill missing with zeros
        for col in model_cols:
            if col not in input_encoded:
                input_encoded[col] = 0
        input_encoded = input_encoded[model_cols]

        # ====== Predict yield ======
        prediction = model.predict(input_encoded)[0]

        st.subheader("🔮 Utabiri wa Mavuno")
        st.success(f"Mazao yanayotarajiwa: **{prediction:.2f} kg**")

        st.subheader("📌 Mapendekezo ya AI")
        if temperature > 30:
            st.warning("➡️ Joto ni juu sana mwaka huu. Angalia uwezekano wa upungufu wa maji au panua kipindi cha kupanda.")
        if rainfall < 500:
            st.warning("➡️ Mvua haitoshi – fikiria kutumia mbegu za muda mfupi au umwagiliaji.")

        if crop == "Mahindi":
            st.info("✅ Mbegu bora za kutumia: DK8031, SC513 – hasa kwa ukame.")
        elif crop == "Maharage":
            st.info("✅ Tumia mbegu za SER-16 au Uyole Njano – zinaendana na hali ya Mbeya.")
        elif crop == "Mpunga":
            st.info("✅ Tumia SARO 5 au TXD306 – hasa kwa maeneo ya mvua nyingi au umwagiliaji.")

        # ====== Download input data as CSV ======
        st.download_button(
            "⬇️ Pakua Ripoti ya CSV",
            data=input_data.to_csv(index=False),
            file_name="prediction_input.csv",
            mime='text/csv'
        )

        # ====== Plot Actual vs Predicted yields ======
        past_yields = pd.read_sql_query(
            """
            SELECT season_year, yield_obtained FROM farm_data
            WHERE farmer_id = ? AND crop_type = ?
            """,
            conn,
            params=(farmer_id, crop),
        )

        if not past_yields.empty:
            st.subheader("📊 Mchoro: Mavuno Halisi vs Utabiri")
            years = past_yields['season_year'].tolist()
            actual = past_yields['yield_obtained'].tolist()
            predicted = [prediction] * len(actual)

            fig, ax = plt.subplots()
            ax.plot(years, actual, marker='o', label='Halisi')
            ax.plot(years, predicted, marker='s', linestyle='--', label='Utabiri wa AI')
            ax.set_xlabel("Mwaka")
            ax.set_ylabel("Mavuno (kg)")
            ax.legend()
            st.pyplot(fig)

            avg_actual = np.mean(actual)
            if prediction < avg_actual:
                st.warning(f"📉 Utabiri ni chini ya mavuno ya miaka ya nyuma (wastani: {avg_actual:.2f} kg)")
            else:
                st.success(f"📈 Utabiri ni mzuri ukilinganishwa na historia ya mavuno (wastani: {avg_actual:.2f} kg)")

        # ====== Feature Importance Visualization ======
        st.subheader("📊 Umuhimu wa Vipengele kwenye AI Model")
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            importance_df = pd.DataFrame({
                'Feature': model_cols,
                'Importance': importances
            }).sort_values(by='Importance', ascending=False).head(10)

            fig4, ax4 = plt.subplots()
            ax4.barh(importance_df['Feature'], importance_df['Importance'], color='teal')
            ax4.invert_yaxis()
            ax4.set_title("Vipengele Vinavyoathiri Utabiri Zaidi")
            st.pyplot(fig4)
        else:
            st.info("ℹ️ Model haina vipimo vya feature importance.")

    else:
        st.warning("⛔ Hakuna taarifa za shamba kwa mkulima huyu.")

else:
    st.info("⛔ Hakuna wakulima waliowekwa bado.")
