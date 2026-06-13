# 🇮🇳 India UPI Payment Intelligence Dashboard

> Tracking India's ₹2,952,542 Crore digital payment revolution — Nov 2019 to Mar 2026.
> Built on verified RBI & NPCI government data. No Kaggle toy datasets.

---

## 📊 Dashboard Preview

| Growth Story | Ecosystem Health | Payment Intelligence |
|:---:|:---:|:---:|
| ![Growth Story](dashboard/screenshots/page1_growth.png) | ![Ecosystem](dashboard/screenshots/page2_ecosystem.png) | ![Payment Intel](dashboard/screenshots/page3_intelligence.png) |

🔗 **[View Live Dashboard on Power BI](your-publish-to-web-link)**

---

## 🔑 Key Findings

### 1. 19x Volume Growth in 7 Years
UPI processed **121.88 Crore transactions in Nov 2019**.
By **Mar 2026 that number hit 2,264.11 Crore** — a **19x increase** in under 7 years.
Annualized run rate as of Mar 2026: **271.7 Billion transactions/year.**

### 2. The COVID Paradox — A Catalyst, Not a Brake
Conventional wisdom said COVID would hurt fintech. The data says otherwise.
- **2020 saw +647.1% YoY growth** — the single largest annual jump in UPI history
- Avg ticket size **peaked at ₹1,959 in Jun 2020** as people moved rent, bulk groceries, and family transfers to digital
- UPI didn't just survive COVID — it used it as a launchpad

| Year | YoY Volume Growth |
|------|------------------|
| 2020 | **+647.1%** |
| 2021 | +105.1% |
| 2022 | +91.2% |
| 2023 | +58.9% |
| 2024 | +46.4% |
| 2025 | +32.6% |

Growth is moderating in percentage terms — but in absolute terms UPI still added ~5,000 Crore transactions per year. **This is a maturing market, not a decelerating one.**

### 3. The Merchant Revolution — P2P → P2M Shift
UPI launched as a peer-to-peer transfer tool. It's now something far bigger.

- **P2M (merchant payment) share: 38.4% (Apr 2020) → 58.5% (Aug 2023)**
- Growing ~3-4 percentage points per year, then **jumped 10pp in 2023 alone**
- UPI is now the primary payment rail at India's chai shops, kirana stores, petrol pumps, and hospitals
- Current P2M share (extrapolated): likely **62-65%+**

### 4. The Micro-Payment Story — Falling Ticket Size
| Era | Period | Avg Monthly Volume | Avg Ticket Size |
|-----|--------|-------------------|-----------------|
| Post-Demonetization Growth | Nov 2019–Feb 2020 | 128.9 Cr | ₹1,609 |
| COVID Impact | Mar 2020–May 2021 | 191.7 Cr | ₹1,825 ← Peak era |
| Post-COVID Surge | Jun 2021–Dec 2022 | 527.8 Cr | ₹1,759 |
| Maturity Phase | Jan 2023–Mar 2026 | 1,494.5 Cr | ₹1,428 |

Avg ticket fell from a peak of **₹1,959 (Jun 2020) → ₹1,304 (Mar 2026)**.
Every ₹50 tea, ₹120 medicine, ₹200 auto ride pulls the average down.
The true Micro-Payment Era (sub-₹1,000 avg) is approaching — not yet arrived.

