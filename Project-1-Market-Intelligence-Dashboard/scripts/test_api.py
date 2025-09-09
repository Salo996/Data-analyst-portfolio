#!/usr/bin/env python3
"""
API Connection Test - Market Intelligence Dashboard
Salomón Santiago Esquivel - Data Analyst Portfolio Project
"""

import sys
import requests
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from config import ALPHA_VANTAGE_API_KEY, TECH_COMPANIES

def test_alpha_vantage():
    """Test Alpha Vantage API connection"""
    print("🔌 Testing Alpha Vantage API...")
    
    try:
        ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
        data, meta_data = ts.get_daily('AAPL', outputsize='compact')
        
        print(f"✅ Alpha Vantage API working!")
        print(f"📊 Retrieved {len(data)} days of AAPL data")
        print(f"📅 Latest date: {data.index[0]}")
        print(f"💰 Latest close price: ${data['4. close'].iloc[0]:.2f}")
        return True
        
    except Exception as e:
        print(f"❌ Alpha Vantage API Error: {e}")
        return False

def test_yahoo_finance():
    """Test Yahoo Finance API (yfinance)"""
    print("\n🔌 Testing Yahoo Finance API...")
    
    try:
        ticker = yf.Ticker("AAPL")
        hist = ticker.history(period="5d")
        
        print(f"✅ Yahoo Finance API working!")
        print(f"📊 Retrieved {len(hist)} days of AAPL data")
        print(f"📅 Latest date: {hist.index[-1].strftime('%Y-%m-%d')}")
        print(f"💰 Latest close price: ${hist['Close'].iloc[-1]:.2f}")
        return True
        
    except Exception as e:
        print(f"❌ Yahoo Finance API Error: {e}")
        return False

def test_company_data():
    """Test data retrieval for our target companies"""
    print(f"\n📈 Testing data for {len(TECH_COMPANIES)} target companies...")
    
    successful = 0
    failed = 0
    
    for symbol, name in list(TECH_COMPANIES.items())[:5]:  # Test first 5 companies
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            print(f"✅ {symbol} ({name}): ${info.get('currentPrice', 'N/A')}")
            successful += 1
        except Exception as e:
            print(f"❌ {symbol} ({name}): Error - {str(e)[:50]}...")
            failed += 1
    
    print(f"\n📊 Results: {successful} successful, {failed} failed")
    return successful, failed

def main():
    """Run all API tests"""
    print("🚀 Market Intelligence Dashboard - API Test")
    print("=" * 50)
    
    # Test APIs
    alpha_success = test_alpha_vantage()
    yahoo_success = test_yahoo_finance()
    companies_success, companies_failed = test_company_data()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print(f"Alpha Vantage API: {'✅ Working' if alpha_success else '❌ Failed'}")
    print(f"Yahoo Finance API: {'✅ Working' if yahoo_success else '❌ Failed'}")
    print(f"Company Data: {companies_success}/{companies_success + companies_failed} working")
    
    if alpha_success or yahoo_success:
        print("\n🎉 Ready to start data collection!")
        print("Next step: Run data_collector.py")
    else:
        print("\n⚠️  Please check your API keys and internet connection")

if __name__ == "__main__":
    main()