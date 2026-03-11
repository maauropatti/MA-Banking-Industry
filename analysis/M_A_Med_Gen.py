"""
Analisi dei Multipli Bancari
-----------------------------
Replicates and improves the original Jupyter notebook analysis.
Run with: python analisi_multipli.py
In VS Code: use the Python Interactive window (# %%) or just run the file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")

# ── Style ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.5,
    "figure.dpi": 120,
})

# ── Colours & groups ─────────────────────────────────────────────────────────
GROUPS = {
    "Banche tradizionali": {
        "banks": ["UniCredit", "Banco BPM", "Intesa Sanpaolo"],
        "color": "#2166ac",
        "marker": "o",
    },
    "Gestori di risparmio": {
        "banks": ["FinecoBank", "Banca Mediolanum", "Banca Generali"],
        "color": "#d6604d",
        "marker": "s",
    },
    "Mediobanca": {
        "banks": ["Mediobanca"],
        "color": "#4dac26",
        "marker": "D",
    },
}

def bank_color(name):
    for g in GROUPS.values():
        if name in g["banks"]:
            return g["color"]
    return "#7f7f7f"

def bank_marker(name):
    for g in GROUPS.values():
        if name in g["banks"]:
            return g["marker"]
    return "o"

# ── Load data ─────────────────────────────────────────────────────────────────
import os
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Dati_Banche.csv")
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()   # strip whitespace from "P/BV "
df = df.rename(columns={"P/BV": "P/B"})

print(f"Loaded {len(df)} observations, {df['Anno'].nunique()} years, {df['Banca'].nunique()} banks\n")
print(df.head(14).to_string(index=False))
print()

# ─────────────────────────────────────────────────────────────────────────────
# Helper: scatter + regression plot
# ─────────────────────────────────────────────────────────────────────────────
def scatter_regression(ax, x, y, nomi, xlabel, ylabel, title):
    """Draw a scatter plot with regression line and bank labels."""
    # Points
    for xi, yi, nome in zip(x, y, nomi):
        ax.scatter(xi, yi,
                   color=bank_color(nome),
                   marker=bank_marker(nome),
                   edgecolors="white", s=90, linewidth=0.8, alpha=0.85, zorder=3)

    # Regression line
    m, b = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min() * 0.95, x.max() * 1.05, 200)
    ax.plot(x_line, m * x_line + b,
            color="black", linestyle="--", linewidth=1.8, label=f"y = {m:.2f}x + {b:.2f}", zorder=2)

    # R²
    y_hat = m * x + b
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    ax.text(0.97, 0.05, f"R² = {r2:.3f}", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="lightgray", alpha=0.8))

    # Bank labels (avoid overlap with a slight vertical offset per year)
    already_labeled = {}
    for xi, yi, nome in zip(x, y, nomi):
        key = nome
        offset_y = already_labeled.get(key, 0)
        ax.annotate(nome, (xi, yi),
                    textcoords="offset points", xytext=(6, 3 + offset_y * 8),
                    fontsize=7, color=bank_color(nome), alpha=0.75)
        already_labeled[key] = already_labeled.get(key, 0) + 1

    # Legend
    legend_handles = [
        Patch(facecolor=g["color"], edgecolor="white", label=label)
        for label, g in GROUPS.items()
    ]
    legend_handles.append(
        plt.Line2D([0], [0], color="black", linestyle="--", linewidth=1.8, label="Regressione lineare")
    )
    ax.legend(handles=legend_handles, fontsize=9, frameon=True, framealpha=0.9)

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=10)

    return m, b, r2

# ─────────────────────────────────────────────────────────────────────────────
# Gap analysis table
# ─────────────────────────────────────────────────────────────────────────────
def gap_table(df, x_col, y_col, m, b, label):
    df = df.copy()
    df[f"{label} atteso"] = m * df[x_col] + b
    df["Gap"] = df[y_col] - df[f"{label} atteso"]

    summary = df.groupby("Banca").agg(
        ROTE_medio=(x_col, "mean"),
        **{f"{label} medio": (y_col, "mean"),
           f"{label} atteso": (f"{label} atteso", "mean"),
           "Gap medio": ("Gap", "mean")}
    ).reset_index().sort_values("Gap medio", ascending=False)

    summary["Giudizio"] = summary["Gap medio"].apply(
        lambda v: "Sopravvalutata" if v > 0.2 else ("Sottovalutata" if v < -0.2 else "Equa")
    )
    return summary

# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — P/E vs ROTE & P/B vs ROTE (side by side)
# ═════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle("Analisi dei Multipli — Banche Italiane", fontsize=17, fontweight="bold", y=1.01)

# P/E
m_pe, b_pe, r2_pe = scatter_regression(
    axes[0],
    x=df["ROTE"], y=df["P/E"], nomi=df["Banca"],
    xlabel="ROTE", ylabel="P/E Ratio",
    title="P/E vs ROTE"
)

# P/B
m_pb, b_pb, r2_pb = scatter_regression(
    axes[1],
    x=df["ROTE"], y=df["P/B"], nomi=df["Banca"],
    xlabel="ROTE", ylabel="P/B Ratio",
    title="P/B vs ROTE"
)

plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "scatter_multipli.png"),
            bbox_inches="tight", dpi=150)
plt.show()

# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Gap analysis bar charts
# ═════════════════════════════════════════════════════════════════════════════
gap_pe = gap_table(df, "ROTE", "P/E", m_pe, b_pe, "P/E")
gap_pb = gap_table(df, "ROTE", "P/B", m_pb, b_pb, "P/B")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Gap di Valutazione — Multiplo Osservato vs Atteso", fontsize=15, fontweight="bold")

for ax, gap_df, label in [(axes[0], gap_pe, "P/E"), (axes[1], gap_pb, "P/B")]:
    colors = ["#d6604d" if v > 0 else "#2166ac" for v in gap_df["Gap medio"]]
    bars = ax.barh(gap_df["Banca"], gap_df["Gap medio"], color=colors,
                   edgecolor="white", height=0.6)
    ax.axvline(0, color="black", linewidth=1.0)
    for bar, val in zip(bars, gap_df["Gap medio"]):
        ax.text(val + (0.005 if val >= 0 else -0.005), bar.get_y() + bar.get_height() / 2,
                f"{val:+.2f}", va="center", ha="left" if val >= 0 else "right", fontsize=9)
    ax.set_title(f"Gap {label} (osservato − atteso)", fontsize=13, fontweight="bold")
    ax.set_xlabel(f"Gap {label}")
    ax.invert_yaxis()

plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "gap_valutazione.png"),
            bbox_inches="tight", dpi=150)
plt.show()

# ═════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Trend multipli per banca (P/E e P/B nel tempo)
# ═════════════════════════════════════════════════════════════════════════════
banks = sorted(df["Banca"].unique())
n = len(banks)
fig, axes = plt.subplots(2, n // 2 + n % 2, figsize=(20, 10), sharey=False)
axes = axes.flatten()
fig.suptitle("Evoluzione Multipli per Banca (2022–2027)", fontsize=15, fontweight="bold")

for i, bank in enumerate(banks):
    sub = df[df["Banca"] == bank].sort_values("Anno")
    ax = axes[i]
    ax2 = ax.twinx()
    color = bank_color(bank)
    ax.plot(sub["Anno"], sub["P/E"], color=color, marker="o", linewidth=2, label="P/E")
    ax2.plot(sub["Anno"], sub["P/B"], color=color, marker="s", linestyle="--",
             linewidth=2, alpha=0.7, label="P/B")
    ax.set_title(bank, fontsize=11, fontweight="bold", color=color)
    ax.set_ylabel("P/E", fontsize=9, color=color)
    ax2.set_ylabel("P/B", fontsize=9, color=color)
    ax.tick_params(axis="x", rotation=45)
    ax.set_xticks(sub["Anno"])
    # Mini legend
    lines = [plt.Line2D([0], [0], color=color, marker="o", label="P/E"),
             plt.Line2D([0], [0], color=color, marker="s", linestyle="--", label="P/B")]
    ax.legend(handles=lines, fontsize=8, framealpha=0.7)

# Hide unused axes
for j in range(len(banks), len(axes)):
    axes[j].set_visible(False)

plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "trend_multipli.png"),
            bbox_inches="tight", dpi=150)
plt.show()

# ═════════════════════════════════════════════════════════════════════════════
# Console output — Gap tables & OLS summaries
# ═════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("  GAP DI VALUTAZIONE — P/E")
print("=" * 60)
print(gap_pe.to_string(index=False, float_format="{:.3f}".format))

print("\n" + "=" * 60)
print("  GAP DI VALUTAZIONE — P/B")
print("=" * 60)
print(gap_pb.to_string(index=False, float_format="{:.3f}".format))

# Predictions at ROTE = 20%
rote_test = 0.20
print(f"\n{'='*60}")
print(f"  PREVISIONE per ROTE = {rote_test:.0%}")
print(f"{'='*60}")
print(f"  P/E atteso : {m_pe * rote_test + b_pe:.2f}")
print(f"  P/B atteso : {m_pb * rote_test + b_pb:.2f}")

# OLS summaries
print("\n" + "=" * 60)
print("  OLS — P/E ~ ROTE")
print("=" * 60)
X = sm.add_constant(df["ROTE"])
print(sm.OLS(df["P/E"], X).fit().summary())

print("\n" + "=" * 60)
print("  OLS — P/B ~ ROTE")
print("=" * 60)
print(sm.OLS(df["P/B"], X).fit().summary())

print("\nCharts saved to: scatter_multipli.png, gap_valutazione.png, trend_multipli.png")