### 5. UPI vs Every Other Payment Rail — There Is No Competition
In all of 2024, IMPS (UPI's closest competitor) processed **5,938 Million transactions**.
UPI processes that volume in **a single month.**
**UPI is 24x IMPS by volume. The Indian retail payments race is over.**

NPCI Product Rankings (2024 volume, Mn):

| Rank | Product | Annual Volume (Mn) |
|------|---------|-------------------|
| 1 | IMPS | 5,938 |
| 2 | NETC (FASTag) | 4,059 |
| 3 | NFS | 3,668 |
| 4 | NACH APBS | 3,219 |
| 5 | NACH Credit | 1,650 |

*UPI not shown above — monthly avg alone (14,350 Mn) exceeds IMPS annual total.*

### 6. Bank Ecosystem — Network Effect in Action
| Year | Banks at Start | Banks at End | Banks Added |
|------|---------------|-------------|-------------|
| 2024 | 563 | 620 | 57 (+10.1%) |
| 2025 | 630 | 682 | 52 (+8.3%) |
| 2026 | 684 | 684 | 0 (data to Mar) |

563 → 684 banks in 2 years. More banks = more users = more merchants = more transactions. The network effect is real and compounding.

### 7. Financial Inclusion Angle
- **458,932,822** Jan Dhan accounts across 36 states & UTs
- **₹169,879 Crore** in deposits from previously unbanked citizens
- This population represents the next frontier for UPI penetration — states with sub-30% smartphone penetration could add billions of monthly transactions

---

## 🗂️ Data Sources

| Dataset | Source | Coverage | Rows |
|---------|--------|----------|------|
| UPI Monthly Volume & Value | NPCI / India Data Portal | Nov 2019–Mar 2026 | 77 |
| UPI P2P vs P2M Breakdown | NPCI / India Data Portal | Apr 2020–Aug 2023 | 41 |
| AePS & Payment Rails (10 products) | NPCI Monthly Statistics | 2024 only | 120 |
| Jan Dhan State-wise Accounts | data.gov.in | Latest snapshot | 36 states |

*All data sourced directly from Indian government portals (RBI, NPCI, data.gov.in). No third-party aggregators.*

---

## 🛠️ Tech Stack

| Layer | Tools |
|-------|-------|
| Data Cleaning & Engineering | Python, Pandas, NumPy |
| Database | PostgreSQL |
| EDA & Charts | Matplotlib, Seaborn |
| SQL Analysis | PostgreSQL (5 analytical queries) |
| Dashboard | Power BI (3-page interactive report) |
| Data Sources | RBI DBIE Portal, NPCI, data.gov.in |

---

## 📁 Project Structure

```
upi-payment-intelligence/
│
├── data/
│   ├── raw/                    ← 13 original source files
│   └── processed/              ← Cleaned CSVs + SQL outputs + Power BI exports
│
├── notebooks/
│   └── charts/                 ← 7 EDA charts (PNG)
│
├── sql/
│   ├── 01_yoy_performance.sql
│   ├── 02_p2p_vs_p2m_shift.sql
│   ├── 03_bank_adoption_rate.sql
│   ├── 04_payment_mode_comparison.sql
│   └── 05_ticket_size_era_analysis.sql
│
├── dashboard/
│   └── screenshots/            ← 3 Power BI page exports
│
├── 00_setup.py                 ← Environment check
├── 01_clean_engineer.py        ← Data cleaning + feature engineering
├── 02_eda_visualizations.py    ← 7 EDA charts
├── 03_load_postgres.py         ← PostgreSQL loader
├── 04_run_sql_queries.py       ← 5 SQL queries
├── export_for_powerbi.py       ← Power BI CSV exporter
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Reproduce

```bash
# 1. Clone and install
git clone https://github.com/yourusername/upi-payment-intelligence.git
cd upi-payment-intelligence
pip install -r requirements.txt

# 2. Add raw data files to data/raw/ (see Data Sources above)

# 3. Run pipeline
python 00_setup.py                  # verify environment
python 01_clean_engineer.py         # clean + engineer features
python 02_eda_visualizations.py     # generate 7 EDA charts
python 03_load_postgres.py          # load to PostgreSQL
python 04_run_sql_queries.py        # run 5 SQL queries
python export_for_powerbi.py        # export Power BI CSVs
```

---

## 📈 EDA Charts Generated

1. **UPI Volume Growth 2019–2026** — era-coloured area chart with event markers
2. **Average Ticket Size** — micro-payment shift story with 12-month rolling avg
3. **YoY Growth % + Banks on UPI** — dual panel showing growth and ecosystem expansion
4. **Seasonality Heatmap** — Year × Month volume matrix
5. **Volume vs Value Divergence** — dual-axis showing growing volume, declining ticket size
6. **Era Comparison** — 3-panel bar chart comparing all 4 eras
7. **P2P vs P2M Shift** — stacked area + merchant share % over time

---

## 💡 SQL Queries

| Query | What It Answers |
|-------|----------------|
| `01_yoy_performance` | Year-over-year volume, value, ticket size, and bank count with growth % |
| `02_p2p_vs_p2m_shift` | Annual P2M share trend — how fast merchants are adopting UPI |
| `03_bank_adoption_rate` | Banks added per year and growth % — quantifying the network effect |
| `04_payment_mode_comparison` | UPI vs IMPS vs NACH vs FASTag — who owns Indian payments in 2024 |
| `05_ticket_size_era_analysis` | Ticket size by era with payment regime classification |

---

## 🎯 Interview Talking Points

- **"COVID paradox"** — 2020 saw 647% growth, proving fintech thrives in forced digital adoption
- **"P2P to P2M is the real story"** — the shift from transfers to merchant payments shows UPI becoming retail infrastructure, not just a banking tool
- **"Growth is moderating but accelerating in absolute terms"** — demonstrates analytical maturity beyond surface-level YoY numbers
- **"IMPS comparison"** — one statistic that contextualises UPI's dominance without needing a chart
- **"Bank data only from 2024"** — being honest about data limitations shows integrity

---

*Built with publicly available government data. All findings reproducible.*