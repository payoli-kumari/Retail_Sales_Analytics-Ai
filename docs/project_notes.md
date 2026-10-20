# Project Notes

Dataset: Global Superstore, 51,290 rows, covering the years 2011 to 2014. After cleaning, the number of columns went from 24 to 33.

Cleaning steps: checked for duplicates (none found), converted dates to datetime, removed extra spaces from text columns, removed invalid rows (sales or quantity zero or negative), and flagged outliers instead of deleting them so that information about large orders is not lost.

The postal code column has many missing values, but it is not needed for the analysis, so it was left untouched.

Discount analysis showed that as the discount increases, the profit margin falls. At 0 percent discount the margin was 25.3 percent, at 21 to 40 percent discount it was minus 17.3 percent, and above 40 percent it was minus 74.1 percent. The correlation between discount and profit is minus 0.316.

In the Furniture category, sales were 41.1 lakh but profit was only 2.85 lakh (margin 6.9 percent), while the Technology margin was 14.0 percent.

Sales grew from 22.6 lakh in 2011 to 43.0 lakh in 2014. Total sales were 1.26 crore, total profit was 14.67 lakh, and the overall profit margin was 11.61 percent.

Customer segmentation (RFM) found 696 Champions, 390 Regular and 504 At Risk customers.

The dashboard is built with Streamlit and has Year, Region and Category filters. The data comes from a CSV file cleaned by the Python scripts.

Forecasting used the Holt-Winters model to predict the next 6 months of sales, and accuracy was checked by hiding the last 6 months. The backtest error (MAPE) was 13.4 percent.

The AI layer has three features: Ask the Data (turns a question into pandas code), Ask the Project (RAG, answers from the project notes), and AI Insights (an automatic summary of the filtered numbers).

Recommendations to increase profit (3 recommendations): first, control high discounts; second, improve the Furniture margin; third, win back At Risk customers.

Recommendation 1 to increase profit, control high discounts: orders with a discount above 20 percent have a negative average margin (21-40 percent discount: -17.3, above 40 percent: -74.1), so limiting very high discounts can raise profit.

Recommendation 2 to increase profit, improve the Furniture margin: Furniture has sales of 41.1 lakh but a margin of only 6.9 percent, compared with 14.0 percent for Technology, so Furniture pricing and costs should be reviewed.

Recommendation 3 to increase profit, win back At Risk customers: the RFM analysis found 504 At Risk customers, so targeted offers can bring them back. These are suggestions based on the analysis, not proven causes.

Limitations of this project: the AI can make mistakes (hallucination), the free API has rate limits, and the document search uses TF-IDF, which only matches words and does not understand meaning.

More limitations: the forecast is only an estimate (backtest MAPE 13.4 percent), the discount and profit relationship is a correlation of -0.316 which does not prove cause, and the code execution safety is basic, so a production system would need a proper sandbox.

What is this project (project overview): This project analyses retail sales data with Python and shows the results in a Streamlit dashboard. It has three layers: analytics, a dashboard, and an AI layer that answers questions and writes insights.

Dataset description (what data was used): The project uses the real Global Superstore dataset with 51,290 rows and 24 columns, covering orders from 2011 to 2014. After cleaning it has 33 columns.

Dashboard features (what can the dashboard do): The dashboard has four tabs: Dashboard, Ask the Data, Ask the Project (RAG), and AI Insights. The sidebar has filters for Year, Region, and Category.

Filters (what do the filters change): The filters change the KPIs, all charts, the data table, Ask the Data, and AI Insights. Ask the Project is not affected by the filters because it answers only from the documents.

Key numbers (KPIs, total sales, total profit): Total sales were 12,642,501.91 and total profit was 1,467,457.29, giving a profit margin of 11.61 percent. There were 25,035 orders from 1,590 customers, and the average order value was 504.99.

Yearly sales growth (sales by year): Sales were 22.6 lakh in 2011, 26.8 lakh in 2012, 34.1 lakh in 2013, and 43.0 lakh in 2014. Yearly growth was 18.5 percent, 27.2 percent, and 26.3 percent.

Category performance (which category is best): Technology had sales of 47.4 lakh, profit of 6.64 lakh, and a margin of 14.0 percent. Office Supplies had sales of 37.9 lakh, profit of 5.18 lakh, and a margin of 13.7 percent. Furniture had sales of 41.1 lakh, profit of 2.85 lakh, and the lowest margin of 6.9 percent.

Discount and profit (effect of discount on margin): The average margin was 25.3 for no discount, 17.2 for 1-10 percent, 9.9 for 11-20 percent, -17.3 for 21-40 percent, and -74.1 for above 40 percent discount. The correlation between discount and profit is -0.316, which shows a relationship but does not prove cause.

Customer segments (RFM analysis result): The RFM analysis found 696 Champions, 390 Regular customers, and 504 At Risk customers.

Top product (best selling product): The top product by sales is Apple Smart Phone, Full Size, with sales of 86,935.78.

Forecast method (how was the forecast made): The forecast uses the Holt-Winters model on 48 months of data. Its accuracy was checked by hiding the last 6 months, which gave a backtest error (MAPE) of 13.4 percent.

Forecast values (sales forecast for 2015): The forecast for January to June 2015 is about 362k, 321k, 378k, 363k, 420k, and 518k. The forecast is only an estimate.

Tables sub-category (should Tables be stopped): The Tables sub-category had sales of 147,131 and a loss of 11,075, which is a margin of -7.5 percent. Tables also had an average discount of about 0.30, compared with 0.15 for the other sub-categories.

How Ask the Data works (how does the AI answer data questions): The AI receives only the column names and 3 sample rows, then writes pandas code. The code runs on the filtered data, the number comes from pandas, and the code is shown so the answer can be verified.

How Ask the Project works (what is RAG): The documents are split into paragraphs, and TF-IDF finds the 3 paragraphs most similar to the question. Only those paragraphs are given to the AI, and it must answer only from them.

How AI Insights works (how are insights made): The dashboard calculates a summary with pandas, including rankings by sales and profit. The AI then writes 5 key insights and 3 business recommendations from that summary.

Future scope (what can be improved): Future improvements include embeddings with ChromaDB for better document search, KMeans clustering on RFM, IsolationForest for anomaly detection, a SQL layer, a local Ollama model, and deployment.