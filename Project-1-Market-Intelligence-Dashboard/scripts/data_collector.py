#!/usr/bin/env python3
"""
Market Intelligence Data Collector
Salomon Santiago Esquivel - Data Analyst Portfolio Project

This script collects stock market data for competitive intelligence analysis.
Focus: Technology companies and Lenovo competitors
"""

import pandas as pd
import yfinance as yf
import requests
import json
from datetime import datetime, timedelta
from alpha_vantage.timeseries import TimeSeries
from config import ALPHA_VANTAGE_API_KEY, TECH_COMPANIES, ANALYSIS_CONFIG

class MarketDataCollector:
    """Collect and process market intelligence data"""
    
    def __init__(self):
        self.companies = TECH_COMPANIES
        self.av_ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
        self.data_path = '../data/'
        
    def collect_daily_prices(self, symbol, period='90d'):
        """Collect daily stock prices using Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                print(f"  WARNING: No data for {symbol}")
                return None
                
            # Add company info
            hist['Symbol'] = symbol
            hist['Company'] = self.companies[symbol]
            hist['Date'] = hist.index
            
            print(f"  SUCCESS: {symbol} - {len(hist)} days")
            return hist
            
        except Exception as e:
            print(f"  ERROR: {symbol} - {str(e)[:100]}")
            return None
    
    def collect_company_fundamentals(self, symbol):
        """Collect company fundamental data"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            fundamentals = {
                'Symbol': symbol,
                'Company': self.companies[symbol],
                'MarketCap': info.get('marketCap', 0),
                'Revenue': info.get('totalRevenue', 0),
                'Employees': info.get('fullTimeEmployees', 0),
                'Sector': info.get('sector', 'Technology'),
                'Industry': info.get('industry', 'Unknown'),
                'Country': info.get('country', 'Unknown'),
                'Website': info.get('website', ''),
                'CollectionDate': datetime.now().strftime('%Y-%m-%d')
            }
            
            return fundamentals
            
        except Exception as e:
            print(f"  ERROR: Fundamentals for {symbol} - {str(e)[:50]}")
            return None
    
    def calculate_market_metrics(self, price_data):
        """Calculate key market intelligence metrics"""
        try:
            # Price volatility (30-day)
            price_data['Volatility_30d'] = price_data['Close'].rolling(window=30).std()
            
            # Price changes
            price_data['Daily_Change'] = price_data['Close'].pct_change()
            price_data['Daily_Change_Abs'] = price_data['Close'].diff()
            
            # Moving averages
            price_data['MA_7'] = price_data['Close'].rolling(window=7).mean()
            price_data['MA_30'] = price_data['Close'].rolling(window=30).mean()
            
            # Volume analysis
            price_data['Volume_MA_7'] = price_data['Volume'].rolling(window=7).mean()
            price_data['Volume_Ratio'] = price_data['Volume'] / price_data['Volume_MA_7']
            
            # High-Low range
            price_data['Daily_Range'] = ((price_data['High'] - price_data['Low']) / price_data['Close']) * 100
            
            return price_data
            
        except Exception as e:
            print(f"  ERROR: Calculating metrics - {e}")
            return price_data
    
    def collect_all_data(self):
        """Main function to collect all market data"""
        print(f"Starting data collection for {len(self.companies)} companies...")
        print("=" * 60)
        
        all_price_data = []
        all_fundamentals = []
        
        for i, (symbol, name) in enumerate(self.companies.items(), 1):
            print(f"[{i}/{len(self.companies)}] Processing {symbol} ({name})...")
            
            # Collect price data
            price_data = self.collect_daily_prices(symbol)
            if price_data is not None:
                # Calculate metrics
                price_data = self.calculate_market_metrics(price_data)
                all_price_data.append(price_data)
            
            # Collect fundamentals
            fundamentals = self.collect_company_fundamentals(symbol)
            if fundamentals is not None:
                all_fundamentals.append(fundamentals)
        
        return all_price_data, all_fundamentals
    
    def save_data(self, all_price_data, all_fundamentals):
        """Save collected data to CSV files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save price data
        if all_price_data:
            combined_prices = pd.concat(all_price_data, ignore_index=True)
            price_filename = f'{self.data_path}stock_prices_{timestamp}.csv'
            combined_prices.to_csv(price_filename, index=False)
            print(f"\nSaved price data: {price_filename}")
            print(f"Total records: {len(combined_prices)}")
        
        # Save fundamentals
        if all_fundamentals:
            fundamentals_df = pd.DataFrame(all_fundamentals)
            fundamentals_filename = f'{self.data_path}company_fundamentals_{timestamp}.csv'
            fundamentals_df.to_csv(fundamentals_filename, index=False)
            print(f"Saved fundamentals: {fundamentals_filename}")
            print(f"Total companies: {len(fundamentals_df)}")
        
        # Create latest files (for consistent access)
        if all_price_data:
            latest_prices = f'{self.data_path}stock_prices_latest.csv'
            combined_prices.to_csv(latest_prices, index=False)
            
        if all_fundamentals:
            latest_fundamentals = f'{self.data_path}company_fundamentals_latest.csv'
            fundamentals_df.to_csv(latest_fundamentals, index=False)
        
        return len(all_price_data), len(all_fundamentals)
    
    def generate_summary_report(self, companies_processed, fundamentals_collected):
        """Generate data collection summary"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""
MARKET INTELLIGENCE DATA COLLECTION REPORT
==========================================
Collection Date: {timestamp}
Analyst: Salomon Santiago Esquivel

SUMMARY:
- Target Companies: {len(self.companies)}
- Price Data Collected: {companies_processed} companies
- Fundamentals Collected: {fundamentals_collected} companies
- Data Period: {ANALYSIS_CONFIG['lookback_days']} days
- Success Rate: {(companies_processed/len(self.companies))*100:.1f}%

COMPANIES TRACKED:
"""
        
        for symbol, name in self.companies.items():
            report += f"  {symbol}: {name}\n"
        
        report += f"""
NEXT STEPS:
1. Load data into SQL database for analysis
2. Create competitive intelligence dashboard
3. Analyze market trends and correlations
4. Generate business insights report

Data files saved in: {self.data_path}
"""
        
        # Save report
        report_filename = f'{self.data_path}collection_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        with open(report_filename, 'w') as f:
            f.write(report)
        
        print(report)
        print(f"Report saved: {report_filename}")

def main():
    """Main execution function"""
    collector = MarketDataCollector()
    
    # Collect all data
    all_price_data, all_fundamentals = collector.collect_all_data()
    
    # Save data
    companies_processed, fundamentals_collected = collector.save_data(all_price_data, all_fundamentals)
    
    # Generate report
    collector.generate_summary_report(companies_processed, fundamentals_collected)
    
    print("\nDATA COLLECTION COMPLETED!")
    print("Ready for SQL analysis and dashboard creation.")

if __name__ == "__main__":
    main()