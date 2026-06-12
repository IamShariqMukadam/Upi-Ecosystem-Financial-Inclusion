"""
02_eda_visualizations.py
Generates all 7 EDA charts. Saves PNGs to notebooks/charts/
Run after 01_clean_engineer.py

CHARTS:
  1. UPI Volume Growth 2019–2026 (area by era, annotated)
  2. Average Ticket Size over time
  3. YoY Growth % + Banks on UPI
  4. Monthly Seasonality Heatmap
  5. Volume vs Value divergence (dual axis)
  6. Era Comparison (3-panel bar)
  7. P2P vs P2M shift (stacked area + share line)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import os

os.makedirs("notebooks/charts", exist_ok=True)

# ── Style ──────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0f0f0f',
    'axes.facecolor':   '#1a1a1a',
    'axes.edgecolor':   '#333',
    'text.color':       'white',
    'axes.labelcolor':  'white',
    'xtick.color':      'white',
    'ytick.color':      'white',
    'grid.color':       '#333',
    'grid.alpha':       0.5,
    'font.family':      'sans-serif',
})

ERA_COLORS = {
    '1_Post-Demonetization Growth': '#fdcb6e',
    '2_COVID Impact':               '#e17055',
    '3_Post-COVID Surge':           '#00b894',
    '4_Maturity Phase':             '#0984e3',
}

# ── Load data ──────────────────────────────────────────────
print("Loading processed data...")
upi = pd.read_csv("data/processed/upi_clean.csv", parse_dates=['date'])

try:
    p2p = pd.read_csv("data/processed/p2p_p2m_clean.csv", parse_dates=['date'])
    has_p2p = len(p2p) > 5
except Exception:
    has_p2p = False

print(f"  UPI : {len(upi)} rows | {upi['date'].min().date()} → {upi['date'].max().date()}")
print(f"  P2P : {len(p2p) if has_p2p else 'N/A'} rows")


# ============================================================
# CHART 1 — UPI Volume Growth 2019–2026 (annotated, era-coloured)
# ============================================================
print("\n[1/7] UPI Volume Growth...")

fig, ax = plt.subplots(figsize=(15, 6))

for era in sorted(upi['era'].unique()):
    subset = upi[upi['era'] == era]
    color  = ERA_COLORS.get(era, '#ffffff')
    ax.fill_between(subset['date'], subset['volume_crore'], alpha=0.35, color=color)
    ax.plot(subset['date'], subset['volume_crore'], color=color, linewidth=2)

# Annotations — only events within data range (Nov 2019–Mar 2026)
key_events = [
    ('2020-03-24', 'COVID\nLockdown',     0.18),
    ('2021-08-01', '3Bn/month\nMilestone',0.40),
    ('2023-08-01', '10Bn/month\nMilestone',0.65),
]
y_max = upi['volume_crore'].max()
for date_str, label, y_frac in key_events:
    xpos = pd.Timestamp(date_str)
    if upi['date'].min() <= xpos <= upi['date'].max():
        ax.axvline(xpos, color='white', linestyle='--', alpha=0.35, linewidth=1)
        ax.text(xpos, y_max * y_frac, label, fontsize=8, color='white',
                ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='#333', alpha=0.7))

patches = [mpatches.Patch(color=ERA_COLORS[e], label=e.split('_', 1)[1])
           for e in sorted(ERA_COLORS) if e in upi['era'].values]
ax.legend(handles=patches, loc='upper left', fontsize=8, framealpha=0.3)

ax.set_title('India UPI Transaction Volume — Nov 2019 to Mar 2026 (Monthly, Crore Transactions)', fontsize=13, pad=12)
ax.set_ylabel('Transactions (Crore)')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f} Cr'))
ax.grid(True, axis='y')
plt.tight_layout()
plt.savefig("notebooks/charts/01_upi_volume_growth.png", dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 01_upi_volume_growth.png")


# ============================================================
# CHART 2 — Average Ticket Size Over Time
# ============================================================
print("[2/7] Avg Ticket Size...")

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(upi['date'], upi['avg_ticket_size_rs'], color='#00cec9', linewidth=2)
ax.fill_between(upi['date'], upi['avg_ticket_size_rs'], alpha=0.2, color='#00cec9')
ax.plot(upi['date'], upi['avg_ticket_size_rs'].rolling(12).mean(),
        color='#fd79a8', linewidth=2, linestyle='--', label='12-month rolling avg')

peak = upi.loc[upi['avg_ticket_size_rs'].idxmax()]
ax.annotate(f"Peak ₹{peak['avg_ticket_size_rs']:.0f}\n{peak['date'].strftime('%b %Y')}",
            xy=(peak['date'], peak['avg_ticket_size_rs']),
            xytext=(peak['date'], peak['avg_ticket_size_rs'] + 80),
            fontsize=8, color='white',
            arrowprops=dict(arrowstyle='->', color='white', lw=1))

ax.set_title('Average UPI Transaction Size (₹) — The Micro-Payment Story', fontsize=13)
ax.set_ylabel('Avg Ticket Size (₹)')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))
ax.legend(fontsize=9, framealpha=0.3)
ax.grid(True, axis='y')
plt.tight_layout()
plt.savefig("notebooks/charts/02_avg_ticket_size.png", dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 02_avg_ticket_size.png")


# ============================================================
# CHART 3 — YoY Volume Growth % + Banks on UPI
# ============================================================
print("[3/7] YoY Growth + Banks...")

yearly = upi.groupby('year').agg(
    total_volume=('volume_crore', 'sum'),
    avg_banks=('banks_live_on_upi', 'mean')
).reset_index()
yearly['yoy_growth'] = yearly['total_volume'].pct_change() * 100

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: YoY bars
colors = ['#e17055' if (not np.isnan(x) and x < 0) else '#00b894'
          for x in yearly['yoy_growth'].fillna(0)]
axes[0].bar(yearly['year'].astype(str), yearly['yoy_growth'].fillna(0),
            color=colors, edgecolor='none')
axes[0].axhline(0, color='white', linewidth=0.5)
axes[0].set_title('Year-over-Year Volume Growth %', fontsize=12)
axes[0].set_ylabel('YoY Growth %')
for yr, val in zip(yearly['year'], yearly['yoy_growth'].fillna(0)):
    if not np.isnan(val):
        axes[0].text(str(yr), val + (3 if val >= 0 else -8), f'{val:.0f}%',
                     ha='center', fontsize=9, color='white')

# Right: Banks on UPI
valid_banks = upi.dropna(subset=['banks_live_on_upi'])
axes[1].plot(valid_banks['date'], valid_banks['banks_live_on_upi'],
             color='#a29bfe', linewidth=2)
axes[1].fill_between(valid_banks['date'], valid_banks['banks_live_on_upi'],
                     alpha=0.3, color='#a29bfe')
axes[1].set_title('Banks Live on UPI Over Time', fontsize=12)
axes[1].set_ylabel('Number of Banks')
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}'))
axes[1].grid(True, axis='y')

plt.tight_layout()
plt.savefig("notebooks/charts/03_yoy_growth_banks.png", dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 03_yoy_growth_banks.png")


# ============================================================
# CHART 4 — Monthly Seasonality Heatmap
# ============================================================
print("[4/7] Seasonality Heatmap...")

month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
pivot = upi.pivot_table(values='volume_crore', index='year', columns='month_name', aggfunc='sum')
pivot = pivot.reindex(columns=[m for m in month_order if m in pivot.columns])
# Data starts Nov 2019, so 2019 only has Nov+Dec — keep it (shows launch ramp)

fig, ax = plt.subplots(figsize=(14, 6))
sns.heatmap(pivot, cmap='YlOrRd', annot=True, fmt='.0f',
            linewidths=0.5, ax=ax,
            cbar_kws={'label': 'Volume (Crore Transactions)'})
ax.set_title('UPI Monthly Volume Heatmap — Seasonal Patterns (Crore Transactions)', fontsize=13)
ax.set_xlabel('')
ax.set_ylabel('Year')
plt.tight_layout()
plt.savefig("notebooks/charts/04_seasonality_heatmap.png", dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 04_seasonality_heatmap.png")


# ============================================================
# CHART 5 — Volume vs Value Divergence (dual axis)
# ============================================================
print("[5/7] Volume vs Value...")

fig, ax1 = plt.subplots(figsize=(14, 5))
ax2 = ax1.twinx()

ax1.plot(upi['date'], upi['volume_crore'], color='#0984e3', linewidth=2, label='Volume (Crore Txns)')
ax2.plot(upi['date'], upi['value_crore'],  color='#e84393', linewidth=2,
         linestyle='--', label='Value (₹ Crore)')

ax1.set_ylabel('Volume (Crore Transactions)', color='#0984e3')
ax2.set_ylabel('Value (₹ Crore)',             color='#e84393')
ax1.tick_params(axis='y', labelcolor='#0984e3')
ax2.tick_params(axis='y', labelcolor='#e84393')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f} Cr'))
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1e5:,.1f}L Cr'))

lines  = ax1.get_legend_handles_labels()[0] + ax2.get_legend_handles_labels()[0]
labels = ax1.get_legend_handles_labels()[1] + ax2.get_legend_handles_labels()[1]
ax1.legend(lines, labels, loc='upper left', framealpha=0.3)
ax1.set_title('UPI Volume vs Value — Growing Volume, Declining Ticket Size', fontsize=13)
ax1.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig("notebooks/charts/05_volume_vs_value.png", dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 05_volume_vs_value.png")


# ============================================================
# CHART 6 — Era Comparison (3-panel)
# ============================================================
print("[6/7] Era Comparison...")

era_stats = upi.groupby('era').agg(
    avg_monthly_vol=('volume_crore',    'mean'),
    avg_ticket=     ('avg_ticket_size_rs','mean'),
    avg_mom_growth= ('volume_mom_pct',  'mean'),
    months=         ('volume_crore',    'count')
).reset_index()
era_stats['era_label'] = era_stats['era'].str.split('_', n=1).str[1]
colors = [ERA_COLORS.get(e, '#fff') for e in era_stats['era']]

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

axes[0].barh(era_stats['era_label'], era_stats['avg_monthly_vol'], color=colors)
axes[0].set_title('Avg Monthly Volume (Crore)', fontsize=11)
axes[0].set_xlabel('Crore Transactions')

axes[1].barh(era_stats['era_label'], era_stats['avg_ticket'], color=colors)
axes[1].set_title('Avg Ticket Size (₹)', fontsize=11)
axes[1].set_xlabel('₹')
axes[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x:,.0f}'))

axes[2].barh(era_stats['era_label'], era_stats['avg_mom_growth'].fillna(0), color=colors)
axes[2].axvline(0, color='white', linewidth=0.5)
axes[2].set_title('Avg Month-over-Month Growth %', fontsize=11)
axes[2].set_xlabel('%')

fig.suptitle('UPI Performance by Era — How Each Phase Differs', fontsize=13, y=1.01)
plt.tight_layout()
plt.savefig("notebooks/charts/06_era_comparison.png", dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ 06_era_comparison.png")


# ============================================================
# CHART 7 — P2P vs P2M Shift
# ============================================================
print("[7/7] P2P vs P2M...")

if has_p2p and 'p2m_vol_crore' in p2p.columns:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Stacked area
    axes[0].stackplot(
        p2p['date'],
        p2p['p2p_vol_crore'],
        p2p['p2m_vol_crore'],
        labels=['P2P (Personal Transfer)', 'P2M (Merchant Payment)'],
        colors=['#636e72', '#00b894'],
        alpha=0.8
    )
    axes[0].set_title('P2P vs P2M Volume — Stacked (Crore)', fontsize=11)
    axes[0].legend(loc='upper left', fontsize=9, framealpha=0.3)
    axes[0].set_ylabel('Volume (Crore Transactions)')
    axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f} Cr'))

    # P2M share trend
    axes[1].plot(p2p['date'], p2p['p2m_share_pct'], color='#00b894', linewidth=2)
    axes[1].fill_between(p2p['date'], p2p['p2m_share_pct'], alpha=0.2, color='#00b894')
    axes[1].axhline(50, color='white', linestyle='--', alpha=0.5, label='50% threshold')
    axes[1].set_title('Merchant Payment (P2M) Share % Over Time', fontsize=11)
    axes[1].set_ylabel('P2M Share %')
    axes[1].legend(fontsize=9, framealpha=0.3)
    axes[1].grid(True, axis='y')

    plt.tight_layout()
    plt.savefig("notebooks/charts/07_p2p_vs_p2m.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("  ✓ 07_p2p_vs_p2m.png")
else:
    print("  ✗ Skipped — p2p data missing or wrong columns")

# ============================================================
# KEY INSIGHTS (paste into README)
# ============================================================
first = upi.iloc[0]
latest = upi.iloc[-1]
print("\n" + "=" * 60)
print("KEY INSIGHTS — paste into README")
print("=" * 60)
peak_t = upi.loc[upi['avg_ticket_size_rs'].idxmax()]
print(f"""
GROWTH: {first['volume_crore']:.2f} Cr (Nov 2019) → {latest['volume_crore']:.2f} Cr ({latest['date'].strftime('%b %Y')})
        = {latest['volume_crore']/first['volume_crore']:.0f}x growth in {(latest['year'] - first['year'])} years

TICKET: Peak ₹{peak_t['avg_ticket_size_rs']:.0f} in {peak_t['date'].strftime('%b %Y')}
        → ₹{latest['avg_ticket_size_rs']:.0f} in {latest['date'].strftime('%b %Y')}
        (UPI now powers micro-transactions, not just bank transfers)

BANKS:  {int(upi['banks_live_on_upi'].dropna().iloc[0])} at start
        → {int(upi["banks_live_on_upi"].dropna().iloc[-1])} in {upi.dropna(subset=["banks_live_on_upi"]).iloc[-1]["date"].strftime("%b %Y")}

RUN RT: {latest['annualized_volume_bn']:.1f} Bn transactions/year (annualized from {latest['date'].strftime('%b %Y')})
""")

print("✓ All 7 charts saved to notebooks/charts/")
print("  Run 03_load_postgres.py next.")