"""Step 2: Analysis - KPIs, trends, top products, discount impact, RFM."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "processed" / "clean_sales.csv",
                 parse_dates=["order_date", "ship_date"])
TAB = ROOT / "outputs" / "tables"

# ---- KPIs ----
kpi = {
    "Total Sales": df["sales"].sum(),
    "Total Profit": df["profit"].sum(),
    "Profit Margin %": df["profit"].sum() / df["sales"].sum() * 100,
    "Total Orders": df["order_id"].nunique(),
    "Customers": df["customer_id"].nunique(),
    "Avg Order Value": df.groupby("order_id")["sales"].sum().mean(),
}
for k, v in kpi.items():
    print(f"{k:18}: {v:,.2f}")

# ---- Group-by analysis ----
yearly = df.groupby("year")[["sales", "profit"]].sum()
yearly["growth_%"] = yearly["sales"].pct_change() * 100
by_cat = df.groupby("category")[["sales", "profit"]].sum().sort_values("profit")
by_region = df.groupby("region")[["sales", "profit"]].sum()
top_sub = (df.groupby("sub_category")["profit"].sum()
             .sort_values(ascending=False))
top_prod = (df.groupby("product_name")["sales"].sum()
              .nlargest(10))

print("\nYearly:\n", yearly.round(2))
print("\nBy category:\n", by_cat.round(2))
print("\nTop 10 products:\n", top_prod.round(2))

# ---- Discount ka profit par asar ----
df["discount_band"] = pd.cut(df["discount"], [-0.01, 0, 0.1, 0.2, 0.4, 1],
                             labels=["0%", "1-10%", "11-20%", "21-40%", "40%+"])
disc = df.groupby("discount_band", observed=True)[["sales", "profit"]].sum()
disc["margin_%"] = disc["profit"] / disc["sales"] * 100
print("\nDiscount vs Profit:\n", disc.round(2))
print("Correlation(discount, profit):",
      round(df["discount"].corr(df["profit"]), 3))

# ---- RFM customer segmentation ----
snapshot = df["order_date"].max() + pd.Timedelta(days=1)
rfm = df.groupby("customer_id").agg(
    recency=("order_date", lambda x: (snapshot - x.max()).days),
    frequency=("order_id", "nunique"),
    monetary=("sales", "sum"),
)
rfm["R"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1]).astype(int)
rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"), 4,
                   labels=[1, 2, 3, 4]).astype(int)
rfm["M"] = pd.qcut(rfm["monetary"], 4, labels=[1, 2, 3, 4]).astype(int)
rfm["score"] = rfm["R"] + rfm["F"] + rfm["M"]
rfm["segment"] = pd.cut(rfm["score"], [0, 5, 8, 12],
                        labels=["At Risk", "Regular", "Champions"])
print("\nRFM segments:\n", rfm["segment"].value_counts())

# ---- Tables save karo (dashboard / report me kaam aayenge) ----
yearly.to_csv(TAB / "yearly.csv")
by_cat.to_csv(TAB / "category.csv")
by_region.to_csv(TAB / "region.csv")
disc.to_csv(TAB / "discount_impact.csv")
rfm.to_csv(TAB / "rfm.csv")
print("\nTables saved in outputs/tables/")