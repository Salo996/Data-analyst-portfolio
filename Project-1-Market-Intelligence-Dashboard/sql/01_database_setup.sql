-- =====================================================
-- MARKET INTELLIGENCE DATABASE SETUP
-- Salomón Santiago Esquivel - Data Analyst Portfolio
-- =====================================================

-- This script creates the database structure for market intelligence analysis
-- Focus: Competitive analysis for technology companies

-- Create database (if using MySQL/PostgreSQL)
-- CREATE DATABASE market_intelligence;
-- USE market_intelligence;

-- =====================================================
-- TABLE: stock_prices
-- Daily stock price data with calculated metrics
-- =====================================================
CREATE TABLE IF NOT EXISTS stock_prices (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    company VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    open_price DECIMAL(10,2) NOT NULL,
    high_price DECIMAL(10,2) NOT NULL,
    low_price DECIMAL(10,2) NOT NULL,
    close_price DECIMAL(10,2) NOT NULL,
    volume BIGINT NOT NULL,
    
    -- Calculated metrics
    daily_change DECIMAL(8,4),          -- % daily change
    daily_change_abs DECIMAL(10,2),     -- Absolute $ change
    volatility_30d DECIMAL(8,4),        -- 30-day volatility
    ma_7 DECIMAL(10,2),                 -- 7-day moving average
    ma_30 DECIMAL(10,2),                -- 30-day moving average
    volume_ma_7 BIGINT,                 -- 7-day volume average
    volume_ratio DECIMAL(6,2),          -- Volume vs average ratio
    daily_range DECIMAL(6,2),           -- High-low range %
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    UNIQUE(symbol, date)
);

-- =====================================================
-- TABLE: company_fundamentals
-- Company fundamental data and metrics
-- =====================================================
CREATE TABLE IF NOT EXISTS company_fundamentals (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL UNIQUE,
    company VARCHAR(100) NOT NULL,
    market_cap BIGINT,
    revenue BIGINT,
    employees INTEGER,
    sector VARCHAR(50),
    industry VARCHAR(100),
    country VARCHAR(50),
    website VARCHAR(200),
    collection_date DATE NOT NULL,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================
CREATE INDEX IF NOT EXISTS idx_stock_symbol_date ON stock_prices(symbol, date);
CREATE INDEX IF NOT EXISTS idx_stock_date ON stock_prices(date);
CREATE INDEX IF NOT EXISTS idx_stock_symbol ON stock_prices(symbol);
CREATE INDEX IF NOT EXISTS idx_fundamentals_symbol ON company_fundamentals(symbol);
CREATE INDEX IF NOT EXISTS idx_fundamentals_sector ON company_fundamentals(sector);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Latest stock prices with company info
CREATE VIEW IF NOT EXISTS v_latest_prices AS
SELECT 
    sp.symbol,
    cf.company,
    cf.sector,
    cf.market_cap,
    sp.close_price,
    sp.daily_change,
    sp.volume,
    sp.volatility_30d,
    sp.date
FROM stock_prices sp
JOIN company_fundamentals cf ON sp.symbol = cf.symbol
WHERE sp.date = (SELECT MAX(date) FROM stock_prices WHERE symbol = sp.symbol);

-- Stock performance summary by company
CREATE VIEW IF NOT EXISTS v_performance_summary AS
SELECT 
    sp.symbol,
    cf.company,
    cf.sector,
    COUNT(sp.date) as trading_days,
    MIN(sp.close_price) as min_price,
    MAX(sp.close_price) as max_price,
    AVG(sp.close_price) as avg_price,
    AVG(sp.daily_change) as avg_daily_change,
    AVG(sp.volume) as avg_volume,
    AVG(sp.volatility_30d) as avg_volatility,
    (MAX(sp.close_price) - MIN(sp.close_price)) / MIN(sp.close_price) * 100 as price_range_pct
FROM stock_prices sp
JOIN company_fundamentals cf ON sp.symbol = cf.symbol
GROUP BY sp.symbol, cf.company, cf.sector;

-- =====================================================
-- SAMPLE DATA VERIFICATION QUERIES
-- =====================================================

-- Check data completeness
SELECT 
    'Stock Prices' as table_name,
    COUNT(*) as total_records,
    COUNT(DISTINCT symbol) as unique_companies,
    MIN(date) as earliest_date,
    MAX(date) as latest_date
FROM stock_prices

UNION ALL

SELECT 
    'Company Fundamentals' as table_name,
    COUNT(*) as total_records,
    COUNT(DISTINCT symbol) as unique_companies,
    MIN(collection_date) as earliest_date,
    MAX(collection_date) as latest_date
FROM company_fundamentals;

-- =====================================================
-- COMMENTS AND DOCUMENTATION
-- =====================================================

/*
BUSINESS PURPOSE:
This database supports competitive intelligence analysis for technology companies,
with specific focus on:

1. COMPETITIVE ANALYSIS: Track Lenovo vs direct competitors (HP, Dell, Apple)
2. SECTOR PERFORMANCE: Analyze technology sector trends and correlations
3. MARKET TIMING: Identify optimal timing for strategic decisions
4. RISK ASSESSMENT: Monitor volatility and market risks

KEY METRICS CALCULATED:
- Daily price changes and volatility measures
- Moving averages for trend analysis  
- Volume analysis for market sentiment
- Performance ratios for comparative analysis

DESIGNED BY: Salomón Santiago Esquivel
PURPOSE: Data Analyst Portfolio Project - Market Intelligence Dashboard
*/