"""
00_setup.py
Run this first. Creates folder structure and verifies environment + all data files.
"""

import os
import sys

# ── CREATE FOLDERS ─────────────────────────────────────────
folders = ["data/raw", "data/processed", "notebooks/charts", "sql", "dashboard"]
print("Creating folders...")
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"  ✓ {folder}")

# ── CHECK LIBRARIES ────────────────────────────────────────
print("\nChecking libraries...")
required = ["pandas", "numpy", "matplotlib", "seaborn", "sqlalchemy", "psycopg2", "plotly", "scipy"]
missing = []
for lib in required:
    try:
        __import__(lib)
        print(f"  ✓ {lib}")
    except ImportError:
        missing.append(lib)
        print(f"  ✗ {lib} — NOT INSTALLED")

if missing:
    print(f"\n  Run: pip install {' '.join(missing)}")
    sys.exit(1)
else:
    print("  ✓ All libraries OK")

# ── CHECK DATA FILES ───────────────────────────────────────
print("\nChecking data/raw files...")

primary = [
    "upi_monthly_stats.csv",
    "upi_p2p_p2w.csv",
    "jan_dhan_statewise.csv",
]

npci_products = [
    "AePS_-_BHIM_Aadhaar_Pay_Monthly_Product_Statistics_Trended.csv",
    "AePS_-_Cash_Withdrawal_Monthly_Product_Statistics_Trended.csv",
    "AePS_-_Funds_Transfer_Monthly_Product_Statistics_Trended.csv",
    "CTS_Monthly_Product_Statistics_Trended.csv",
    "IMPS_Monthly_Product_Statistics_Trended.csv",
    "NACH_-_APBS_Monthly_Product_Statistics_Trended.csv",
    "NACH_-_Credit_Monthly_Product_Statistics_Trended.csv",
    "NACH_-_Debit_Monthly_Product_Statistics_Trended.csv",
    "NETC_Monthly_Product_Statistics_Trended.csv",
    "NFS_Monthly_Product_Statistics_Trended.csv",
]

missing_files = []

print("\n  [Primary datasets]")
for f in primary:
    exists = os.path.exists(f"data/raw/{f}")
    print(f"  {'✓' if exists else '✗'} {f}")
    if not exists:
        missing_files.append(f)

print("\n  [NPCI product CSVs]")
for f in npci_products:
    exists = os.path.exists(f"data/raw/{f}")
    print(f"  {'✓' if exists else '✗'} {f}")
    if not exists:
        missing_files.append(f)

# ── FINAL VERDICT ──────────────────────────────────────────
print("\n" + "=" * 55)
if missing_files:
    print(f"✗ {len(missing_files)} file(s) missing from data/raw/ — copy them before continuing:")
    for f in missing_files:
        print(f"    - {f}")
    sys.exit(1)
else:
    print(f"✓ All 13 files present.")
    print("✓ Environment ready.")
    print("\n  Run order:")
    print("  1. python 01_clean_engineer.py")
    print("  2. python 02_eda_visualizations.py")
    print("  3. python 03_load_postgres.py")
    print("  4. python 04_run_sql_queries.py")