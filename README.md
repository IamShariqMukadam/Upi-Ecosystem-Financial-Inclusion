<div align="center">

# 💳 UPI Payment Intelligence

### *India processed more digital payments than the entire US & Europe combined in 2024.*
### *This project shows exactly how that happened.*

<br>

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Data Source](https://img.shields.io/badge/Data-RBI%20%26%20NPCI%20Official-green?style=for-the-badge)

<br>

| 📅 Coverage | 📊 Records | 🏦 Data Sources | 🔢 SQL Queries | 📈 Charts |
|:-----------:|:----------:|:---------------:|:--------------:|:---------:|
| Nov 2019 – Mar 2026 | 77 months | RBI · NPCI · data.gov.in | 5 | 7 |

<br>

**[🚀 View Live Dashboard](#) &nbsp;·&nbsp; [📂 Explore Data](#data-sources) &nbsp;·&nbsp; [💡 Key Findings](#-the-numbers-that-matter)**

</div>

---

<div align="center">

## 📸 Dashboard

| 📈 Growth Story | 🏦 Ecosystem Health | 🧠 Payment Intelligence |
|:---:|:---:|:---:|
| ![Page 1](dashboard/screenshots/page1_growth.png) | ![Page 2](dashboard/screenshots/page2_ecosystem.png) | ![Page 3](dashboard/screenshots/page3_intelligence.png) |
| Volume growth by era | Bank network expansion | Seasonality & regime shift |

</div>

---

## ⚡ The Numbers That Matter

<table>
<tr>
<td width="25%" align="center">
<h2>19x</h2>
Volume growth<br><sub>Nov 2019 → Mar 2026</sub>
</td>
<td width="25%" align="center">
<h2>+647%</h2>
YoY growth in 2020<br><sub>COVID was a catalyst</sub>
</td>
<td width="25%" align="center">
<h2>58.5%</h2>
P2M share by Aug 2023<br><sub>Up from 38.4% in 2020</sub>
</td>
<td width="25%" align="center">
<h2>271.7 Bn</h2>
Annual run rate<br><sub>Transactions per year</sub>
</td>
</tr>
<tr>
<td width="25%" align="center">
<h2>₹1,304</h2>
Avg ticket Mar 2026<br><sub>Down from ₹1,959 peak</sub>
</td>
<td width="25%" align="center">
<h2>684</h2>
Banks on UPI<br><sub>Up from 563 in 2024</sub>
</td>
<td width="25%" align="center">
<h2>24x</h2>
UPI vs IMPS volume<br><sub>No competition exists</sub>
</td>
<td width="25%" align="center">
<h2>458.9M</h2>
Jan Dhan accounts<br><sub>₹1.7L Cr in deposits</sub>
</td>
</tr>
</table>

---

## 🔍 5 Findings That Tell the Real Story

### `#1` 🦠 COVID Was a Launchpad, Not a Setback
> Everyone expected COVID to kill digital payments. The data says +647% YoY in 2020.

When lockdowns hit, Indians stopped using cash overnight. Avg ticket size **peaked at ₹1,959 in Jun 2020** — people were moving rent, bulk groceries, and family funds digitally. UPI didn't just survive COVID, it used it as a growth engine.

---

### `#2` 🏪 The Merchant Revolution Nobody Talks About
> UPI started as a way to split bills. It's now India's primary retail payment rail.

```
Apr 2020  ████████████████░░░░░░░░░░░░░░  38.4% merchant payments
Aug 2023  ████████████████████████░░░░░░  58.5% merchant payments
```
P2M (merchant) share grew **~3-4pp per year**, then **jumped 10pp in 2023 alone.**
Every chai shop, kirana store, and petrol pump is now a UPI merchant.

---

### `#3` 📉 Falling Ticket Size = Rising Adoption (Counterintuitive)
> The avg transaction value is falling. That's actually the best sign possible.

| Era | Period | Avg Ticket |
|-----|--------|-----------|
| Post-Demonetization Growth | Nov 2019–Feb 2020 | ₹1,609 |
| COVID Impact | Mar 2020–May 2021 | **₹1,825 ← peak** |
| Post-COVID Surge | Jun 2021–Dec 2022 | ₹1,759 |
| Maturity Phase | Jan 2023–Mar 2026 | ₹1,428 ↓ |

Ticket dropped ₹655 in 3 years because millions of ₹50 tea payments entered the system. That's not decline — that's mass adoption.

---

### `#4` 🏆 There Is No Competition
> IMPS is India's second-largest payment rail. UPI does IMPS's entire annual volume in **one month.**

| Payment Rail | 2024 Annual Volume |
|-------------|-------------------|
| IMPS | 5,938 Mn |
| NETC (FASTag) | 4,059 Mn |
| NACH APBS | 3,219 Mn |
| **UPI (monthly avg)** | **~14,350 Mn** |

UPI is **24x IMPS**. The Indian retail payments race ended years ago.

---

### `#5` 📊 Year-over-Year — Moderating but Still Massive
> Growth % is slowing. Absolute growth is not.

| Year | Total Volume | YoY Growth |
|------|-------------|-----------|
| 2019 (2 months) | 253 Cr | — |
| 2020 | 1,888 Cr | 🟢 **+647.1%** |
| 2021 | 3,873 Cr | 🟢 +105.1% |
| 2022 | 7,404 Cr | 🟢 +91.2% |
| 2023 | 11,761 Cr | 🟢 +58.9% |
| 2024 | 17,221 Cr | 🟢 +46.4% |
| 2025 | 22,828 Cr | 🟢 +32.6% |

UPI still adds ~5,000 Crore transactions annually in absolute terms. Maturing ≠ slowing.

---

## 🏗️ How It Was Built

```
📥 RAW DATA          🔧 PYTHON PIPELINE        🗄️ POSTGRESQL         📊 POWER BI
─────────────        ──────────────────        ──────────────        ──────────
RBI Excel       →    01_clean_engineer    →    upi_monthly      →    Growth Story
NPCI CSVs       →    02_eda_charts        →    upi_p2p_p2m      →    Ecosystem
Jan Dhan CSV    →    03_load_postgres     →    npci_products    →    Payment Intel
13 files total  →    04_sql_queries       →    jan_dhan         →    3-page report
                →    export_powerbi       →    5 SQL queries    →    Live dashboard
```

---

## 📁 Project Structure

```
upi-payment-intelligence/
├── 📂 data/raw/                ← 13 original government source files
├── 📂 data/processed/          ← Cleaned CSVs + SQL outputs + Power BI exports
├── 📂 notebooks/charts/        ← 7 EDA charts (PNG)
├── 📂 sql/                     ← 5 analytical SQL queries
├── 📂 dashboard/screenshots/   ← 3 Power BI page exports
├── 🐍 00_setup.py              ← Environment verification
├── 🐍 01_clean_engineer.py     ← Cleaning + feature engineering (77 rows → 18 features)
├── 🐍 02_eda_visualizations.py ← 7 production charts
├── 🐍 03_load_postgres.py      ← PostgreSQL loader (4 tables)
├── 🐍 04_run_sql_queries.py    ← 5 SQL analytical queries
└── 🐍 export_for_powerbi.py    ← Power BI CSV exporter (6 files)
```

---

## 🗄️ Data Sources

| Dataset | Source | Coverage |
|---------|--------|----------|
| UPI Monthly Volume & Value | NPCI via India Data Portal | Nov 2019–Mar 2026 |
| UPI P2P vs P2M Breakdown | NPCI via India Data Portal | Apr 2020–Aug 2023 |
| 10 Payment Rails (IMPS, NACH, FASTag etc.) | NPCI Monthly Statistics | 2024 |
| Jan Dhan State-wise Accounts | data.gov.in | Latest snapshot, 36 states |

> ⚠️ All data sourced directly from Indian government portals. No Kaggle. No synthetic data.

---

## ⚙️ Reproduce This Project

```bash
git clone https://github.com/yourusername/upi-payment-intelligence
cd upi-payment-intelligence
pip install -r requirements.txt

python 00_setup.py                 # ✓ verify environment & files
python 01_clean_engineer.py        # ✓ clean + engineer 18 features
python 02_eda_visualizations.py    # ✓ generate 7 EDA charts
python 03_load_postgres.py         # ✓ load 4 tables to PostgreSQL
python 04_run_sql_queries.py       # ✓ run 5 SQL queries
python export_for_powerbi.py       # ✓ export 6 Power BI CSVs
```

---

<div align="center">

**Built on verified government data · Python · PostgreSQL · Power BI**

*If this repo helped you, give it a ⭐*

</div>