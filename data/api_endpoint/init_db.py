"""
Initialize SQLite database with sample market data
Run this script to set up the database for the Flask API
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_database(db_path="market_data.db"):
    """Create SQLite database with schema"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_prices (
        date TEXT NOT NULL,
        ticker TEXT NOT NULL,
        open REAL NOT NULL,
        high REAL NOT NULL,
        low REAL NOT NULL,
        close REAL NOT NULL,
        volume INTEGER NOT NULL,
        PRIMARY KEY (date, ticker)
    )
    """)
    
    # Create indexes for fast queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ticker ON stock_prices(ticker)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON stock_prices(date)")
    
    conn.commit()
    print(f"✓ Database schema created at {db_path}")
    return conn


def generate_synthetic_data(ticker, start_date, num_days=252, initial_price=100):
    """Generate realistic synthetic OHLCV data"""
    dates = []
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []
    
    current_date = start_date
    current_price = initial_price
    
    for _ in range(num_days):
        # Skip weekends
        if current_date.weekday() >= 5:
            current_date += timedelta(days=1)
            continue
        
        dates.append(current_date.strftime("%Y-%m-%d"))
        
        # Generate realistic OHLCV
        daily_return = np.random.normal(0.0005, 0.015)  # mean, std
        close_price = current_price * (1 + daily_return)
        
        open_price = current_price
        high_price = max(open_price, close_price) * (1 + abs(np.random.normal(0, 0.008)))
        low_price = min(open_price, close_price) * (1 - abs(np.random.normal(0, 0.008)))
        
        opens.append(round(open_price, 2))
        highs.append(round(high_price, 2))
        lows.append(round(low_price, 2))
        closes.append(round(close_price, 2))
        
        # Volume with some autocorrelation
        volume = int(np.random.normal(50_000_000, 10_000_000))
        volume = max(volume, 1_000_000)  # Minimum volume
        volumes.append(volume)
        
        current_price = close_price
        current_date += timedelta(days=1)
    
    return pd.DataFrame({
        "date": dates,
        "ticker": ticker,
        "open": opens,
        "high": highs,
        "low": lows,
        "close": closes,
        "volume": volumes
    })


def insert_data(conn, df):
    """Insert data into database"""
    df.to_sql('stock_prices', conn, if_exists='append', index=False)
    print(f"✓ Inserted {len(df)} rows for {df['ticker'].iloc[0]}")


def populate_sample_data(conn):
    """Populate database with sample data for common tickers"""
    tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    start_date = datetime(2023, 1, 1)
    
    print("\nGenerating synthetic data for tickers...")
    
    for ticker in tickers:
        df = generate_synthetic_data(ticker, start_date, num_days=252)
        insert_data(conn, df)
    
    conn.commit()


def verify_database(conn):
    """Verify database contents"""
    cursor = conn.cursor()
    
    # Count records per ticker
    cursor.execute("SELECT ticker, COUNT(*) as count FROM stock_prices GROUP BY ticker")
    results = cursor.fetchall()
    
    print("\nDatabase verification:")
    print("Ticker | Record Count | Date Range")
    print("-------|--------------|-------------------")
    
    for ticker, count in results:
        cursor.execute(
            "SELECT MIN(date), MAX(date) FROM stock_prices WHERE ticker = ?",
            (ticker,)
        )
        min_date, max_date = cursor.fetchone()
        print(f"{ticker:6} | {count:12} | {min_date} to {max_date}")
    
    cursor.execute("SELECT COUNT(*) FROM stock_prices")
    total = cursor.fetchone()[0]
    print(f"\nTotal records: {total}")


if __name__ == "__main__":
    print("=== Market Data Database Setup ===\n")
    
    # Create database
    conn = create_database()
    
    # Populate with sample data
    populate_sample_data(conn)
    
    # Verify
    verify_database(conn)
    
    conn.close()
    print("\n✓ Database setup complete! Ready to run Flask app.")
