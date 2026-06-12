"""
01_clean_engineer.py
Loads, cleans, and feature-engineers all UPI datasets.
Run this first. Saves processed CSVs to data/processed/

DATASETS USED:
  - upi_monthly_stats.csv         → PRIMARY: Nov 2019–Mar 2026, 77 rows
  - upi_p2p_p2w.csv               → P2P vs P2M breakdown, Apr 2020–Aug 2023
  - jan_dhan_statewise.csv        → State-wise PMJDY accounts
  - AePS_*.csv (3 files)          → NPCI product comparison (2024)

UNITS CONFIRMED:
  - volume_crore = transactions in crore  (121.88 crore = 1.22 billion in Nov 2019)
  - value_crore  = rupee value in crore
  - avg_ticket   = value_crore / volume_crore  (Rs per transaction, crore cancels)
  - p2p/p2m vols in million → divide by 10 to get crore  (1 crore = 10 million)
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs("data/processed", exist_ok=True)

print("=" * 60)
print("STEP 1 — CLEANING & FEATURE ENGINEERING")
print("=" * 60)


# ============================================================
# 1. UPI MONTHLY — PRIMARY SOURCE
# ============================================================
print("\n[1/4] Loading upi_monthly_stats.csv ...")

upi = pd.read_csv("data/raw/upi_monthly_stats.csv", parse_dates=['date'])
upi = upi.sort_values('date').reset_index(drop=True)

print(f"  Shape     : {upi.shape}")
print(f"  Columns   : {upi.columns.tolist()}")
print(f"  Date range: {upi['date'].min().date()} → {upi['date'].max().date()}")
print(f"  Nulls     :\n{upi.isnull().sum()}")

# Verify expected columns exist
required = ['date', 'volume_crore', 'value_crore']
for col in required:
    assert col in upi.columns, f"Missing column: {col}"

# Ensure numeric
upi['volume_crore'] = pd.to_numeric(upi['volume_crore'], errors='coerce')
upi['value_crore']  = pd.to_numeric(upi['value_crore'], errors='coerce')
if 'banks_live_on_upi' in upi.columns:
    upi['banks_live_on_upi'] = pd.to_numeric(upi['banks_live_on_upi'], errors='coerce')

print(f"\n  Sample:\n{upi[['date','volume_crore','value_crore','banks_live_on_upi']].tail(3).to_string(index=False)}")


# ============================================================
# 2. FEATURE ENGINEERING
# ============================================================
print("\n[2/4] Engineering features ...")

# --- Time dimensions ---
upi['year']       = upi['date'].dt.year
upi['month']      = upi['date'].dt.month
upi['month_name'] = upi['date'].dt.strftime('%b')
upi['year_month'] = upi['date'].dt.to_period('M').astype(str)
upi['quarter']    = upi['date'].dt.quarter

# --- Growth rates ---
upi['volume_mom_pct'] = (upi['volume_crore'].pct_change() * 100).round(2)
upi['value_mom_pct']  = (upi['value_crore'].pct_change() * 100).round(2)
upi['volume_yoy_pct'] = (upi['volume_crore'].pct_change(12) * 100).round(2)
upi['value_yoy_pct']  = (upi['value_crore'].pct_change(12) * 100).round(2)

# --- Avg ticket size (Rs per transaction) ---
# Both columns in crore → crore cancels → result is Rs
upi['avg_ticket_size_rs'] = (upi['value_crore'] / upi['volume_crore']).round(2)

# --- Rolling averages (volume) ---
upi['volume_3m_avg']  = upi['volume_crore'].rolling(3).mean().round(2)
upi['volume_12m_avg'] = upi['volume_crore'].rolling(12).mean().round(2)

# --- Annualized run rate (billion transactions) ---
# volume_crore * 12 months / 100 (100 crore = 1 billion)
upi['annualized_volume_bn'] = (upi['volume_crore'] * 12 / 100).round(2)

# --- Era flag ---
def label_era(date):
    if date < pd.Timestamp('2020-03-01'):   return '1_Post-Demonetization Growth'
    if date < pd.Timestamp('2021-06-01'):   return '2_COVID Impact'
    if date < pd.Timestamp('2023-01-01'):   return '3_Post-COVID Surge'
    return '4_Maturity Phase'

upi['era'] = upi['date'].apply(label_era)

print(f"  ✓ Engineered columns: volume_mom_pct, value_mom_pct, volume_yoy_pct, value_yoy_pct,")
print(f"    avg_ticket_size_rs, volume_3m_avg, volume_12m_avg, annualized_volume_bn, era")

# Save
upi.to_csv("data/processed/upi_clean.csv", index=False)
print(f"\n  ✓ Saved data/processed/upi_clean.csv ({len(upi)} rows)")

# Quick sanity check
latest = upi.iloc[-1]
first  = upi.iloc[0]
print(f"\n  SANITY CHECK:")
print(f"  First row  : {first['date'].date()} | vol={first['volume_crore']} Cr | ticket=₹{first['avg_ticket_size_rs']:.0f}")
print(f"  Latest row : {latest['date'].date()} | vol={latest['volume_crore']} Cr | ticket=₹{latest['avg_ticket_size_rs']:.0f}")
print(f"  Volume growth: {first['volume_crore']} → {latest['volume_crore']} Cr ({latest['volume_crore']/first['volume_crore']:.0f}x)")


# ============================================================
# 3. P2P vs P2M — upi_p2p_p2w.csv
# ============================================================
print("\n[3/4] Loading upi_p2p_p2w.csv (P2P vs P2M) ...")

p2p_raw = pd.read_csv("data/raw/upi_p2p_p2w.csv")
print(f"  Shape  : {p2p_raw.shape}")
print(f"  Columns: {p2p_raw.columns.tolist()}")

# Parse date
p2p_raw['date'] = pd.to_datetime(p2p_raw['month'])
p2p = p2p_raw[['date','total_vol','total_val','p2p_vol','p2p_val','p2m_vol','p2m_val']].copy()
p2p = p2p.sort_values('date').reset_index(drop=True)

# Convert million → crore (1 crore = 10 million)
for col in ['total_vol','p2p_vol','p2m_vol']:
    p2p[col + '_crore'] = (p2p[col] / 10).round(2)

p2p.rename(columns={
    'total_val': 'total_val_crore',
    'p2p_val':   'p2p_val_crore',
    'p2m_val':   'p2m_val_crore'
}, inplace=True)

# Drop original million columns
p2p.drop(columns=['total_vol', 'p2p_vol', 'p2m_vol'], inplace=True)

# P2M share %
p2p['p2m_share_pct'] = (
    p2p['p2m_vol_crore'] / p2p['total_vol_crore'] * 100
).round(2)

# Time dims
p2p['year']  = p2p['date'].dt.year
p2p['month'] = p2p['date'].dt.month

p2p.to_csv("data/processed/p2p_p2m_clean.csv", index=False)
print(f"  ✓ Saved data/processed/p2p_p2m_clean.csv ({len(p2p)} rows)")
print(f"  Date range: {p2p['date'].min().date()} → {p2p['date'].max().date()}")
print(f"  P2M share : {p2p['p2m_share_pct'].min():.1f}% → {p2p['p2m_share_pct'].max():.1f}%")


# ============================================================
# 4. JAN DHAN + AePS NPCI PRODUCTS
# ============================================================
print("\n[4/4] Loading Jan Dhan + AePS product files ...")

# --- Jan Dhan ---
jd = pd.read_csv("data/raw/jan_dhan_statewise.csv")
jd.columns = (jd.columns.str.strip().str.lower()
              .str.replace(r'[\s\-\/\(\)]+', '_', regex=True)
              .str.replace(r'_+', '_', regex=True).str.strip('_'))
# Remove total row for state-level analysis
jd_states = jd[jd['state_ut'].str.lower() != 'total'].copy()
jd_states.to_csv("data/processed/jan_dhan_clean.csv", index=False)
total_row = jd[jd['state_ut'].str.lower() == 'total']
total_accounts = int(total_row['number_of_pmjdy_accounts'].values[0])
total_deposit  = float(total_row['deposit_in_rs._crore'].values[0])
print(f"  ✓ Jan Dhan: {len(jd_states)} states | {total_accounts:,} total accounts | ₹{total_deposit:,.0f} Cr deposits")

# --- AePS NPCI Products ---
import glob
aePS_map = {
    "AePS_-_BHIM_Aadhaar_Pay_Monthly_Product_Statistics_Trended.csv": "AePS_BHIM_Aadhaar_Pay",
    "AePS_-_Cash_Withdrawal_Monthly_Product_Statistics_Trended.csv":  "AePS_Cash_Withdrawal",
    "AePS_-_Funds_Transfer_Monthly_Product_Statistics_Trended.csv":   "AePS_Funds_Transfer",
    "CTS_Monthly_Product_Statistics_Trended.csv":                     "CTS",
    "IMPS_Monthly_Product_Statistics_Trended.csv":                    "IMPS",
    "NACH_-_APBS_Monthly_Product_Statistics_Trended.csv":             "NACH_APBS",
    "NACH_-_Credit_Monthly_Product_Statistics_Trended.csv":           "NACH_Credit",
    "NACH_-_Debit_Monthly_Product_Statistics_Trended.csv":            "NACH_Debit",
    "NETC_Monthly_Product_Statistics_Trended.csv":                    "NETC",
    "NFS_Monthly_Product_Statistics_Trended.csv":                     "NFS",
}

npci_frames = []
for filename, product_name in aePS_map.items():
    fpath = f"data/raw/{filename}"
    if os.path.exists(fpath):
        df_tmp = pd.read_csv(fpath)
        # Remove unnamed leading columns
        df_tmp = df_tmp.loc[:, ~df_tmp.columns.str.match(r'^Unnamed')]
        df_tmp.columns = [c.strip() for c in df_tmp.columns]
        df_tmp['product_name'] = product_name
        # Parse month: "24-Jan" → date
        df_tmp['date'] = pd.to_datetime(df_tmp['Month'].str.strip(), format='%y-%b')
        df_tmp.rename(columns={'Volume (in Mn.)': 'volume_mn', 'Avg. Daily Volume (in Mn.)': 'avg_daily_vol_mn'}, inplace=True)
        df_tmp['year'] = df_tmp['date'].dt.year
        df_tmp['month_name'] = df_tmp['date'].dt.strftime('%b')
        npci_frames.append(df_tmp[['product_name','date','year','month_name','volume_mn','avg_daily_vol_mn']])
        print(f"  ✓ {product_name}: {len(df_tmp)} rows")
    else:
        print(f"  ✗ Not found: {fpath}")

if npci_frames:
    npci_all = pd.concat(npci_frames, ignore_index=True).sort_values(['product_name','date'])
    npci_all.to_csv("data/processed/npci_products_clean.csv", index=False)
    print(f"  ✓ Saved data/processed/npci_products_clean.csv ({len(npci_all)} rows total)")


# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  upi_monthly    : {len(upi)} rows | {upi['date'].min().strftime('%b %Y')} → {upi['date'].max().strftime('%b %Y')}")
print(f"  p2p_p2m        : {len(p2p)} rows | {p2p['date'].min().strftime('%b %Y')} → {p2p['date'].max().strftime('%b %Y')}")
print(f"  jan_dhan       : {len(jd_states)} states")
print(f"  npci_products  : {len(npci_all) if npci_frames else 0} rows (3 AePS product types, 2024)")

print(f"\n  Key metrics (latest = {latest['date'].strftime('%b %Y')}):")
print(f"  Volume      : {latest['volume_crore']:.2f} Cr transactions/month")
print(f"  Value       : ₹{latest['value_crore']:,.0f} Cr")
print(f"  Avg ticket  : ₹{latest['avg_ticket_size_rs']:.0f}")
print(f"  Ann. run rt : {latest['annualized_volume_bn']:.1f} Bn txns/year")
print(f"  Banks on UPI: {int(upi['banks_live_on_upi'].dropna().iloc[-1])}")

print("\n  Era breakdown:")
era_s = upi.groupby('era').agg(
    months=('volume_crore','count'),
    avg_vol_crore=('volume_crore','mean'),
    avg_ticket=('avg_ticket_size_rs','mean')
).round(1)
print(era_s.to_string())

print("\n✓ Done. Run 02_eda_visualizations.py next.")