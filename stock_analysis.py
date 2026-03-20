import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# ---------------------------
# STEP 1: Download Data
# ---------------------------
df = yf.download("TCS.NS", start="2020-01-01", end="2024-12-31")

# Fix multi-level columns
df.columns = df.columns.get_level_values(0)

# ---------------------------
# STEP 2: Clean Data
# ---------------------------
df.dropna(inplace=True)
df.reset_index(inplace=True)

# ---------------------------
# STEP 3: Feature Engineering
# ---------------------------
df['MA50'] = df['Close'].rolling(window=50).mean()
df['MA200'] = df['Close'].rolling(window=200).mean()

df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

# 🔥 IMPORTANT DEBUG
print("FINAL COLUMNS BEFORE SAVE:", df.columns)

# ---------------------------
# STEP 4: Visualization
# ---------------------------
df_plot = df.tail(300)

plt.figure(figsize=(10,5))
plt.plot(df_plot['Date'], df_plot['Close'], label='Close Price')
plt.plot(df_plot['Date'], df_plot['MA50'], label='MA50')
plt.plot(df_plot['Date'], df_plot['MA200'], label='MA200')

plt.legend()
plt.title("Stock Price Analysis (TCS)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()

plt.figure(figsize=(10,5))
plt.plot(df_plot['Date'], df_plot['Volume'])
plt.title("Trading Volume")
plt.xlabel("Date")
plt.ylabel("Volume")
plt.show()

# ---------------------------
# STEP 5: SQL ANALYSIS
# ---------------------------
conn = sqlite3.connect("stock.db")

df.to_sql("stock_data", conn, if_exists="replace", index=False)

query = """
SELECT 
    Year,
    AVG(Close) AS Avg_Price
FROM stock_data
GROUP BY Year
"""

result = pd.read_sql(query, conn)
print("\nYear-wise Average Price:\n", result)

# ---------------------------
# STEP 6: SAVE FINAL CSV (LAST STEP)
# ---------------------------
df.to_csv("stock_data.csv", index=False)
