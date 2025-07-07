# 📄 populate_test_data.py
# Run this once to insert sample farmer, farm, and climate data for testing

import sqlite3

conn = sqlite3.connect("database/climate_yield.db")
c = conn.cursor()

# ✅ 1. Add a sample farmer
c.execute("""
    INSERT INTO farmers (name, phone, location, latitude, longitude)
    VALUES (?, ?, ?, ?, ?)
""", ("Joseph Mindas", "+255700000000", "Kyela, Mbeya", -9.5623, 33.5789))
farmer_id = c.lastrowid

# ✅ 2. Add farm data for that farmer
farm_data = [
    (farmer_id, "Mahindi", 1.2, "Tifutifu", 1, "Hybrid", 2020, "2020-12-01", "2021-04-01", 1050),
    (farmer_id, "Mpunga", 1.5, "Mfinyanzi", 1, "Hybrid", 2021, "2021-11-20", "2022-03-15", 1300),
    (farmer_id, "Maharage", 1.0, "Kichanga", 0, "Local", 2022, "2022-12-01", "2023-03-01", 800)
]

c.executemany("""
    INSERT INTO farm_data (farmer_id, crop_type, farm_size, soil_type, irrigation, seed_type, season_year, planting_date, harvest_date, yield_obtained)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", farm_data)

# ✅ 3. Add climate data for Kyela, Mbeya
climate_data = [
    ("Kyela, Mbeya", 2020, 820, 24.8),
    ("Kyela, Mbeya", 2021, 910, 25.6),
    ("Kyela, Mbeya", 2022, 880, 26.2),
    ("Kyela, Mbeya", 2023, 640, 30.5)
]

c.executemany("""
    INSERT INTO climate_data (location, year, rainfall, temperature)
    VALUES (?, ?, ?, ?)
""", climate_data)

conn.commit()
conn.close()
print("✅ Sample data inserted successfully!")