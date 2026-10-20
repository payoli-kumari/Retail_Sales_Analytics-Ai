# Data Dictionary

sales: total sales amount (revenue) of one order line. This dataset has no currency column.

profit: profit of that order line; a negative value means a loss.

discount: discount given on the order line, between 0 and 1 (0.2 means 20 percent).

profit_margin_pct: profit divided by sales, multiplied by 100 (shown as a percentage).

shipping_days: ship_date minus order_date, which is the number of days taken to ship the order.

year_month: year and month of the order in YYYY-MM format, created for trend charts.

is_loss: True if the order has negative profit, otherwise False.

sales_outlier: True if the order's sales value is unusually high or low according to the IQR method. It is only a flag, and the row is not deleted.

RFM: Recency (how recently the customer bought), Frequency (how often they bought), Monetary (how much they spent). Together they create the customer segments Champions, Regular and At Risk.

Profit margin: profit margin is profit divided by sales, multiplied by 100. It shows how much profit is earned from every 100 of sales.

Discount: the discount column is a fraction, so 0.20 means a 20 percent discount. A higher discount usually lowers the profit margin.

Order line: each row in the data is one order line, which is one product in an order. One order can have several order lines, so the number of order lines is larger than the number of orders.

Lakh and crore: lakh and crore are used only to make large numbers easy to read. One lakh is 100,000 and one crore is 10,000,000. The dataset has no currency, so these numbers are plain values without a currency symbol.

KPI: a KPI (key performance indicator) is an important number used to track business performance. This project shows total sales, total profit, profit margin, and number of orders as KPIs.

Correlation: correlation measures how strongly two numbers move together, from -1 to 1. A correlation does not prove that one thing causes the other.

Holt-Winters: Holt-Winters is a forecasting method that uses the level, trend, and seasonality of past monthly sales to estimate future sales.

Backtest and MAPE: a backtest hides the last months of data, forecasts them, and compares the forecast with the real values. MAPE (mean absolute percentage error) is the average percentage error of that comparison; a lower MAPE means a better forecast.

TF-IDF: TF-IDF is a method that turns text into numbers based on word importance. This project uses it to find the paragraphs most similar to a question, so it matches words and does not understand meaning.

Columns overview (list of all columns): the cleaned data has 33 columns. The 24 original columns are row_id, order_id, order_date, ship_date, ship_mode, customer_id, customer_name, segment, city, state, country, postal_code, market, region, product_id, category, sub_category, product_name, sales, quantity, discount, profit, shipping_cost and order_priority. Cleaning added 9 new columns: year, month, month_name, quarter, year_month, shipping_days, profit_margin_pct, is_loss and sales_outlier.

row_id: a running number that identifies each row in the original data file. Each row is one order line.

order_id: the identifier of the order. One order can contain several order lines, so the same order_id can appear in more than one row.

order_date: the date on which the order was placed.

ship_date: the date on which the order was shipped.

ship_mode: the shipping method used to deliver the order.

customer_id: the identifier of the customer who placed the order.

customer_name: the name of the customer who placed the order.

segment: the customer segment, which is the type of customer group the customer belongs to.

city: the city to which the order was delivered.

state: the state or province to which the order was delivered.

country: the country to which the order was delivered.

postal_code: the postal code of the delivery address. This is the only column with missing values (41,296 missing).

market: the larger market group that the order belongs to, which is a bigger group than the region.

region: the sales region of the order. The dashboard Region filter uses this column.

product_id: the identifier of the product that was sold.

category: the main product category. The dashboard Category filter uses this column.

sub_category: the more detailed product group inside a category, for example Tables inside Furniture.

product_name: the name of the product that was sold.

quantity: the number of units of the product sold in that order line.

shipping_cost: the cost of shipping that order line.

order_priority: the priority level assigned to the order.

year: the year of the order, taken from order_date. The dashboard Year filter uses this column.

month: the month number of the order, taken from order_date.

month_name: the name of the month of the order, taken from order_date.

quarter: the quarter of the year in which the order was placed, taken from order_date.