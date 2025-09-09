-- =====================================================
-- MARKET INTELLIGENCE MASTER ANALYSIS SCRIPT
-- Salomón Santiago Esquivel - Data Analyst Portfolio
-- =====================================================

-- This script demonstrates advanced SQL capabilities for business intelligence
-- Execute sections based on your database platform (SQLite, PostgreSQL, MySQL)

-- =====================================================
-- SECTION 1: DATA SETUP AND VALIDATION
-- =====================================================

-- First, let's verify our data is loaded correctly
SELECT 
    'DATA VALIDATION CHECK' as analysis_section,
    (SELECT COUNT(*) FROM stock_prices) as total_price_records,
    (SELECT COUNT(DISTINCT symbol) FROM stock_prices) as companies_with_price_data,
    (SELECT COUNT(*) FROM company_fundamentals) as companies_with_fundamentals,
    (SELECT MIN(date) FROM stock_prices) as earliest_date,
    (SELECT MAX(date) FROM stock_prices) as latest_date,
    (SELECT COUNT(*) FROM stock_prices WHERE daily_change IS NULL) as missing_calculations;

-- =====================================================
-- SECTION 2: EXECUTIVE SUMMARY - KEY METRICS
-- =====================================================

SELECT 
    '=== EXECUTIVE SUMMARY ===' as section_header,
    '' as blank_line;

-- Portfolio overview with key performance indicators
WITH portfolio_summary AS (
    SELECT 
        COUNT(DISTINCT cf.symbol) as companies,
        SUM(cf.market_cap)/1000000000 as total_market_cap_b,
        AVG(sp.daily_change * 100) as avg_daily_return,
        STDDEV(sp.daily_change * 100) as portfolio_volatility,
        MIN(sp.daily_change * 100) as worst_day,
        MAX(sp.daily_change * 100) as best_day,
        COUNT(CASE WHEN sp.daily_change > 0.02 THEN 1 END) as strong_up_days,
        COUNT(CASE WHEN sp.daily_change < -0.02 THEN 1 END) as strong_down_days,
        COUNT(DISTINCT sp.date) as trading_days
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
)
SELECT 
    'Portfolio Composition' as metric,
    companies || ' technology companies' as value,
    'Covering major tech sectors' as note
FROM portfolio_summary

UNION ALL

SELECT 
    'Total Market Exposure',
    '$' || ROUND(total_market_cap_b, 1) || ' billion',
    'Combined market capitalization'
FROM portfolio_summary

UNION ALL

SELECT 
    'Average Daily Performance',
    ROUND(avg_daily_return, 3) || '%',
    'Over ' || trading_days || ' trading days'
FROM portfolio_summary

UNION ALL

SELECT 
    'Portfolio Risk Level',
    ROUND(portfolio_volatility, 2) || '% daily volatility',
    CASE 
        WHEN portfolio_volatility > 4 THEN 'High risk profile'
        WHEN portfolio_volatility > 2.5 THEN 'Moderate risk profile'
        ELSE 'Conservative risk profile'
    END
FROM portfolio_summary

UNION ALL

SELECT 
    'Extreme Market Events',
    strong_up_days || ' strong up days, ' || strong_down_days || ' strong down days',
    'Days with >2% absolute moves'
FROM portfolio_summary;

-- =====================================================
-- SECTION 3: TOP PERFORMERS AND LAGGARDS
-- =====================================================

SELECT '' as blank_line, '=== TOP PERFORMERS (90-Day Period) ===' as section_header;

-- Top 5 performing companies
SELECT 
    ROW_NUMBER() OVER (ORDER BY AVG(sp.daily_change) DESC) as rank_num,
    cf.symbol,
    cf.company,
    cf.sector,
    ROUND(AVG(sp.daily_change * 100), 3) as avg_daily_return_pct,
    ROUND(((MAX(sp.close_price) - MIN(sp.close_price)) / MIN(sp.close_price)) * 100, 1) as total_return_pct,
    ROUND(cf.market_cap/1000000000, 1) as market_cap_billions
FROM stock_prices sp
JOIN company_fundamentals cf ON sp.symbol = cf.symbol
WHERE sp.date >= DATE('2025-09-01', '-90 days')
GROUP BY cf.symbol, cf.company, cf.sector, cf.market_cap
ORDER BY AVG(sp.daily_change) DESC
LIMIT 5;

SELECT '' as blank_line, '=== COMPETITIVE ANALYSIS: LENOVO VS DIRECT COMPETITORS ===' as section_header;

