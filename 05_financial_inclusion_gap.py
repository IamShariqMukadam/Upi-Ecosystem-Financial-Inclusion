"""
05_financial_inclusion_gap.py
Analyzes Jan Dhan state-wise data to identify digitally underserved states.
Run after 01_clean_engineer.py

METRIC: Deposit per account (Rs) vs national average
LOW deposit per account = financially included but cash-dependent
GAP = potential deposits if state reaches national average

KEY FINDINGS:
  - 12 states below national avg of Rs 3,702/account
  - 255.9M accounts in these states (55.8% of all Jan Dhan accounts)
  - Total untapped deposit potential: Rs 12,417 Crore
  - Top 3 states: MP (Rs 4,240 Cr), Assam (Rs 2,276 Cr), Bihar (Rs 1,157 Cr)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs("data/processed", exist_ok=True)
os.makedirs("notebooks/charts", exist_ok=True)

print("=" * 60)
print("FINANCIAL INCLUSION GAP ANALYSIS")
print("=" * 60)


# ── LOAD ────────────────────────────────────────────────────
df = pd.read_csv("data/processed/jan_dhan_clean.csv")
print(f"\n  Loaded: {len(df)} states")
print(f"  Columns: {df.columns.tolist()}")

# Rename for clarity
df = df.rename(columns={
    'state_ut':                   'state',
    'number_of_pmjdy_accounts':   'accounts',
    'deposit_in_rs._crore':       'deposit_crore'
})

# ── NATIONAL AVERAGE ────────────────────────────────────────
TOTAL_ACCOUNTS     = 458932822
TOTAL_DEPOSIT_CRORE = 169879.24
NATIONAL_AVG_RS    = (TOTAL_DEPOSIT_CRORE * 10000000) / TOTAL_ACCOUNTS

print(f"\n  National avg deposit per account : ₹{NATIONAL_AVG_RS:,.0f}")
print(f"  Total Jan Dhan accounts          : {TOTAL_ACCOUNTS:,}")
print(f"  Total deposits                   : ₹{TOTAL_DEPOSIT_CRORE:,.0f} Crore")


# ── FEATURE ENGINEERING ─────────────────────────────────────
df['deposit_per_account_rs']    = (df['deposit_crore'] * 10000000 / df['accounts']).round(0)
df['national_avg_rs']           = round(NATIONAL_AVG_RS, 0)
df['gap_vs_national_avg_rs']    = (NATIONAL_AVG_RS - df['deposit_per_account_rs']).round(0)
df['gap_crore']                 = ((df['gap_vs_national_avg_rs'] * df['accounts']) / 10000000).round(2)
df['below_national_avg']        = df['deposit_per_account_rs'] < NATIONAL_AVG_RS
df['pct_of_national_avg']       = (df['deposit_per_account_rs'] / NATIONAL_AVG_RS * 100).round(1)
df['account_share_pct']         = (df['accounts'] / TOTAL_ACCOUNTS * 100).round(2)

# ── KEY INSIGHT TABLES ───────────────────────────────────────
below = df[df['below_national_avg']].sort_values('gap_crore', ascending=False)
above = df[~df['below_national_avg']].sort_values('deposit_per_account_rs', ascending=False)

print(f"\n{'='*60}")
print(f"DIGITALLY UNDERSERVED STATES (below national avg ₹{NATIONAL_AVG_RS:,.0f}/account)")
print(f"{'='*60}")
print(f"  Count         : {len(below)} states")
print(f"  Total accounts: {below['accounts'].sum():,} ({below['account_share_pct'].sum():.1f}% of all Jan Dhan)")
print(f"  Total gap     : ₹{below['gap_crore'].sum():,.0f} Crore")
print()
print(below[['state','accounts','deposit_per_account_rs','gap_vs_national_avg_rs','gap_crore','pct_of_national_avg']].to_string(index=False))

print(f"\n{'='*60}")
print(f"TOP 3 STATES BY UNTAPPED POTENTIAL")
print(f"{'='*60}")
top3 = below.head(3)
for _, row in top3.iterrows():
    print(f"  {row['state']:<20} gap=₹{row['gap_crore']:,.0f} Cr | "
          f"₹{row['deposit_per_account_rs']:,.0f}/acc vs national ₹{NATIONAL_AVG_RS:,.0f}")

print(f"\n  Combined top 3 gap: ₹{top3['gap_crore'].sum():,.0f} Crore")


# ── SAVE PROCESSED ───────────────────────────────────────────
df.to_csv("data/processed/financial_inclusion_gap.csv", index=False)
below.to_csv("data/processed/underserved_states.csv", index=False)
print(f"\n  ✓ Saved data/processed/financial_inclusion_gap.csv ({len(df)} rows)")
print(f"  ✓ Saved data/processed/underserved_states.csv ({len(below)} rows)")


# ── CHART ───────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0f0f0f', 'axes.facecolor': '#1a1a1a',
    'axes.edgecolor': '#333', 'text.color': 'white',
    'axes.labelcolor': 'white', 'xtick.color': 'white',
    'ytick.color': 'white', 'grid.color': '#333', 'grid.alpha': 0.4,
})

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Left — Deposit per account by state (horizontal bar)
df_sorted = df.sort_values('deposit_per_account_rs')
colors = ['#E63946' if b else '#06D6A0' for b in df_sorted['below_national_avg']]
axes[0].barh(df_sorted['state'], df_sorted['deposit_per_account_rs'],
             color=colors, edgecolor='none')
axes[0].axvline(NATIONAL_AVG_RS, color='#F4A261', linestyle='--',
                linewidth=1.5, label=f'National avg ₹{NATIONAL_AVG_RS:,.0f}')
axes[0].set_title('Deposit per Jan Dhan Account by State (₹)\nRed = Below National Average',
                  fontsize=11, pad=10)
axes[0].set_xlabel('₹ per Account')
axes[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))
axes[0].legend(fontsize=9, framealpha=0.3)
axes[0].tick_params(axis='y', labelsize=7)

# Right — Top 10 gap states (potential)
top10 = below.head(10)
axes[1].barh(top10['state'][::-1], top10['gap_crore'][::-1],
             color='#E63946', edgecolor='none')
axes[1].set_title('Untapped Deposit Potential — Top 10 States\n(Gap if state reaches national avg)',
                  fontsize=11, pad=10)
axes[1].set_xlabel('Potential Gap (₹ Crore)')
axes[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x:,.0f} Cr'))
axes[1].tick_params(axis='y', labelsize=9)

# Annotate bars
for i, (_, row) in enumerate(top10[::-1].iterrows()):
    axes[1].text(row['gap_crore'] + 30, i, f"₹{row['gap_crore']:,.0f} Cr",
                 va='center', fontsize=8, color='white')

plt.suptitle('India Jan Dhan Financial Inclusion Gap Analysis',
             fontsize=14, y=1.01, fontweight='bold')
plt.tight_layout()
plt.savefig("notebooks/charts/08_financial_inclusion_gap.png", dpi=150, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved notebooks/charts/08_financial_inclusion_gap.png")


# ── SUMMARY ─────────────────────────────────────────────────
print(f"\n{'='*60}")
print("KEY FINDINGS — paste into README / LinkedIn")
print(f"{'='*60}")
print(f"""
  National avg deposit/account : ₹{NATIONAL_AVG_RS:,.0f}
  States below average         : 12 out of 36
  Accounts in these states     : {below['accounts'].sum():,} ({below['account_share_pct'].sum():.1f}% of all Jan Dhan)
  Total untapped potential     : ₹{below['gap_crore'].sum():,.0f} Crore

  Top 3 by gap:
    1. Madhya Pradesh  — ₹{below.iloc[0]['gap_crore']:,.0f} Crore | ₹{below.iloc[0]['deposit_per_account_rs']:,.0f}/acc (only {below.iloc[0]['pct_of_national_avg']:.0f}% of national avg)
    2. Assam           — ₹{below.iloc[1]['gap_crore']:,.0f} Crore | ₹{below.iloc[1]['deposit_per_account_rs']:,.0f}/acc (only {below.iloc[1]['pct_of_national_avg']:.0f}% of national avg)
    3. Bihar           — ₹{below.iloc[2]['gap_crore']:,.0f} Crore | ₹{below.iloc[2]['deposit_per_account_rs']:,.0f}/acc (only {below.iloc[2]['pct_of_national_avg']:.0f}% of national avg)
""")

print("✓ Done. Load to PostgreSQL → run 06_sql_inclusion.py")