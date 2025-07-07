import sqlite3

# Connect to the database file (will create it if it doesn't exist)
conn = sqlite3.connect("database/climate_yield.db")
c = conn.cursor()

# Create farmers table
c.execute("""
CREATE TABLE IF NOT EXISTS farmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    location TEXT,
    latitude REAL,
    longitude REAL
)
""")

# Create farm_data table
c.execute("""
CREATE TABLE IF NOT EXISTS farm_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    crop_type TEXT,
    farm_size REAL,
    soil_type TEXT,
    irrigation BOOLEAN,
    seed_type TEXT,
    season_year INTEGER,
    planting_date TEXT,
    harvest_date TEXT,
    yield_obtained REAL,
    FOREIGN KEY (farmer_id) REFERENCES farmers(id)
)
""")

# Create climate_data table
c.execute("""
CREATE TABLE IF NOT EXISTS climate_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    year INTEGER,
    rainfall REAL,
    temperature REAL
)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully.")