<div align="center">

# 🇮🇳 UPI Payment Intelligence

### India's ₹2.95 Lakh Crore digital payment revolution — decoded.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Data](https://img.shields.io/badge/Source-RBI%20%7C%20NPCI-orange?style=for-the-badge)
![Coverage](https://img.shields.io/badge/Coverage-Nov%202019–Mar%202026-green?style=for-the-badge)

*Real government data. No Kaggle toy datasets. No made-up numbers.*

</div>

---

## 📊 Dashboard — 3 Pages, 10 Visuals, 1 Story

| 🚀 Growth Story | 🏦 Ecosystem Health | 🧠 Payment Intelligence |
|:---:|:---:|:---:|
| ![Page 1](dashboard/screenshots/page1_growth.png) | ![Page 2](dashboard/screenshots/page2_ecosystem.png) | ![Page 3](dashboard/screenshots/page3_intelligence.png) |
| Volume growth by era | Bank network expansion | Seasonality & micro-payment shift |

<div align="center">

### 🔗 [View Live Interactive Dashboard →](your-powerbi-link-here)

</div>

---

## ⚡ The Numbers That Matter

<div align="center">

| | | | |
|:---:|:---:|:---:|:---:|
| **19x** | **₹1,304** | **271.7 Bn** | **58.5%** |
| Volume growth since 2019 | Avg ticket size Mar 2026 | Annual txn run rate | P2M merchant share |
| **2,264 Cr** | **684** | **458.9 Mn** | **+647%** |
| Monthly txns Mar 2026 | Banks on UPI | Jan Dhan accounts | 2020 YoY growth |

</div>

---

## 🔍 What The Data Actually Says

### 📈 Finding 1 — The Growth Is Unprecedented
```
Nov 2019  ████░░░░░░░░░░░░░░░░░░░░░░░░░░  121.88 Cr/month
2021      ████████░░░░░░░░░░░░░░░░░░░░░░  322.28 Cr/month
2023      ████████████████░░░░░░░░░░░░░░  980.10 Cr/month
Mar 2026  ██████████████████████████████  2,264.11 Cr/month  ← 19x
```
UPI added more transactions in 2025 alone than it processed in its first 3 years combined.

---

### 😷 Finding 2 — COVID Was a Catalyst, Not a Crisis
> *"Every other industry crashed in 2020. UPI grew 647%."*

When India locked down in Mar 2020, cash became dangerous. UPI became essential.
- Avg ticket size **peaked at ₹1,959 in Jun 2020** — people moved rent, bulk groceries, family transfers online
- **2020: +647.1% YoY** — the largest annual jump in UPI history
- **2021: +105.1% YoY** — momentum didn't stop when lockdowns ended

---

### 🏪 Finding 3 — The Merchant Revolution Nobody Talks About
UPI launched as a way to send money to friends. It's now something far more powerful.

```
2020  P2P ████████████████████████ 61.6%  |  P2M ██████████ 38.4%
2021  P2P ███████████████████████  56.5%  |  P2M ███████████ 43.5%
2022  P2P █████████████████████    53.3%  |  P2M ████████████ 46.7%
2023  P2P █████████████████        43.4%  |  P2M █████████████████ 56.6% ← tipped
```
**Merchants crossed 50% in 2023. Every chai shop, kirana store, and auto-rickshaw is now a UPI terminal.**

---

### 💸 Finding 4 — The Micro-Payment Shift Is Real
| Era | Period | Avg Ticket | Payment Regime |
|-----|--------|-----------|----------------|
| Post-Demonetization Growth | Nov 2019–Feb 2020 | ₹1,609 | High-Value Transfers |
| COVID Impact | Mar 2020–May 2021 | **₹1,825** ← Peak | High-Value Transfers |
| Post-COVID Surge | Jun 2021–Dec 2022 | ₹1,759 | High-Value Transfers |
| Maturity Phase | Jan 2023–Mar 2026 | ₹1,428 | **Transition → Micro** |

Peak: ₹1,959 (Jun 2020) → Current: ₹1,304 (Mar 2026) — **33% drop in 6 years.**
Every ₹50 chai, ₹120 medicine, ₹200 auto ride pulls the average down.

---

### 🏆 Finding 5 — There Is No Second Place
```
IMPS (UPI's closest competitor)
2024 full year total:  5,938 Million transactions
                       ████████░░░░░░░░░░░░░░░░░░░░░░

UPI monthly average (2024):
                       ████████████████████████████████████████  14,350 Million
```
**UPI processes in ONE MONTH what IMPS processes in an ENTIRE YEAR.**
The Indian retail payments race ended years ago. Everyone else is competing for second.

---

### 🏛️ Finding 6 — 459 Million People, One Account
Jan Dhan → UPI → Financial inclusion pipeline:
- **458,932,822** previously unbanked citizens now have accounts
- **₹1,69,879 Crore** in deposits from zero-balance account holders
- 36 states & UTs covered
- States with sub-30% smartphone penetration = next 4 billion monthly transactions

---

## 🗄️ Data Pipeline

```
RBI / NPCI / data.gov.in          Python (Pandas)            PostgreSQL
Government Sources          →      Clean + Engineer    →      4 Tables
                                   77 rows primary            upi_monthly
13 raw files                       41 rows P2P/P2M            upi_p2p_p2m
Nov 2019–Mar 2026                  120 rows NPCI              npci_products
                                   36 rows Jan Dhan           jan_dhan_statewise
                                         ↓
                                   5 SQL Queries
                                         ↓
                                   Power BI Dashboard
                                   3 pages · 10 visuals
```

---

## 🔬 SQL Queries

| # | Query | The Question It Answers |
|---|-------|------------------------|
| 1 | `01_yoy_performance` | How fast did UPI grow each year and is it still growing? |
| 2 | `02_p2p_vs_p2m_shift` | When did merchants overtake personal transfers? |
| 3 | `03_bank_adoption_rate` | How fast is the banking network expanding? |
| 4 | `04_payment_mode_comparison` | How dominant is UPI vs every other payment rail? |
| 5 | `05_ticket_size_era_analysis` | Are we in the micro-payment era yet? |

---

## 📦 Tech Stack

```
Data Sources    →  RBI DBIE Portal · NPCI Monthly Stats · data.gov.in
Engineering     →  Python 3.12 · Pandas · NumPy
Database        →  PostgreSQL 16 · SQLAlchemy · psycopg2
Visualisation   →  Matplotlib · Seaborn (EDA) · Power BI (Dashboard)
```

---

## 🚀 Reproduce This

```bash
git clone https://github.com/yourusername/upi-payment-intelligence
cd upi-payment-intelligence
pip install -r requirements.txt

python 00_setup.py                 # verify 13 files + libraries
python 01_clean_engineer.py        # clean → 4 processed CSVs
python 02_eda_visualizations.py    # 7 EDA charts → notebooks/charts/
python 03_load_postgres.py         # load 4 PostgreSQL tables
python 04_run_sql_queries.py       # run 5 SQL queries
python export_for_powerbi.py       # export 6 Power BI CSVs
```

---

<div align="center">

**Data Period:** Nov 2019 – Mar 2026 &nbsp;|&nbsp; **Source:** RBI & NPCI &nbsp;|&nbsp; **Rows Analysed:** 274 across 4 tables

*Every number in this README came directly from the pipeline output. Nothing estimated.*

</div>