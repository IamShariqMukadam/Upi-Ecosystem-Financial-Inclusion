"""
04_run_sql_queries.py
Runs all 5 SQL queries and prints results.
Run after 03_load_postgres.py
"""

import pandas as pd
from sqlalchemy import create_engine
import os

DB_CONFIG = {
    "user":     "postgres",
    "password": "Shar$12345",
    "host":     "localhost",
    "port":     "5432",
    "database": "upi_intelligence_db",
}
CONN = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)
engine = create_engine(CONN)
print("✓ Connected to PostgreSQL\n")
os.makedirs("data/processed", exist_ok=True)

queries = {}

# Q1 — Fix: cast entire window expression to ::NUMERIC before ROUND
queries['01_yoy_performance'] = """
SELECT
    year,
    COUNT(*)                                               AS months_of_data,
    ROUND(SUM(volume_crore)::NUMERIC, 0)                   AS total_volume_crore,
    ROUND(SUM(value_crore)::NUMERIC, 0)                    AS total_value_crore,
    ROUND(AVG(avg_ticket_size_rs)::NUMERIC, 0)             AS avg_ticket_size_rs,
    ROUND(AVG(banks_live_on_upi)::NUMERIC, 0)              AS avg_banks_on_upi,
    ROUND(
        (100.0 * (SUM(volume_crore) - LAG(SUM(volume_crore)) OVER (ORDER BY year))
        / NULLIF(LAG(SUM(volume_crore)) OVER (ORDER BY year), 0))::NUMERIC,
    2)                                                     AS yoy_volume_growth_pct
FROM upi_monthly
GROUP BY year
ORDER BY year;
"""

# Q2 — Fix: cast LAG subtraction expression to ::NUMERIC before ROUND
queries['02_p2p_vs_p2m_shift'] = """
SELECT
    DATE_TRUNC('year', date)::DATE                         AS year,
    COUNT(*)                                               AS months,
    ROUND(AVG(p2m_share_pct)::NUMERIC, 2)                  AS avg_p2m_share_pct,
    ROUND(MIN(p2m_share_pct)::NUMERIC, 2)                  AS min_p2m_share_pct,
    ROUND(MAX(p2m_share_pct)::NUMERIC, 2)                  AS max_p2m_share_pct,
    ROUND(
        (AVG(p2m_share_pct)
        - LAG(AVG(p2m_share_pct)) OVER (ORDER BY DATE_TRUNC('year', date)))::NUMERIC,
    2)                                                     AS p2m_share_yoy_change
FROM upi_p2p_p2m
GROUP BY DATE_TRUNC('year', date)
ORDER BY year;
"""

# Q3 — Fix: cast entire percentage expression to ::NUMERIC before ROUND
queries['03_bank_adoption_rate'] = """
SELECT
    year,
    MIN(banks_live_on_upi)                                 AS banks_at_year_start,
    MAX(banks_live_on_upi)                                 AS banks_at_year_end,
    MAX(banks_live_on_upi) - MIN(banks_live_on_upi)        AS banks_added_in_year,
    ROUND(
        (100.0 * (MAX(banks_live_on_upi) - MIN(banks_live_on_upi))
        / NULLIF(MIN(banks_live_on_upi), 0))::NUMERIC,
    2)                                                     AS bank_growth_pct
FROM upi_monthly
WHERE banks_live_on_upi IS NOT NULL
GROUP BY year
ORDER BY year;
"""

# Q4 — unchanged, already working
queries['04_payment_mode_comparison'] = """
SELECT
    product_name,
    year,
    COUNT(*)                                               AS months,
    ROUND(SUM(volume_mn)::NUMERIC, 2)                      AS total_volume_mn,
    ROUND(AVG(volume_mn)::NUMERIC, 2)                      AS avg_monthly_volume_mn,
    ROUND(MAX(volume_mn)::NUMERIC, 2)                      AS peak_monthly_volume_mn,
    RANK() OVER (
        PARTITION BY year
        ORDER BY SUM(volume_mn) DESC
    )                                                      AS rank_by_volume
FROM npci_products
GROUP BY product_name, year
ORDER BY year, rank_by_volume;
"""

# Q5 — unchanged, already working
queries['05_ticket_size_era_analysis'] = """
SELECT
    era,
    COUNT(*)                                               AS months,
    ROUND(AVG(volume_crore)::NUMERIC, 0)                   AS avg_monthly_volume_crore,
    ROUND(AVG(avg_ticket_size_rs)::NUMERIC, 0)             AS avg_ticket_rs,
    ROUND(MIN(avg_ticket_size_rs)::NUMERIC, 0)             AS min_ticket_rs,
    ROUND(MAX(avg_ticket_size_rs)::NUMERIC, 0)             AS max_ticket_rs,
    ROUND(AVG(volume_mom_pct)::NUMERIC, 2)                 AS avg_mom_growth_pct,
    MIN(date)::DATE                                        AS era_start,
    MAX(date)::DATE                                        AS era_end,
    CASE
        WHEN AVG(avg_ticket_size_rs) > 1500 THEN 'High-Value Transfer Dominant'
        WHEN AVG(avg_ticket_size_rs) BETWEEN 1000 AND 1500 THEN 'Transition / Mixed Use'
        WHEN AVG(avg_ticket_size_rs) < 1000  THEN 'Micro-Payment Era'
    END                                                    AS payment_regime
FROM upi_monthly
GROUP BY era
ORDER BY era_start;
"""

for name, sql in queries.items():
    print(f"\n{'='*55}")
    print(f"QUERY: {name}")
    print('='*55)
    try:
        df = pd.read_sql(sql, engine)
        print(df.to_string(index=False))
        df.to_csv(f"data/processed/sql_{name}.csv", index=False)
        print(f"  ✓ Saved data/processed/sql_{name}.csv")
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\n" + "=" * 55)
print("✓ All 5 SQL queries complete.")
print("  Day 1 DONE. Start Streamlit dashboard (Day 2) next.")
print("=" * 55)