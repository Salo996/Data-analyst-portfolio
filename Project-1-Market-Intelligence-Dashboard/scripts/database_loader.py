#!/usr/bin/env python3
"""
Database Loader Script
Salomón Santiago Esquivel - Data Analyst Portfolio

Converts CSV data to SQLite database for SQL analysis
"""

import sqlite3
import pandas as pd
import glob
import os
from datetime import datetime

def load_data_to_database():
    """Load CSV data into SQLite database"""
    
    # Find the most recent data files
    price_files = glob.glob('../data/stock_prices_*.csv')
    fundamentals_files = glob.glob('../data/company_fundamentals_*.csv')
    
    if not price_files or not fundamentals_files:
        print("No data files found. Run data_collector.py first.")
        return
    
    # Get the most recent files
    latest_price_file = max(price_files, key=os.path.getctime)
    latest_fundamentals_file = max(fundamentals_files, key=os.path.getctime)
    
    print(f"Loading data from:")
    print(f"  Prices: {latest_price_file}")
    print(f"  Fundamentals: {latest_fundamentals_file}")
    
    # Create database directory
    os.makedirs('../data', exist_ok=True)
    
    # Connect to database
    db_path = '../data/market_intelligence.db'
    conn = sqlite3.connect(db_path)
    
    try:
        # Load and process stock prices
        print("\nLoading stock prices...")
        prices_df = pd.read_csv(latest_price_file)
        
        # Rename columns to match database schema
        column_mapping = {
            'Open': 'open_price',
            'High': 'high_price', 
            'Low': 'low_price',
            'Close': 'close_price',
            'Volume': 'volume',
            'Symbol': 'symbol',
            'Company': 'company',
            'Date': 'date',
            'Daily_Change': 'daily_change',
            'Daily_Change_Abs': 'daily_change_abs',
            'Volatility_30d': 'volatility_30d',
            'MA_7': 'ma_7',
            'MA_30': 'ma_30',
            'Volume_MA_7': 'volume_ma_7',
            'Volume_Ratio': 'volume_ratio',
            'Daily_Range': 'daily_range'
        }
        
        prices_df = prices_df.rename(columns=column_mapping)
        
        # Convert date column
        prices_df['date'] = pd.to_datetime(prices_df['date']).dt.date
        
        # Create stock_prices table
        prices_df.to_sql('stock_prices', conn, if_exists='replace', index=False)
        print(f"  Loaded {len(prices_df)} price records")
        
        # Load and process company fundamentals
        print("Loading company fundamentals...")
        fundamentals_df = pd.read_csv(latest_fundamentals_file)
        
        # Rename columns to match database schema
        fundamentals_mapping = {
            'Symbol': 'symbol',
            'Company': 'company',
            'MarketCap': 'market_cap',
            'Revenue': 'revenue',
            'Employees': 'employees',
            'Sector': 'sector',
            'Industry': 'industry',
            'Country': 'country',
            'Website': 'website',
            'CollectionDate': 'collection_date'
        }
        
        fundamentals_df = fundamentals_df.rename(columns=fundamentals_mapping)
        
        # Convert date column
        fundamentals_df['collection_date'] = pd.to_datetime(fundamentals_df['collection_date']).dt.date
        
        # Create company_fundamentals table
        fundamentals_df.to_sql('company_fundamentals', conn, if_exists='replace', index=False)
        print(f"  Loaded {len(fundamentals_df)} company records")
        
        # Create indexes for performance
        print("Creating database indexes...")
        cursor = conn.cursor()
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_stock_symbol_date ON stock_prices(symbol, date)",
            "CREATE INDEX IF NOT EXISTS idx_stock_date ON stock_prices(date)",
            "CREATE INDEX IF NOT EXISTS idx_stock_symbol ON stock_prices(symbol)",
            "CREATE INDEX IF NOT EXISTS idx_fundamentals_symbol ON company_fundamentals(symbol)",
            "CREATE INDEX IF NOT EXISTS idx_fundamentals_sector ON company_fundamentals(sector)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        conn.commit()
        print("  Database indexes created")
        
        # Verify data
        print("\nDatabase verification:")
        cursor.execute("SELECT COUNT(*) FROM stock_prices")
        price_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM company_fundamentals")
        fundamentals_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT symbol) FROM stock_prices")
        unique_companies = cursor.fetchone()[0]
        
        print(f"  Stock prices: {price_count} records")
        print(f"  Company fundamentals: {fundamentals_count} records")
        print(f"  Unique companies: {unique_companies}")
        
        print(f"\nDatabase created successfully: {db_path}")
        
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Market Intelligence Database Loader")
    print("=" * 40)
    load_data_to_database()
    print("\nDatabase ready for SQL analysis!")