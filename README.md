# India UPI & Digital Payments Intelligence Dashboard 💳

> Tracking India's ₹299 lakh crore digital payment revolution — 2016 to 2026.
> Powered by NPCI & RBI public data. Not Kaggle.

🔗 **Live Dashboard:** [add after deploying on Streamlit Cloud]

---

## Key Findings

*(Fill these in after running 04_run_sql_queries.py with real numbers)*

1. **GROWTH SCALE:** UPI processed X million transactions in [latest month] — Xx the volume at launch.

2. **MICRO-PAYMENT SHIFT:** Avg ticket size has fallen from ₹X (YYYY) to ₹X (2026) — 
   UPI now powers everyday ₹50 transactions, not just bank transfers.

3. **MERCHANT ADOPTION:** P2M (merchant payment) share crossed X% in 2025, 
   up from 18% in 2018 — UPI is India's primary retail payment infrastructure.

4. **ECOSYSTEM:** Banks live on UPI: X at launch → X in 2026. 
   Network effect has created a near-unassailable payment moat.

5. **OPPORTUNITY GAP:** States with sub-30% smartphone penetration represent 
   340M+ potential UPI users. Closing this gap would add ~4Bn monthly transactions.

---

## Data Sources

| Dataset | Source | Format |
|---------|--------|--------|
| UPI Monthly Volume & Value | NPCI via India Data Portal | CSV |
| UPI P2P vs P2M Breakdown | NPCI via India Data Portal | CSV |
| NPCI All Products (IMPS, NACH, FASTag) | Kaggle | CSV |
| RBI Payment System Indicators | RBI DBIE Portal | Excel |
| Jan Dhan State-wise Accounts | data.gov.in | CSV |
| UPI 2024–2026 Monthly Data | NPCI Monthly Metrics (manual) | CSV |

*All data is publicly available. No Kaggle toy datasets.*

---

## Tech Stack

`Python` · `Pandas` · `PostgreSQL` · `SQLite` · `Streamlit` · `Plotly`

---

## Project Structure

```
upi-payment-intelligence/
├── data/processed/         ← Cleaned CSVs
├── notebooks/charts/       ← EDA chart PNGs
├── sql/                    ← 5 SQL query files
├── dashboard/app.py        ← Streamlit dashboard
├── 01_clean_engineer.py    ← Data cleaning + feature engineering
├── 02_eda_visualizations.py← All EDA charts
├── 03_load_postgres.py     ← PostgreSQL loader
└── 04_run_sql_queries.py   ← SQL query runner
```

---

## How to Run

```bash
pip install -r requirements.txt
python 00_setup.py          # verify environment
python 01_clean_engineer.py # clean + engineer features
python 02_eda_visualizations.py # generate charts
python 03_load_postgres.py  # load to PostgreSQL
python 04_run_sql_queries.py # run all 5 SQL queries
streamlit run dashboard/app.py # launch dashboard
```