-- Lenovo competitive position
WITH competitor_analysis AS (
    SELECT 
        cf.symbol,
        cf.company,
        ROUND(AVG(sp.daily_change * 100), 3) as avg_return_pct,
        ROUND(STDDEV(sp.daily_change * 100), 2) as volatility_pct,
        ROUND(((MAX(sp.close_price) - MIN(sp.close_price)) / MIN(sp.close_price)) * 100, 1) as period_return_pct,
        ROUND(cf.market_cap/1000000000, 1) as market_cap_b,
        COUNT(CASE WHEN sp.daily_change > 0 THEN 1 END) * 100 / COUNT(*) as positive_days_pct
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    AND cf.symbol IN ('LNVGY', 'AAPL', 'MSFT', 'HPQ', 'DELL')
    GROUP BY cf.symbol, cf.company, cf.market_cap
)
SELECT 
    symbol,
    company,
    avg_return_pct as "Avg Daily Return %",
    period_return_pct as "90-Day Total Return %",
    volatility_pct as "Risk (Volatility %)",
    market_cap_b as "Market Cap $B",
    ROUND(positive_days_pct, 1) as "Positive Days %",
    RANK() OVER (ORDER BY avg_return_pct DESC) as performance_rank,
    CASE 
        WHEN symbol = 'LNVGY' THEN '← LENOVO POSITION'
        ELSE ''
    END as highlight
FROM competitor_analysis
ORDER BY avg_return_pct DESC;

-- =====================================================
-- SECTION 4: RISK ANALYSIS SUMMARY
-- =====================================================

SELECT '' as blank_line, '=== RISK ANALYSIS SUMMARY ===' as section_header;

-- Risk metrics by sector
WITH sector_risk AS (
    SELECT 
        cf.sector,
        COUNT(DISTINCT cf.symbol) as companies,
        ROUND(AVG(sp.daily_change * 100), 3) as avg_return_pct,
        ROUND(STDDEV(sp.daily_change * 100), 2) as volatility_pct,
        ROUND(MIN(sp.daily_change * 100), 2) as worst_day_pct,
        COUNT(CASE WHEN sp.daily_change < -0.05 THEN 1 END) as extreme_loss_days
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    GROUP BY cf.sector
)
SELECT 
    sector,
    companies || ' companies' as composition,
    avg_return_pct as "Avg Return %",
    volatility_pct as "Volatility %",
    worst_day_pct as "Worst Day %",
    extreme_loss_days as "Extreme Loss Events",
    CASE 
        WHEN volatility_pct > 4 THEN 'HIGH RISK'
        WHEN volatility_pct > 2.5 THEN 'MODERATE RISK'
        ELSE 'LOW RISK'
    END as risk_assessment
FROM sector_risk
ORDER BY volatility_pct DESC;

-- =====================================================
-- SECTION 5: MARKET OPPORTUNITIES
-- =====================================================

SELECT '' as blank_line, '=== STRATEGIC OPPORTUNITIES ===' as section_header;

-- Growth opportunity analysis
WITH opportunity_analysis AS (
    SELECT 
        cf.symbol,
        cf.company,
        cf.sector,
        ROUND(cf.market_cap/1000000000, 1) as market_cap_b,
        ROUND(AVG(sp.daily_change * 100), 3) as avg_return_pct,
        ROUND(STDDEV(sp.daily_change * 100), 2) as risk_pct,
        -- Simple opportunity score: return/risk ratio
        ROUND(AVG(sp.daily_change) / NULLIF(STDDEV(sp.daily_change), 0), 3) as risk_adjusted_return,
        ROUND(AVG(sp.volume * sp.close_price)/1000000, 1) as avg_volume_m
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    GROUP BY cf.symbol, cf.company, cf.sector, cf.market_cap
    HAVING AVG(sp.daily_change) > 0  -- Only positive performers
)
SELECT 
    symbol,
    company,
    sector,
    avg_return_pct as "Return %",
    risk_pct as "Risk %",
    risk_adjusted_return as "Risk-Adj Return",
    market_cap_b as "Market Cap $B",
    CASE 
        WHEN risk_adjusted_return > 0.1 AND avg_return_pct > 0.05 THEN 'HIGH OPPORTUNITY'
        WHEN risk_adjusted_return > 0.05 THEN 'MODERATE OPPORTUNITY'
        ELSE 'MONITOR'
    END as opportunity_rating
