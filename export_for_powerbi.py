"""
export_for_powerbi.py
Exports all PostgreSQL tables as clean CSVs for Power BI.
Run after 04_run_sql_queries.py

FILES EXPORTED to data/processed/:
  powerbi_upi_main.csv          — full monthly time-series (77 rows)
  powerbi_era_summary.csv       — era-level aggregates (4 rows)
  powerbi_p2p_p2m.csv           — P2P vs P2M monthly (41 rows)
  powerbi_npci_products.csv     — payment rail comparison 2024 (120 rows)
  powerbi_jan_dhan.csv          — state-wise financial inclusion (36 rows)
  powerbi_yoy_summary.csv       — year-over-year summary (8 rows)
"""

import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:Shar$12345@localhost/upi_intelligence_db')
print("✓ Connected\n")

exported = []

def export(query, filename, label):
    df = pd.read_sql(query, engine)
    path = f"data/processed/{filename}"
    df.to_csv(path, index=False)
    print(f"  ✓ {label:<30} {len(df):>4} rows → {filename}")
    exported.append(filename)
    return df


# ── 1. FULL UPI MONTHLY ─────────────────────────────────────
export(
    "SELECT * FROM upi_monthly ORDER BY date",
    "powerbi_upi_main.csv",
    "upi_monthly"
)


# ── 2. ERA SUMMARY ──────────────────────────────────────────
export("""
SELECT
    era,
    COUNT(*)                                    AS months,
    ROUND(AVG(volume_crore)::NUMERIC, 0)        AS avg_monthly_volume_crore,
    ROUND(AVG(avg_ticket_size_rs)::NUMERIC, 0)  AS avg_ticket_rs,
    ROUND(AVG(volume_mom_pct)::NUMERIC, 2)      AS avg_mom_growth_pct,
    MIN(date)::DATE                             AS era_start,
    MAX(date)::DATE                             AS era_end
FROM upi_monthly
GROUP BY era
ORDER BY era_start;
""", "powerbi_era_summary.csv", "era_summary")


# ── 3. P2P vs P2M ───────────────────────────────────────────
export(
    "SELECT * FROM upi_p2p_p2m ORDER BY date",
    "powerbi_p2p_p2m.csv",
    "p2p_p2m"
)


# ── 4. NPCI PRODUCT COMPARISON ──────────────────────────────
export(
    "SELECT * FROM npci_products ORDER BY product_name, date",
    "powerbi_npci_products.csv",
    "npci_products"
)


# ── 5. JAN DHAN STATE-WISE ──────────────────────────────────
export(
    "SELECT * FROM jan_dhan_statewise",
    "powerbi_jan_dhan.csv",
    "jan_dhan_statewise"
)


# ── 6. YOY SUMMARY ──────────────────────────────────────────
export("""
SELECT
    year,
    COUNT(*)                                              AS months_of_data,
    ROUND(SUM(volume_crore)::NUMERIC, 0)                  AS total_volume_crore,
    ROUND(SUM(value_crore)::NUMERIC, 0)                   AS total_value_crore,
    ROUND(AVG(avg_ticket_size_rs)::NUMERIC, 0)            AS avg_ticket_size_rs,
    ROUND(AVG(banks_live_on_upi)::NUMERIC, 0)             AS avg_banks_on_upi,
    ROUND(
        (100.0 * (SUM(volume_crore) - LAG(SUM(volume_crore)) OVER (ORDER BY year))
        / NULLIF(LAG(SUM(volume_crore)) OVER (ORDER BY year), 0))::NUMERIC,
    2)                                                    AS yoy_volume_growth_pct
FROM upi_monthly
GROUP BY year
ORDER BY year;
""", "powerbi_yoy_summary.csv", "yoy_summary")


# ── DONE ────────────────────────────────────────────────────
print(f"\n✓ {len(exported)} files exported to data/processed/")
print("  Import these CSVs into Power BI via Get Data → Text/CSV")