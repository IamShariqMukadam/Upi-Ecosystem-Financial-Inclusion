"""
06_run_inclusion_analysis.py
Loads financial inclusion gap CSV to PostgreSQL and runs the SQL query.
Run after 05_financial_inclusion_gap.py

ADDS TABLE: financial_inclusion_gap (36 rows)
RUNS QUERY: 06_financial_inclusion_gap.sql
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os

DB_CONFIG = {
    "user":     "postgres",
    "password": "Shar$12345",
    "host":     "localhost",
    "port":     "5432",
    "database": "upi_intelligence_db",
}
CONN = (f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")

engine = create_engine(CONN)
print("✓ Connected\n")

# ── LOAD TABLE ───────────────────────────────────────────────
df = pd.read_csv("data/processed/financial_inclusion_gap.csv")
df.to_sql("financial_inclusion_gap", engine, if_exists='replace', index=False)
with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM financial_inclusion_gap")).scalar()
print(f"  ✓ financial_inclusion_gap: {count} rows loaded")

# ── ALSO EXPORT FOR POWER BI ─────────────────────────────────
df.to_csv("data/processed/powerbi_inclusion_gap.csv", index=False)
print(f"  ✓ powerbi_inclusion_gap.csv saved ({len(df)} rows)")

# ── RUN SQL QUERY ────────────────────────────────────────────
print(f"\n{'='*55}")
print("QUERY: 06_financial_inclusion_gap")
print('='*55)

# Note: jan_dhan_statewise column name in DB may have different naming
# Using financial_inclusion_gap table directly
sql = """
SELECT
    state,
    accounts,
    deposit_crore,
    deposit_per_account_rs,
    national_avg_rs,
    gap_vs_national_avg_rs,
    gap_crore,
    pct_of_national_avg,
    account_share_pct,
    CASE
        WHEN gap_crore > 0 THEN 'Digitally Underserved'
        ELSE 'Above National Average'
    END AS inclusion_status,
    CASE
        WHEN gap_crore > 2000  THEN 'Critical Gap'
        WHEN gap_crore > 500   THEN 'High Gap'
        WHEN gap_crore > 0     THEN 'Moderate Gap'
        ELSE 'No Gap'
    END AS gap_severity
FROM financial_inclusion_gap
ORDER BY gap_crore DESC;
"""

result = pd.read_sql(sql, engine)
print(result.to_string(index=False))
result.to_csv("data/processed/sql_06_financial_inclusion_gap.csv", index=False)
print(f"\n  ✓ Saved data/processed/sql_06_financial_inclusion_gap.csv")

# ── SUMMARY ─────────────────────────────────────────────────
below = result[result['gap_crore'] > 0]
print(f"\n{'='*55}")
print("SUMMARY")
print(f"{'='*55}")
print(f"  Underserved states  : {len(below)}")
print(f"  Total accounts      : {below['accounts'].sum():,}")
print(f"  Total gap           : ₹{below['gap_crore'].sum():,.0f} Crore")
print(f"\n  Critical gap states:")
for _, row in result[result['gap_crore'] > 2000].iterrows():
    print(f"    {row['state']:<20} ₹{row['gap_crore']:,.0f} Cr gap | "
          f"only {row['pct_of_national_avg']:.0f}% of national avg")

print("\n✓ Done. Add powerbi_inclusion_gap.csv to Power BI as Page 4.")