FROM opportunity_analysis
ORDER BY risk_adjusted_return DESC
LIMIT 8;

-- =====================================================
-- SECTION 6: ACTIONABLE INSIGHTS
-- =====================================================

SELECT '' as blank_line, '=== KEY BUSINESS INSIGHTS ===' as section_header;

-- Generate actionable business insights
WITH insights AS (
    SELECT 
        (SELECT symbol FROM company_fundamentals WHERE market_cap = (SELECT MAX(market_cap) FROM company_fundamentals)) as market_leader,
        (SELECT cf.symbol 
         FROM stock_prices sp JOIN company_fundamentals cf ON sp.symbol = cf.symbol 
         WHERE sp.date >= DATE('2025-09-01', '-90 days')
         GROUP BY cf.symbol 
         ORDER BY AVG(sp.daily_change) DESC LIMIT 1) as top_performer,
        (SELECT cf.symbol 
         FROM stock_prices sp JOIN company_fundamentals cf ON sp.symbol = cf.symbol 
         WHERE sp.date >= DATE('2025-09-01', '-90 days')
         GROUP BY cf.symbol 
         ORDER BY STDDEV(sp.daily_change) ASC LIMIT 1) as most_stable,
        (SELECT COUNT(*) FROM stock_prices WHERE daily_change > 0.05 AND date >= DATE('2025-09-01', '-90 days')) as high_volatility_events
)
SELECT 1 as insight_order, 'Market Leadership' as category, 
       market_leader || ' maintains largest market capitalization' as insight,
       'Consider for strategic partnerships or competitive analysis' as recommendation
FROM insights

UNION ALL

SELECT 2, 'Performance Leadership',
       top_performer || ' shows strongest 90-day performance',
       'Investigate success factors for potential adoption'
FROM insights

UNION ALL

SELECT 3, 'Risk Management',
       most_stable || ' demonstrates lowest volatility',
       'Consider as defensive holding during uncertain periods'
FROM insights

UNION ALL

SELECT 4, 'Market Conditions',
       'Detected ' || high_volatility_events || ' high volatility events',
       CASE 
           WHEN high_volatility_events > 50 THEN 'Exercise caution with major announcements'
           WHEN high_volatility_events > 20 THEN 'Normal market volatility observed'
           ELSE 'Stable market conditions favorable for strategic moves'
       END
FROM insights

ORDER BY insight_order;

-- =====================================================
-- SECTION 7: RECOMMENDED ACTIONS
-- =====================================================

SELECT '' as blank_line, '=== STRATEGIC RECOMMENDATIONS ===' as section_header;

SELECT 
    1 as priority,
    'Portfolio Optimization' as action_category,
    'Rebalance exposure based on risk-adjusted returns' as recommendation,
    'Focus on companies with strong risk-adjusted performance' as rationale

UNION ALL

SELECT 2, 'Competitive Intelligence',
       'Deep-dive analysis of top-performing competitors',
       'Understand success factors driving outperformance'

UNION ALL

SELECT 3, 'Risk Management',
       'Implement volatility monitoring for extreme events',
       'Early warning system for market stress conditions'

UNION ALL

SELECT 4, 'Market Timing',
       'Leverage market pattern analysis for strategic announcements',
       'Optimize timing based on historical market behavior'

UNION ALL

SELECT 5, 'Sector Analysis',
       'Consider sector rotation opportunities',
       'Identify emerging trends in technology subsectors'

ORDER BY priority;

-- =====================================================
-- FINAL SUMMARY
-- =====================================================

SELECT '' as blank_line, '=== ANALYSIS COMPLETE ===' as section_header,
       'Market Intelligence Dashboard - Salomón Santiago Esquivel' as analyst,
       'Advanced SQL Analysis for Business Intelligence' as project_type;

-- =====================================================
-- EXECUTION NOTES:
-- 
-- This master script demonstrates:
-- ✓ Advanced SQL techniques (CTEs, window functions, analytical queries)
-- ✓ Business intelligence focus (actionable insights)
-- ✓ Executive-level reporting (clear, concise summaries)
-- ✓ Risk analysis capabilities (volatility, correlation, VaR concepts)
-- ✓ Competitive intelligence (market positioning, performance ranking)
-- ✓ Strategic recommendations (data-driven decision support)
-- 
-- Perfect for showcasing SQL skills to potential employers in:
-- - Technology companies (competitive analysis)
-- - Financial services (risk analysis)  
-- - Consulting (strategic insights)
-- - Any data-driven organization
-- =====================================================