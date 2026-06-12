"""
03_load_postgres.py
Loads all processed CSVs into PostgreSQL.
Run after 02_eda_visualizations.py

TABLES LOADED:
  - upi_monthly         (77 rows — primary time-series)
  - upi_p2p_p2m         (41 rows — P2P vs P2M breakdown)
  - jan_dhan_statewise  (36 rows — state-wise inclusion data)
  - npci_products       (36 rows — AePS product comparison, 2024)

BEFORE RUNNING: update DB_CONFIG below.
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os

# ── CONFIG ─────────────────────────────────────────────────
DB_CONFIG = {
    "user":     "postgres",
    "password": "Shar$12345",   # ← change this
    "host":     "localhost",
    "port":     "5432",
    "database": "upi_intelligence_db",
}
CONN = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# ── CONNECT ─────────────────────────────────────────────────
print("Connecting to PostgreSQL...")
try:
    engine = create_engine(CONN)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("  ✓ Connected")
except Exception as e:
    print(f"  ✗ Failed: {e}")
    print("\n  Checklist:")
    print("  1. Is PostgreSQL running? (pgAdmin / services)")
    print("  2. Did you create the DB?  CREATE DATABASE upi_intelligence_db;")
    print("  3. Is the password correct in DB_CONFIG?")
    raise


# ── HELPER ──────────────────────────────────────────────────
def load_table(filepath, table_name, engine, date_cols=None):
    if not os.path.exists(filepath):
        print(f"  ✗ Skipped {table_name} — not found: {filepath}")
        return
    df = pd.read_csv(filepath)
    if date_cols:
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    with engine.connect() as conn:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
    print(f"  ✓ {table_name:<25} {count:>5} rows")


# ── LOAD ────────────────────────────────────────────────────
print("\nLoading tables...")
load_table("data/processed/upi_clean.csv",        "upi_monthly",        engine, ['date'])
load_table("data/processed/p2p_p2m_clean.csv",    "upi_p2p_p2m",        engine, ['date'])
load_table("data/processed/jan_dhan_clean.csv",   "jan_dhan_statewise", engine)
load_table("data/processed/npci_products_clean.csv", "npci_products",   engine, ['date'])


# ── VERIFY: schema of main table ────────────────────────────
print("\n--- upi_monthly schema ---")
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'upi_monthly'
        ORDER BY ordinal_position;
    """))
    for row in result:
        print(f"  {row[0]:<35} {row[1]}")


# ── QUICK TEST ───────────────────────────────────────────────
print("\n--- Quick test: YoY summary ---")
df_test = pd.read_sql("""
    SELECT year,
           COUNT(*) AS months,
           ROUND(SUM(volume_crore)::NUMERIC, 0) AS total_vol_crore,
           ROUND(AVG(avg_ticket_size_rs)::NUMERIC, 0) AS avg_ticket_rs
    FROM upi_monthly
    GROUP BY year ORDER BY year;
""", engine)
print(df_test.to_string(index=False))

print("\n✓ PostgreSQL loaded. Run 04_run_sql_queries.py next.")