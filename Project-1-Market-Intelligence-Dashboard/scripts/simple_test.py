#!/usr/bin/env python3
"""
Simple API Test - Market Intelligence Dashboard
Salomon Santiago Esquivel
"""

import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from config import ALPHA_VANTAGE_API_KEY

def test_apis():
    print("Market Intelligence Dashboard - API Test")
    print("=" * 50)
    
    # Test Yahoo Finance
    print("Testing Yahoo Finance API...")
    try:
        ticker = yf.Ticker("AAPL")
        hist = ticker.history(period="5d")
        print(f"SUCCESS: Yahoo Finance working! Latest AAPL close: ${hist['Close'].iloc[-1]:.2f}")
    except Exception as e:
        print(f"ERROR: Yahoo Finance failed - {e}")
    
    # Test Alpha Vantage
    print("\nTesting Alpha Vantage API...")
    try:
        ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
        data, meta_data = ts.get_daily('AAPL', outputsize='compact')
        print(f"SUCCESS: Alpha Vantage working! Retrieved {len(data)} days of data")
        print(f"Latest AAPL close: ${data['4. close'].iloc[0]:.2f}")
    except Exception as e:
        print(f"ERROR: Alpha Vantage failed - {e}")
    
    # Test multiple companies
    print("\nTesting multiple companies...")
    companies = ['AAPL', 'MSFT', 'LNVGY', 'IBM', 'NVDA']
    
    for symbol in companies:
        try:
            ticker = yf.Ticker(symbol)
            price = ticker.history(period="1d")['Close'].iloc[-1]
            print(f"  {symbol}: ${price:.2f}")
        except:
            print(f"  {symbol}: Failed to get data")
    
    print("\nAPI tests completed!")
    print("Ready to start building the data collection system!")

if __name__ == "__main__":
    test_apis()