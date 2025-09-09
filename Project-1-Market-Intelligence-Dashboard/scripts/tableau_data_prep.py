#!/usr/bin/env python3
"""
Tableau Data Preparation Script
Salomón Santiago Esquivel - Data Analyst Portfolio

Prepares market intelligence data for Tableau visualization
Creates optimized CSV exports for dashboard creation
"""

import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta

# Database connection
db_path = '../data/market_intelligence.db'

def create_tableau_datasets():
    """Create optimized datasets for Tableau dashboards"""
    
    if not os.path.exists(db_path):
        print("Database not found. Run data_collector.py first.")
        return
    
    conn = sqlite3.connect(db_path)
    print("Preparing Tableau datasets...")
    
    # 1. Executive Summary Dataset
    executive_query = """
    SELECT 
        cf.symbol,
        cf.company,
        cf.sector,
        cf.market_cap/1000000000 as market_cap_billions,
        sp.date,
        sp.close_price,
        sp.daily_change * 100 as daily_return_pct,
        sp.volume/1000000 as volume_millions,
        sp.volatility_30d * 100 as volatility_pct,
        sp.ma_7 as ma_7_days,
        sp.ma_30 as ma_30_days,
        -- Performance indicators
        CASE 
            WHEN sp.daily_change > 0.02 THEN 'Strong Up'
            WHEN sp.daily_change > 0 THEN 'Up'
            WHEN sp.daily_change < -0.02 THEN 'Strong Down'
            ELSE 'Down'
        END as performance_category,
        -- Risk categories
        CASE 
            WHEN sp.volatility_30d > 0.04 THEN 'High Risk'
            WHEN sp.volatility_30d > 0.025 THEN 'Medium Risk'
            ELSE 'Low Risk'
        END as risk_category
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= date('2025-09-01', '-90 days')
    ORDER BY sp.date DESC, cf.market_cap DESC
    """
    
    executive_df = pd.read_sql_query(executive_query, conn)
    executive_df.to_csv('../tableau/executive_summary.csv', index=False)
    print(f"Executive Summary: {len(executive_df)} records")
    
    # 2. Competitive Analysis Dataset
    competitive_query = """
    WITH competitor_metrics AS (
        SELECT 
            cf.symbol,
            cf.company,
            cf.sector,
            cf.market_cap/1000000000 as market_cap_billions,
            AVG(sp.daily_change * 100) as avg_daily_return_pct,
            STDDEV(sp.daily_change * 100) as volatility_pct,
            (MAX(sp.close_price) - MIN(sp.close_price)) / MIN(sp.close_price) * 100 as total_return_pct,
            AVG(sp.volume/1000000) as avg_volume_millions,
            COUNT(CASE WHEN sp.daily_change > 0 THEN 1 END) * 100.0 / COUNT(*) as positive_days_pct,
            -- Lenovo specific indicator
            CASE WHEN cf.symbol = 'LNVGY' THEN 'Lenovo' ELSE 'Competitor' END as company_type
        FROM stock_prices sp
        JOIN company_fundamentals cf ON sp.symbol = cf.symbol
        WHERE sp.date >= date('2025-09-01', '-90 days')
        AND cf.symbol IN ('LNVGY', 'AAPL', 'MSFT', 'HPQ', 'DELL', 'IBM')
        GROUP BY cf.symbol, cf.company, cf.sector, cf.market_cap
    )
    SELECT 
        *,
        RANK() OVER (ORDER BY avg_daily_return_pct DESC) as performance_rank,
        RANK() OVER (ORDER BY volatility_pct ASC) as stability_rank
    FROM competitor_metrics
    """
    
    competitive_df = pd.read_sql_query(competitive_query, conn)
    competitive_df.to_csv('../tableau/competitive_analysis.csv', index=False)
    print(f"Competitive Analysis: {len(competitive_df)} records")
    
    # 3. Risk Analysis Dataset
    risk_query = """
    WITH risk_metrics AS (
        SELECT 
            cf.symbol,
            cf.company,
            cf.sector,
            sp.date,
            sp.daily_change * 100 as daily_return_pct,
            sp.volatility_30d * 100 as volatility_pct,
            sp.volume/1000000 as volume_millions,
            cf.market_cap/1000000000 as market_cap_billions,
            -- VaR approximation (95% confidence)
            AVG(sp.daily_change * 100) OVER (PARTITION BY sp.symbol ORDER BY sp.date ROWS 29 PRECEDING) - 
            (1.645 * AVG(sp.daily_change * 100) OVER (PARTITION BY sp.symbol ORDER BY sp.date ROWS 29 PRECEDING)) as var_95_pct,
            -- Sector weight
            cf.market_cap / (SELECT SUM(market_cap) FROM company_fundamentals) * 100 as portfolio_weight_pct
        FROM stock_prices sp
        JOIN company_fundamentals cf ON sp.symbol = cf.symbol
        WHERE sp.date >= date('2025-09-01', '-90 days')
    )
    SELECT 
        *,
        CASE 
            WHEN volatility_pct > 4 THEN 'Very High Risk'
            WHEN volatility_pct > 2.5 THEN 'High Risk'
            WHEN volatility_pct > 1.5 THEN 'Medium Risk'
            ELSE 'Low Risk'
        END as risk_level
    FROM risk_metrics
    """
    
    risk_df = pd.read_sql_query(risk_query, conn)
    risk_df.to_csv('../tableau/risk_analysis.csv', index=False)
    print(f"Risk Analysis: {len(risk_df)} records")
    
    # 4. Time Series Dataset for Trends
    timeseries_query = """
    SELECT 
        sp.date,
        cf.symbol,
        cf.company,
        cf.sector,
        sp.close_price,
        sp.daily_change * 100 as daily_return_pct,
        sp.volume/1000000 as volume_millions,
        sp.ma_7 as ma_7_days,
        sp.ma_30 as ma_30_days,
        -- Cumulative returns
        (sp.close_price / FIRST_VALUE(sp.close_price) OVER (PARTITION BY sp.symbol ORDER BY sp.date) - 1) * 100 as cumulative_return_pct
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= date('2025-09-01', '-90 days')
    ORDER BY sp.date, cf.market_cap DESC
    """
    
    timeseries_df = pd.read_sql_query(timeseries_query, conn)
    timeseries_df.to_csv('../tableau/timeseries_data.csv', index=False)
    print(f"Time Series Data: {len(timeseries_df)} records")
    
    conn.close()
    print("\nAll Tableau datasets ready!")
    print("Files created in: market-intelligence-dashboard/tableau/")
    
    return {
        'executive': len(executive_df),
        'competitive': len(competitive_df),
        'risk': len(risk_df),
        'timeseries': len(timeseries_df)
    }

def create_tableau_folder():
    """Create tableau folder structure"""
    tableau_dir = '../tableau'
    if not os.path.exists(tableau_dir):
        os.makedirs(tableau_dir)
        print("Created tableau/ directory")

if __name__ == "__main__":
    create_tableau_folder()
    results = create_tableau_datasets()
    
    print("\n" + "="*50)
    print("TABLEAU DATA PREPARATION COMPLETE")
    print("="*50)
    print("Ready for dashboard creation!")
    print("\nNext steps:")
    print("1. Open Tableau Public")
    print("2. Connect to CSV files in tableau/ folder")
    print("3. Follow dashboard creation guide")