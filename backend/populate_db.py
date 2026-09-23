import os, sys, json, sqlite3
sys.path.insert(0, '.')
from backend.static_data import ROUTE_WEIGHTS, HORIZONS, BASE_FARES, SELECTED_PAIRS
from backend.pipeline import process_pipeline

db_path = "backend/apix_data.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Create tables
cur.executescript("""
CREATE TABLE IF NOT EXISTS raw_fares (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    route_id TEXT NOT NULL,
    airline TEXT NOT NULL,
    flight_number TEXT,
    travel_date TEXT NOT NULL,
    lead_time_horizon TEXT NOT NULL,
    cabin_class TEXT NOT NULL,
    total_fare REAL NOT NULL,
    query_date TEXT,
    source TEXT
);

CREATE TABLE IF NOT EXISTS route_weights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id TEXT UNIQUE NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    passenger_share REAL NOT NULL,
    passenger_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS representative_fares (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id TEXT NOT NULL,
    lead_time_horizon TEXT NOT NULL,
    cabin_class TEXT NOT NULL,
    base_fare REAL NOT NULL,
    representative_fare REAL NOT NULL,
    price_relative REAL NOT NULL,
    pct_change REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS apix_index_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    horizon TEXT NOT NULL,
    index_value REAL NOT NULL,
    calculated_at TEXT NOT NULL
);
""")

# 2. Insert raw fares
with open("raw_scraped_fares.json", "r", encoding="utf-8") as f:
    fares = json.load(f)

cur.execute("DELETE FROM raw_fares")
for r in fares:
    cur.execute("""
        INSERT INTO raw_fares (origin, destination, route_id, airline, flight_number, travel_date, lead_time_horizon, cabin_class, total_fare, query_date, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        r["origin"], r["destination"], r["route_id"], r["airline"],
        r.get("flight_number", ""), r["travel_date"], r["lead_time_horizon"],
        r["cabin_class"], r["total_fare"], r.get("query_date", ""), r.get("source", "")
    ))

# 3. Insert route weights
cur.execute("DELETE FROM route_weights")
for orig, dest in SELECTED_PAIRS:
    rid = f"{orig}-{dest}"
    w = ROUTE_WEIGHTS.get(rid, 0.0125)
    cnt = int(w * 150_000_000)
    cur.execute("""
        INSERT OR REPLACE INTO route_weights (route_id, origin, destination, passenger_share, passenger_count)
        VALUES (?, ?, ?, ?, ?)
    """, (rid, orig, dest, round(w, 6), cnt))

# 4. Compute pipeline and insert representative fares & index
pipeline_res = process_pipeline(fares)
rep_df = pipeline_res["rep_fares"]

cur.execute("DELETE FROM representative_fares")
for _, row in rep_df.iterrows():
    cur.execute("""
        INSERT INTO representative_fares (route_id, lead_time_horizon, cabin_class, base_fare, representative_fare, price_relative, pct_change)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        row["route_id"], row["lead_time_horizon"], row.get("cabin_class", "Economy"),
        row["base_fare"], row["representative_fare"], row["price_relative"], row["pct_change"]
    ))

# 5. Insert APIx Index
cur.execute("DELETE FROM apix_index_history")
for h, val in pipeline_res["apix_index"].items():
    cur.execute("""
        INSERT INTO apix_index_history (horizon, index_value, calculated_at)
        VALUES (?, ?, datetime('now'))
    """, (h, val))

conn.commit()
print("Populated backend/apix_data.db successfully!")

# Copy also to apix.db in root
import shutil
shutil.copyfile("backend/apix_data.db", "apix.db")
print("Synced to root apix.db")

conn.close()
