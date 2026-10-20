"""Step 4 (Advanced): Next 6 months ki sales ka forecast (Holt-Winters)."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "processed" / "clean_sales.csv",
                 parse_dates=["order_date"])

# Har mahine ki total sales (MS = month start)
monthly = df.set_index("order_date")["sales"].resample("MS").sum()
print("Months of data:", len(monthly))  # seasonal model ke liye 24+ chahiye

# Model train karo aur agle 6 mahine predict karo
model = ExponentialSmoothing(monthly, trend="add", seasonal="add",
                             seasonal_periods=12).fit()
forecast = model.forecast(6)

# Accuracy check: last 6 mahine chhupa ke predict karo
train, test = monthly[:-6], monthly[-6:]
m2 = ExponentialSmoothing(train, trend="add", seasonal="add",
                          seasonal_periods=12).fit()
mape = ((m2.forecast(6) - test).abs() / test).mean() * 100
print(f"Backtest error (MAPE): {mape:.1f}%")

forecast.rename("forecast_sales").to_csv(ROOT / "outputs" / "tables" / "forecast.csv")

plt.figure(figsize=(10, 4))
monthly.plot(label="Actual")
forecast.plot(label="Forecast (6 months)", style="--")
plt.legend(); plt.title("Sales Forecast")
plt.tight_layout()
plt.savefig(ROOT / "outputs" / "charts" / "forecast.png", dpi=150)
print(forecast.round(0))