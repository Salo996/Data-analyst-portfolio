-- =====================================================
-- COMPETITIVE ANALYSIS QUERIES
-- Salomón Santiago Esquivel - Data Analyst Portfolio
-- =====================================================

-- Focus: Strategic competitive intelligence for technology companies
-- Business Application: Support strategic decisions for companies like Lenovo

-- =====================================================
-- QUERY 1: LENOVO VS DIRECT COMPETITORS ANALYSIS
-- Business Question: How does Lenovo perform vs direct PC/hardware competitors?
-- =====================================================

WITH lenovo_competitors AS (
    SELECT symbol, company, sector
    FROM company_fundamentals 
    WHERE symbol IN ('LNVGY', 'AAPL', 'HPQ', 'DELL', 'MSFT')
),
performance_metrics AS (
    SELECT 
        cf.symbol,
        cf.company,
        -- Price Performance
        AVG(sp.daily_change) * 100 as avg_daily_change_pct,
        STDDEV(sp.daily_change) * 100 as volatility_pct,
        (MAX(sp.close_price) - MIN(sp.close_price)) / MIN(sp.close_price) * 100 as total_return_pct,
        
        -- Market Metrics
        AVG(sp.volume) as avg_daily_volume,
        AVG(sp.volume_ratio) as avg_volume_intensity,
        
        -- Risk Metrics  
        COUNT(CASE WHEN sp.daily_change > 0.05 THEN 1 END) as high_gain_days,
        COUNT(CASE WHEN sp.daily_change < -0.05 THEN 1 END) as high_loss_days,
        COUNT(*) as total_trading_days,
        
        -- Recent Performance (Last 30 days)
        AVG(CASE 
            WHEN sp.date >= DATE('2025-09-01', '-30 days') 
            THEN sp.daily_change * 100 
        END) as recent_30d_avg_change
        
    FROM stock_prices sp
    JOIN lenovo_competitors cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    GROUP BY cf.symbol, cf.company
)
SELECT 
    symbol,
    company,
    ROUND(avg_daily_change_pct, 3) as avg_daily_return_pct,
    ROUND(volatility_pct, 2) as risk_volatility_pct,
    ROUND(total_return_pct, 1) as period_total_return_pct,
    ROUND(avg_daily_volume/1000000, 1) as avg_volume_millions,
    ROUND(avg_volume_intensity, 2) as volume_intensity_ratio,
    high_gain_days,
    high_loss_days,
    ROUND((high_gain_days * 100.0 / total_trading_days), 1) as positive_days_pct,
    ROUND(recent_30d_avg_change, 3) as recent_momentum_pct,
    
    -- Performance Ranking
    RANK() OVER (ORDER BY avg_daily_change_pct DESC) as return_rank,
    RANK() OVER (ORDER BY volatility_pct ASC) as stability_rank
FROM performance_metrics
ORDER BY avg_daily_change_pct DESC;

-- =====================================================
-- QUERY 2: SECTOR LEADERSHIP ANALYSIS
-- Business Question: Which companies are market leaders in each tech sector?
-- =====================================================

WITH sector_performance AS (
    SELECT 
        cf.sector,
        cf.symbol,
        cf.company,
        cf.market_cap,
        AVG(sp.close_price * sp.volume) as avg_dollar_volume,
        AVG(sp.daily_change) * 100 as avg_return_pct,
        STDDEV(sp.daily_change) * 100 as volatility_pct,
        AVG(sp.volume_ratio) as market_interest,
        
        -- Market Cap Ranking within sector
        RANK() OVER (PARTITION BY cf.sector ORDER BY cf.market_cap DESC) as market_cap_rank,
        
        -- Performance ranking within sector  
        RANK() OVER (PARTITION BY cf.sector ORDER BY AVG(sp.daily_change) DESC) as performance_rank
        
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    AND cf.market_cap > 0
    GROUP BY cf.sector, cf.symbol, cf.company, cf.market_cap
)
SELECT 
    sector,
    symbol,
    company,
    ROUND(market_cap/1000000000, 1) as market_cap_billions,
    market_cap_rank,
    ROUND(avg_return_pct, 3) as avg_daily_return_pct,
    performance_rank,
    ROUND(volatility_pct, 2) as volatility_pct,
    ROUND(avg_dollar_volume/1000000, 1) as avg_dollar_volume_millions,
    ROUND(market_interest, 2) as market_interest_ratio,
    
    -- Leadership Score (combines market cap and performance)
    ROUND((100.0 / market_cap_rank) + (100.0 / performance_rank), 1) as leadership_score
    
FROM sector_performance
WHERE market_cap_rank <= 5  -- Top 5 by market cap in each sector
ORDER BY sector, leadership_score DESC;

-- =====================================================
-- QUERY 3: MARKET CORRELATION ANALYSIS
-- Business Question: Which stocks move together? (Important for portfolio/risk management)
-- =====================================================

