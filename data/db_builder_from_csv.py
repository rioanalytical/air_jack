import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime
import pandas  as pd
import os 

# ----------------------------
# CONFIG
# ----------------------------
list_of_file = os.listdir("./equities/")
list_of_file
DB_NAME = "market_data.db"
TABLE_NAME = "stock_prices"

START_DATE = "2000-01-01"
END_DATE = datetime.today().strftime("%Y-%m-%d")


# ----------------------------
# SQLITE SETUP
# ----------------------------
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    date TEXT NOT NULL,
    ticker TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    PRIMARY KEY (date, ticker)
)
""")

# Performance tuning (safe)
cursor.execute("PRAGMA journal_mode=WAL;")
cursor.execute("PRAGMA synchronous=NORMAL;")

conn.commit()

# ----------------------------
# DOWNLOAD DATA
# ----------------------------
for i in list_of_file:
    print("⏳ Downloading data from NAS...", i)
    
    df = pd.read_csv("./equities/" + i)
    
    if df.empty:
        continue
    if df.shape[0] < 3:
        continue
    
    # ----------------------------
    # NORMALIZE DATA
    # ----------------------------
    # Convert multi-index columns -> rows
    df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    df['Ticker'] = i.split(".")[0]
    df.drop(df.index[:2], inplace=True)
    df = df[['Ticker','Date', 'Close', 'High', 'Low', 'Open', 'Volume']]
        
    # Drop rows with no volume (market holidays, bad symbols)
    df = df.dropna(subset=["Volume"])
    
    print(f"🚀 Prepared {len(df):,} rows for insertion")
    
    # ----------------------------
    # INSERT INTO SQLITE
    # ----------------------------
    insert_query = f"""
    INSERT OR IGNORE INTO {TABLE_NAME}
    (date, ticker, open, high, low, close, volume)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.executemany(
        insert_query,
        df[["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]].values.tolist()
    )
    
    conn.commit()
    
    
    print("✅ Data successfully stored in SQLite", i)
conn.close()
