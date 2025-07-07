import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk

st.title("📈 Tathmini ya Mabadiliko ya Tabianchi")

conn = sqlite3.connect("database/climate_yield.db", check_same_thread=False)
c = conn.cursor()

# Chagua mkulima kwa jina au namba
c.execute("SELECT id, name FROM farmers")
farmers = c.fetchall()

if farmers:
    selected = st.selectbox("Chagua mkulima", farmers, format_func=lambda x: x[1])
    farmer_id = selected[0]

    # Taarifa za kilimo
    farm_df = pd.read_sql_query(f"""
        SELECT season_year, crop_type, yield_obtained
        FROM farm_data WHERE farmer_id = {farmer_id}
    """, conn)

    # Location ya mkulima
    c.execute("SELECT location, latitude, longitude FROM farmers WHERE id = ?", (farmer_id,))
    location_data = c.fetchone()
    location = location_data[0]
    latitude = location_data[1]
    longitude = location_data[2]

    # Taarifa za hali ya hewa kwa eneo lake
    climate_df = pd.read_sql_query("""
      SELECT year, rainfall, temperature
      FROM climate_data
      WHERE location = ?
    """, conn, params=(location,))

    # Wastani wa hali ya hewa
    rainfall = climate_df["rainfall"].mean()
    temperature = climate_df["temperature"].mean()

    st.markdown("### 📊 Muhtasari wa Tabianchi")
    st.markdown(f"""
    Katika eneo la **{location}**, wastani wa hali ya hewa kwa kipindi kilichopita ni:
    - 🌧️ Mvua: **{rainfall:.1f} mm**
    - 🌡️ Joto: **{temperature:.1f}°C**
    """)

    if rainfall < 500:
        st.warning("⚠️ Mvua ilikuwa ndogo – kuna hatari ya ukame na mavuno kidogo.")
    elif rainfall > 900:
        st.info("🌧️ Mvua ilikuwa nyingi – mazao kama mpunga yanaweza kufaidika.")
    else:
        st.success("✅ Mvua ilikuwa ya wastani – hali nzuri kwa mazao mengi.")

    if temperature > 30:
        st.warning("🔥 Joto lilikuwa juu – angalia uwezekano wa ukame au kuharibu mbegu.")
    elif temperature < 18:
        st.warning("❄️ Joto la chini linaweza kuchelewesha ukuaji wa mimea.")
    else:
        st.success("🌤️ Joto la wastani linasaidia ukuaji wa mimea.")

    # Ramani ya eneo la mkulima
    if latitude and longitude:
        st.markdown("### 🗺️ Ramani ya Shamba la Mkulima")
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=latitude,
                longitude=longitude,
                zoom=10,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=pd.DataFrame({"lat": [latitude], "lon": [longitude]}),
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200,
                ),
            ],
        ))

    # Graph: Mvua kwa miaka au Jedwali
    view = st.radio("🔀 Chagua namna ya kuona taarifa za mvua", ["📈 Mchoro", "📋 Jedwali"])
    if view == "📋 Jedwali":
        st.dataframe(climate_df[["year", "rainfall"]])
    else:
        st.write("🌧️ Mvua (mm) kwa kila mwaka")
        fig1, ax1 = plt.subplots()
        ax1.plot(climate_df['year'], climate_df['rainfall'], marker='o', color='blue')
        ax1.set_xlabel("Mwaka")
        ax1.set_ylabel("Mvua (mm)")
        st.pyplot(fig1)

    # Graph: Joto kwa miaka
    st.write("🔥 Joto la Wastani kwa kila mwaka")
    fig2, ax2 = plt.subplots()
    ax2.plot(climate_df['year'], climate_df['temperature'], marker='s', color='red')
    ax2.set_xlabel("Mwaka")
    ax2.set_ylabel("Joto (°C)")
    st.pyplot(fig2)

    # Graph: Ukame (ikiwa ipo)
    if "drought" in climate_df.columns:
        st.write("⚠️ Miaka yenye Ukame")
        drought_years = climate_df[climate_df['drought'] == 1]['year'].tolist()
        if drought_years:
            st.warning("Miaka yenye ukame: " + ", ".join(map(str, drought_years)))
        else:
            st.success("✅ Hakuna ukame ulioripotiwa kwa miaka hii.")

    # Graph: Mavuno ya mkulima
    st.write("🌾 Mavuno kwa kila mwaka wa kilimo")
    fig3, ax3 = plt.subplots()
    for crop in farm_df['crop_type'].unique():
        crop_data = farm_df[farm_df['crop_type'] == crop]
        ax3.plot(crop_data['season_year'], crop_data['yield_obtained'], marker='^', label=crop)
    ax3.set_xlabel("Mwaka wa Kilimo")
    ax3.set_ylabel("Mavuno (kg)")
    ax3.legend()
    st.pyplot(fig3)

    # Chart interpretation based on correlation
    merged_df = pd.merge(farm_df, climate_df, left_on="season_year", right_on="year", how="inner")
    if not merged_df.empty:
        correlation_rain = merged_df["rainfall"].corr(merged_df["yield_obtained"])
        correlation_temp = merged_df["temperature"].corr(merged_df["yield_obtained"])

        st.markdown("### 🧠 Ufafanuzi wa Mahusiano ya Takwimu")
        if correlation_rain < -0.3:
            st.warning("📉 Kuna uhusiano hasi kati ya mvua na mavuno. Inawezekana mvua nyingi sana inaharibu mavuno.")
        elif correlation_rain > 0.3:
            st.success("🌧️ Kuna uhusiano chanya kati ya mvua na mavuno. Mvua zaidi huongeza mavuno.")
        else:
            st.info("ℹ️ Hakuna uhusiano mkubwa kati ya mvua na mavuno kwa data zilizopo.")

        if correlation_temp < -0.3:
            st.warning("🥵 Joto la juu linaonekana kupunguza mavuno kwa miaka iliyopita.")
        elif correlation_temp > 0.3:
            st.success("🌡️ Joto linaweza kusaidia ukuaji kama halizidi mipaka.")
        else:
            st.info("ℹ️ Hakuna uhusiano mkubwa kati ya joto na mavuno kwa data zilizopo.")

        st.markdown("### 🤖 Mapendekezo ya AI")
        if correlation_rain < -0.3 and rainfall > 900:
            st.warning("➡️ Fikiria kutumia mbegu zinazostahimili mvua nyingi au kurekebisha ratiba ya kupanda.")
        if correlation_rain > 0.3 and rainfall < 600:
            st.info("➡️ Tumia umwagiliaji au mbegu za muda mfupi kuongeza mavuno.")
        if correlation_temp > 0.3 and temperature > 30:
            st.warning("➡️ Tumia kivuli cha mimea au panda mapema ili kuepuka joto kali la baadaye.")

    # Export button
    st.markdown("### ⬇️ Pakua Taarifa")
    st.download_button("Pakua Taarifa ya Tabianchi (CSV)", climate_df.to_csv(index=False), file_name="climate_report.csv", mime="text/csv")

else:
    st.info("⛔ Hakuna wakulima waliowekwa bado.")
