import os
import time
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

# Directory to store stock data
DATA_DIR = "/Users/username/Downloads"
FILE_PATH = os.path.join(DATA_DIR, "stock_data.csv")

# Top 10 Companies (Adjust as needed)
TOP_COMPANIES = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK-B", "JPM", "V"]

def fetch_stock_data():
    """Fetches stock data for the top 10 companies, processes it, and saves to CSV."""
    
    print("Fetching new stock data...")
    
    # Fetch latest stock data
    data = yf.download(TOP_COMPANIES, period="1d", interval="5m")  # 5-minute interval for recent data
    
    # Extract relevant columns
    latest_prices = data['Close'].iloc[-1]  # Last row (latest price)
    prev_prices = data['Close'].iloc[-2]  # Previous close for % change
    
    # Calculate % Change
    percent_change = ((latest_prices - prev_prices) / prev_prices) * 100

    # Calculate Moving Average (5)
    moving_avg_5 = data['Close'].rolling(window=5).mean().iloc[-1]

    # Calculate Volatility (Standard Deviation over last 5 intervals)
    volatility = data['Close'].rolling(window=5).std().iloc[-1]

    # Identify anomalies (if % change > 2%)
    anomalies = np.where(abs(percent_change) > 2, "YES", "NO")

    # Get current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create DataFrame
    stock_df = pd.DataFrame({
        "Date": current_time,  # Same timestamp for all rows
        "Symbol": TOP_COMPANIES,
        "Price ($)": latest_prices.values,
        "% Change": percent_change.values,
        "Moving Avg (5)": moving_avg_5.values,
        "Volatility": volatility.values,
        "Anomaly": anomalies
    })
    
    # Ensure directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Remove old file
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)

    # Save new data
    stock_df.to_csv(FILE_PATH, index=False)
    print(f"Stock data updated and saved to {FILE_PATH}\n")

# Infinite loop to refresh data every 30 seconds
while True:
    fetch_stock_data()
    time.sleep(30)  # Wait 30 seconds before fetching again
