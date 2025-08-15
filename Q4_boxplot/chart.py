# chart.py
# Requirements satisfied:
# - Uses seaborn, matplotlib.pyplot, pandas (and numpy for data gen)
# - Generates realistic synthetic data (10,000 rows)
# - Creates a Seaborn boxplot
# - Professional styling via sns.set_style / sns.set_context
# - Figure size 8x8 inches -> 512x512 px at dpi=64
# - Saves as chart.png with bbox_inches='tight'

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# 1) Synthetic data generation
# -----------------------------
np.random.seed(42)

n = 10_000
methods = ["Cash", "Debit Card", "Credit Card", "Online Payment"]
# plausible channel mix (adjust as needed)
weights = [0.28, 0.32, 0.25, 0.15]
choices = np.random.choice(methods, size=n, p=weights)

# lognormal params chosen to mimic realistic spend distributions (right-skewed)
params = {
    "Cash":            dict(mean=4.55, sigma=0.48),  # median ~ 94
    "Debit Card":      dict(mean=4.90, sigma=0.45),  # median ~ 134
    "Credit Card":     dict(mean=5.15, sigma=0.55),  # median ~ 172
    "Online Payment":  dict(mean=4.80, sigma=0.50),  # median ~ 122
}

def sample_amount(method):
    m, s = params[method]["mean"], params[method]["sigma"]
    # lognormal -> positive, right-skewed; clip to a sensible retail range
    val = np.random.lognormal(mean=m, sigma=s)
    val = np.clip(val, 5, 1000)
    return round(float(val), 2)

amounts = [sample_amount(m) for m in choices]

df = pd.DataFrame({
    "PurchaseAmount": amounts,
    "PaymentMethod": choices
})

# optional sanity check to ensure we really have 10,000 rows
assert len(df) == 10_000, "Expected 10,000 rows"

# --------------------------------
# 2) Seaborn styling & boxplot
# --------------------------------
sns.set_style("whitegrid")               # professional look
sns.set_context("talk")                  # presentation-ready text sizes

order = ["Cash", "Debit Card", "Credit Card", "Online Payment"]
palette = sns.color_palette("Set2", n_colors=len(order))

# exact pixel output: 8in * 64 dpi = 512 px
fig = plt.figure(figsize=(8, 8), dpi=64)

ax = sns.boxplot(
    data=df,
    x="PaymentMethod",
    y="PurchaseAmount",
    order=order,
    palette=palette,
    width=0.6,
    showfliers=True,      # set False if you want a cleaner central spread
    linewidth=1.5
)

ax.set_title("Customer Spend by Payment Method (n=10,000)", pad=14, weight="bold")
ax.set_xlabel("Payment Method")
ax.set_ylabel("Purchase Amount")

# tidy up axes
sns.despine(offset=10, trim=True)
ax.tick_params(axis='x', rotation=10)

# --------------------------------
# 3) Save the chart (exact size)
# --------------------------------
plt.tight_layout()
plt.savefig("chart.png", dpi=64, bbox_inches="tight")
plt.close(fig)

# Also save the data in case you want it in the Colab pane
df.to_csv("synthetic_purchases.csv", index=False)
print("Saved chart.png (512x512) and synthetic_purchases.csv")
