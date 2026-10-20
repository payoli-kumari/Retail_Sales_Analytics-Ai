"""Step 1: Data Cleaning - raw CSV ko analysis-ready banana."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "superstore.csv"
OUT = ROOT / "data" / "processed" / "clean_sales.csv"

# Global Superstore me dates "31-07-2012" (din-mahina-saal) hoti hain -> True
DATE_DAYFIRST = True

# 1) Load (is file me latin-1 encoding lagti hai)
try:
    df = pd.read_csv(RAW)
except UnicodeDecodeError:
    df = pd.read_csv(RAW, encoding="latin-1")
print("Shape before:", df.shape)

# 2) Column names ko saaf karo: "Sub-Category" -> "sub_category"
df.columns = (df.columns.str.strip().str.lower()
              .str.replace(" ", "_").str.replace("-", "_"))

# 3) Missing values aur duplicates
print("\nMissing values:\n", df.isna().sum()[df.isna().sum() > 0])
before = len(df)
df = df.drop_duplicates()
print("Duplicates removed:", before - len(df))

# 4) Date columns ko datetime me badlo
df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=DATE_DAYFIRST, errors="coerce")
df["ship_date"] = pd.to_datetime(df["ship_date"], dayfirst=DATE_DAYFIRST, errors="coerce")
df = df.dropna(subset=["order_date", "sales"])

# 5) Text columns me extra spaces / case theek karo
text_cols = ["segment", "region", "category", "sub_category",
             "state", "city", "ship_mode"]
for c in text_cols:
    if c in df.columns:  # jo column file me nahi hai use skip karo
        df[c] = df[c].astype(str).str.strip().str.title()

# 6) Invalid rows hatao
df = df[(df["sales"] > 0) & (df["quantity"] > 0)]

# 7) Feature engineering (naye useful columns)
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%b")
df["quarter"] = df["order_date"].dt.quarter
df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
df["profit_margin_pct"] = (df["profit"] / df["sales"] * 100).round(2)
df["is_loss"] = df["profit"] < 0

# 8) Outlier flag (IQR method) - delete nahi, sirf flag karte hain
q1, q3 = df["sales"].quantile([0.25, 0.75])
iqr = q3 - q1
df["sales_outlier"] = (df["sales"] > q3 + 1.5 * iqr) | (df["sales"] < q1 - 1.5 * iqr)

df.to_csv(OUT, index=False)
print("\nShape after:", df.shape)
print("Saved ->", OUT)