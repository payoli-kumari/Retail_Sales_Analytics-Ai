"""Step 3: Static charts (report ke liye PNG)."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "processed" / "clean_sales.csv",
                 parse_dates=["order_date"])
OUT = ROOT / "outputs" / "charts"
sns.set_theme(style="whitegrid")

# 1) Monthly sales trend
m = df.groupby("year_month")["sales"].sum()
plt.figure(figsize=(10, 4))
m.plot(marker="o")
plt.title("Monthly Sales Trend"); plt.xticks(rotation=60)
plt.tight_layout(); plt.savefig(OUT / "monthly_trend.png", dpi=150); plt.close()

# 2) Category-wise sales vs profit
c = df.groupby("category")[["sales", "profit"]].sum().reset_index()
plt.figure(figsize=(7, 5))
sns.barplot(data=c.melt("category"), x="category", y="value", hue="variable")
plt.title("Sales vs Profit by Category")
plt.tight_layout(); plt.savefig(OUT / "category.png", dpi=150); plt.close()

# 3) Discount vs profit scatter
plt.figure(figsize=(7, 5))
sns.scatterplot(data=df.sample(min(2000, len(df)), random_state=1),
                x="discount", y="profit", alpha=0.4)
plt.title("Discount vs Profit")
plt.tight_layout(); plt.savefig(OUT / "discount_vs_profit.png", dpi=150); plt.close()

# 4) Correlation heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(df[["sales", "quantity", "discount", "profit"]].corr(),
            annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.tight_layout(); plt.savefig(OUT / "correlation.png", dpi=150); plt.close()

print("Charts saved in outputs/charts/")