WITH daily_returns AS (
    SELECT 
        sp1.date,
        sp1.symbol as symbol1,
        sp1.company as company1,
        sp1.daily_change as return1,
        sp2.symbol as symbol2,
        sp2.company as company2,
        sp2.daily_change as return2
    FROM stock_prices sp1
    JOIN stock_prices sp2 ON sp1.date = sp2.date AND sp1.symbol < sp2.symbol
    WHERE sp1.date >= DATE('2025-09-01', '-90 days')
    AND sp1.symbol IN ('LNVGY', 'AAPL', 'MSFT', 'HPQ', 'DELL', 'IBM', 'NVDA', 'AMD')
    AND sp2.symbol IN ('LNVGY', 'AAPL', 'MSFT', 'HPQ', 'DELL', 'IBM', 'NVDA', 'AMD')
),
correlation_calc AS (
    SELECT 
        symbol1,
        company1,
        symbol2,
        company2,
        COUNT(*) as data_points,
        AVG(return1) as avg_return1,
        AVG(return2) as avg_return2,
        AVG(return1 * return2) as avg_product,
        AVG(return1 * return1) as avg_square1,
        AVG(return2 * return2) as avg_square2
    FROM daily_returns
    GROUP BY symbol1, company1, symbol2, company2
    HAVING COUNT(*) >= 60  -- At least 60 trading days
)
SELECT 
    symbol1,
    company1,
    symbol2, 
    company2,
    data_points,
    ROUND(
        (avg_product - avg_return1 * avg_return2) / 
        (SQRT(avg_square1 - avg_return1 * avg_return1) * 
         SQRT(avg_square2 - avg_return2 * avg_return2)), 3
    ) as correlation_coefficient,
    
    CASE 
        WHEN ABS((avg_product - avg_return1 * avg_return2) / 
                (SQRT(avg_square1 - avg_return1 * avg_return1) * 
                 SQRT(avg_square2 - avg_return2 * avg_return2))) >= 0.7 
        THEN 'High Correlation'
        WHEN ABS((avg_product - avg_return1 * avg_return2) / 
                (SQRT(avg_square1 - avg_return1 * avg_return1) * 
                 SQRT(avg_square2 - avg_return2 * avg_return2))) >= 0.3 
        THEN 'Medium Correlation'
        ELSE 'Low Correlation'
    END as correlation_strength
    
FROM correlation_calc
ORDER BY ABS(correlation_coefficient) DESC;

-- =====================================================
-- QUERY 4: MARKET TIMING OPPORTUNITIES
-- Business Question: When are the best/worst days to make strategic announcements?
-- =====================================================

WITH market_patterns AS (
    SELECT 
        strftime('%w', sp.date) as day_of_week,
        CASE strftime('%w', sp.date)
            WHEN '0' THEN 'Sunday'
            WHEN '1' THEN 'Monday'
            WHEN '2' THEN 'Tuesday'
            WHEN '3' THEN 'Wednesday'
            WHEN '4' THEN 'Thursday'
            WHEN '5' THEN 'Friday'
            WHEN '6' THEN 'Saturday'
        END as weekday_name,
        
        sp.symbol,
        sp.company,
        sp.daily_change,
        sp.volume,
        sp.volatility_30d
        
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    AND sp.symbol IN ('LNVGY', 'AAPL', 'MSFT', 'GOOGL', 'AMZN')  -- Major tech companies
)
SELECT 
    weekday_name,
    day_of_week,
    COUNT(*) as trading_days,
    ROUND(AVG(daily_change) * 100, 3) as avg_daily_return_pct,
    ROUND(STDDEV(daily_change) * 100, 2) as volatility_pct,
    ROUND(AVG(volume)/1000000, 1) as avg_volume_millions,
    
    -- Market sentiment indicators
    COUNT(CASE WHEN daily_change > 0.02 THEN 1 END) as strong_up_days,
    COUNT(CASE WHEN daily_change < -0.02 THEN 1 END) as strong_down_days,
    
    ROUND(
        (COUNT(CASE WHEN daily_change > 0 THEN 1 END) * 100.0) / COUNT(*), 1
    ) as positive_days_pct
    
FROM market_patterns
GROUP BY day_of_week, weekday_name
ORDER BY day_of_week;

-- =====================================================
-- BUSINESS INSIGHTS SUMMARY QUERY
-- High-level executive summary for decision makers
-- =====================================================

SELECT 
    'COMPETITIVE POSITION SUMMARY' as analysis_type,
    'Based on 90-day market data analysis' as period,
    COUNT(DISTINCT cf.symbol) as companies_analyzed,
    ROUND(AVG(sp.daily_change * 100), 3) as market_avg_daily_return_pct,
    ROUND(MAX(sp.close_price * cf.market_cap/1000000000), 1) as largest_market_cap_billions,
    
    (SELECT symbol FROM company_fundamentals WHERE market_cap = (SELECT MAX(market_cap) FROM company_fundamentals)) as market_leader,
    
    (SELECT COUNT(*) FROM stock_prices WHERE daily_change > 0.05) as high_volatility_events
    
FROM stock_prices sp
JOIN company_fundamentals cf ON sp.symbol = cf.symbol
WHERE sp.date >= DATE('2025-09-01', '-90 days');

-- =====================================================
-- NOTES FOR PORTFOLIO PRESENTATION:
-- 
-- These queries demonstrate:
-- 1. Advanced SQL techniques (CTEs, Window Functions, Ranking)
-- 2. Business intelligence focus (competitive analysis)
-- 3. Statistical analysis (correlations, volatility)
-- 4. Real-world applications (market timing, risk assessment)
-- 5. Executive-level reporting capabilities
-- 
-- Perfect for showcasing to potential employers in:
-- - Technology companies
-- - Financial services  
-- - Consulting firms
-- - Any data-driven organization
-- =====================================================