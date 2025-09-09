#!/usr/bin/env python3
"""
Simple Tableau Data Preparation Script
Salomón Santiago Esquivel - Data Analyst Portfolio

Creates simplified CSV datasets for Tableau visualization
Uses pandas calculations instead of complex SQL
"""

import sqlite3
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Database connection
db_path = '../data/market_intelligence.db'

def create_tableau_datasets_simple():
    """Create optimized datasets for Tableau dashboards using pandas"""
    
    if not os.path.exists(db_path):
        print("Database not found. Run database_loader.py first.")
        return
    
    conn = sqlite3.connect(db_path)
    print("Preparing Tableau datasets...")
    
    # Load all data with specific columns to avoid duplicates
    prices_query = """
    SELECT 
        sp.symbol,
        sp.company,
        sp.date,
        sp.open_price,
        sp.high_price,
        sp.low_price,
        sp.close_price,
        sp.volume,
        sp.daily_change,
        sp.daily_change_abs,
        sp.volatility_30d,
        sp.ma_7,
        sp.ma_30,
        sp.volume_ma_7,
        sp.volume_ratio,
        sp.daily_range,
        cf.market_cap,
        cf.revenue,
        cf.employees,
        cf.sector,
        cf.industry,
        cf.country,
        cf.website
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= date('2025-09-01', '-90 days')
    """
    
    df = pd.read_sql_query(prices_query, conn)
    conn.close()
    
    # Ensure tableau directory exists
    os.makedirs('../tableau', exist_ok=True)
    
    # 1. Executive Summary Dataset
    executive_df = df.copy()
    executive_df['market_cap_billions'] = executive_df['market_cap'] / 1000000000
    executive_df['daily_return_pct'] = executive_df['daily_change'] * 100
    executive_df['volume_millions'] = executive_df['volume'] / 1000000
    executive_df['volatility_pct'] = executive_df['volatility_30d'] * 100
    
    # Performance categories
    executive_df['performance_category'] = pd.cut(
        executive_df['daily_change'],
        bins=[-np.inf, -0.02, 0, 0.02, np.inf],
        labels=['Strong Down', 'Down', 'Up', 'Strong Up']
    )
    
    # Risk categories
    executive_df['risk_category'] = pd.cut(
        executive_df['volatility_30d'],
        bins=[0, 0.025, 0.04, np.inf],
        labels=['Low Risk', 'Medium Risk', 'High Risk']
    )
    
    exec_cols = [
        'symbol', 'company', 'sector', 'market_cap_billions', 'date',
        'close_price', 'daily_return_pct', 'volume_millions', 'volatility_pct',
        'ma_7', 'ma_30', 'performance_category', 'risk_category'
    ]
    
    executive_df[exec_cols].to_csv('../tableau/executive_summary.csv', index=False)
    print(f"Executive Summary: {len(executive_df)} records")
    
    # 2. Competitive Analysis Dataset
    competitors = ['LNVGY', 'AAPL', 'MSFT', 'HPQ', 'DELL', 'IBM']
    comp_df = df[df['symbol'].isin(competitors)].copy()
    
    # Calculate metrics by company
    comp_metrics = comp_df.groupby(['symbol', 'company', 'sector', 'market_cap']).agg({
        'daily_change': ['mean', 'std'],
        'close_price': ['min', 'max'],
        'volume': 'mean'
    }).round(6)
    
    comp_metrics.columns = ['avg_daily_return', 'volatility', 'min_price', 'max_price', 'avg_volume']
    comp_metrics = comp_metrics.reset_index()
    
    # Calculate additional metrics
    comp_metrics['market_cap_billions'] = comp_metrics['market_cap'] / 1000000000
    comp_metrics['avg_daily_return_pct'] = comp_metrics['avg_daily_return'] * 100
    comp_metrics['volatility_pct'] = comp_metrics['volatility'] * 100
    comp_metrics['total_return_pct'] = ((comp_metrics['max_price'] - comp_metrics['min_price']) / comp_metrics['min_price']) * 100
    comp_metrics['avg_volume_millions'] = comp_metrics['avg_volume'] / 1000000
    comp_metrics['company_type'] = comp_metrics['symbol'].apply(lambda x: 'Lenovo' if x == 'LNVGY' else 'Competitor')
    
    # Rankings
    comp_metrics['performance_rank'] = comp_metrics['avg_daily_return_pct'].rank(ascending=False)
    comp_metrics['stability_rank'] = comp_metrics['volatility_pct'].rank(ascending=True)
    
    # Positive days calculation
    positive_days = comp_df[comp_df['daily_change'] > 0].groupby('symbol').size()
    total_days = comp_df.groupby('symbol').size()
    comp_metrics['positive_days_pct'] = (positive_days / total_days * 100).fillna(0)
    
    comp_metrics.to_csv('../tableau/competitive_analysis.csv', index=False)
    print(f"Competitive Analysis: {len(comp_metrics)} records")
    
    # 3. Risk Analysis Dataset (sample of daily data)
    risk_df = df.copy()
    risk_df['daily_return_pct'] = risk_df['daily_change'] * 100
    risk_df['volatility_pct'] = risk_df['volatility_30d'] * 100
    risk_df['volume_millions'] = risk_df['volume'] / 1000000
    risk_df['market_cap_billions'] = risk_df['market_cap'] / 1000000000
    risk_df['portfolio_weight_pct'] = (risk_df['market_cap'] / risk_df['market_cap'].sum()) * 100
    
    # Risk levels
    risk_df['risk_level'] = pd.cut(
        risk_df['volatility_30d'],
        bins=[0, 0.015, 0.025, 0.04, np.inf],
        labels=['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk']
    )
    
    risk_cols = [
        'symbol', 'company', 'sector', 'date', 'daily_return_pct', 
        'volatility_pct', 'volume_millions', 'market_cap_billions',
        'portfolio_weight_pct', 'risk_level'
    ]
    
    risk_df[risk_cols].to_csv('../tableau/risk_analysis.csv', index=False)
    print(f"Risk Analysis: {len(risk_df)} records")
    
    # 4. Time Series Dataset
    ts_df = df.copy()
    ts_df['volume_millions'] = ts_df['volume'] / 1000000
    ts_df['daily_return_pct'] = ts_df['daily_change'] * 100
    
    # Calculate cumulative returns by company
    ts_df = ts_df.sort_values(['symbol', 'date'])
    ts_df['cumulative_return_pct'] = 0.0
    
    for symbol in ts_df['symbol'].unique():
        mask = ts_df['symbol'] == symbol
        prices = ts_df.loc[mask, 'close_price'].values
        if len(prices) > 0:
            base_price = prices[0]
            ts_df.loc[mask, 'cumulative_return_pct'] = ((prices / base_price) - 1) * 100
    
    ts_cols = [
        'date', 'symbol', 'company', 'sector', 'close_price',
        'daily_return_pct', 'volume_millions', 'ma_7', 'ma_30',
        'cumulative_return_pct'
    ]
    
    ts_df[ts_cols].to_csv('../tableau/timeseries_data.csv', index=False)
    print(f"Time Series Data: {len(ts_df)} records")
    
    print("\nAll Tableau datasets ready!")
    print("Files created in: market-intelligence-dashboard/tableau/")
    
    return {
        'executive': len(executive_df),
        'competitive': len(comp_metrics),
        'risk': len(risk_df),
        'timeseries': len(ts_df)
    }

if __name__ == "__main__":
    print("Tableau Data Preparation (Simplified)")
    print("=" * 40)
    results = create_tableau_datasets_simple()
    
    print("\n" + "="*50)
    print("TABLEAU DATA PREPARATION COMPLETE")
    print("="*50)
    print("Ready for dashboard creation!")
    print("\nNext steps:")
    print("1. Open Tableau Public")
    print("2. Connect to CSV files in tableau/ folder")
    print("3. Follow dashboard creation guide")