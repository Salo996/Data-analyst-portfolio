-- =====================================================
-- BUSINESS INTELLIGENCE AND STRATEGIC INSIGHTS
-- Salomón Santiago Esquivel - Data Analyst Portfolio
-- =====================================================

-- Advanced analytical queries for executive decision-making
-- Focus: Strategic insights for technology company management

-- =====================================================
-- QUERY 1: MARKET OPPORTUNITY IDENTIFICATION
-- Business Question: Which market segments show the best growth opportunities?
-- =====================================================

WITH market_segments AS (
    SELECT 
        cf.sector,
        cf.industry,
        COUNT(DISTINCT cf.symbol) as companies_in_segment,
        SUM(cf.market_cap) as total_segment_value,
        AVG(cf.market_cap) as avg_company_size,
        
        -- Performance metrics over 90 days
        AVG(sp.daily_change) as avg_daily_growth,
        STDDEV(sp.daily_change) as growth_volatility,
        (MAX(sp.close_price) - MIN(sp.close_price)) / MIN(sp.close_price) as total_growth,
        
        -- Market activity indicators
        AVG(sp.volume * sp.close_price) as avg_dollar_volume,
        AVG(sp.volume_ratio) as market_interest_level,
        
        -- Growth momentum (last 30 vs previous 60 days)
        AVG(CASE 
            WHEN sp.date >= DATE('2025-09-01', '-30 days') 
            THEN sp.daily_change 
        END) as recent_momentum,
        AVG(CASE 
            WHEN sp.date BETWEEN DATE('2025-09-01', '-90 days') AND DATE('2025-09-01', '-31 days')
            THEN sp.daily_change 
        END) as earlier_performance
        
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    AND cf.market_cap > 1000000000  -- Focus on companies > $1B market cap
    GROUP BY cf.sector, cf.industry
    HAVING COUNT(DISTINCT cf.symbol) >= 2  -- At least 2 companies in segment
)
SELECT 
    sector,
    industry,
    companies_in_segment,
    ROUND(total_segment_value/1000000000, 1) as segment_value_billions,
    ROUND(avg_company_size/1000000000, 2) as avg_company_size_billions,
    ROUND(avg_daily_growth * 100, 3) as avg_daily_growth_pct,
    ROUND(growth_volatility * 100, 2) as volatility_pct,
    ROUND(total_growth * 100, 1) as total_90d_growth_pct,
    ROUND(avg_dollar_volume/1000000, 1) as avg_dollar_volume_millions,
    ROUND(market_interest_level, 2) as market_interest_ratio,
    ROUND(recent_momentum * 100, 3) as recent_30d_momentum_pct,
    ROUND((recent_momentum - earlier_performance) * 100, 3) as momentum_change_pct,
    
    -- Opportunity Score (combines growth, size, and momentum)
    ROUND(
        (avg_daily_growth * 10000) +  -- Growth factor
        (total_growth * 100) +        -- Total performance
        (recent_momentum - earlier_performance) * 5000 + -- Momentum shift
        LOG(total_segment_value/1000000000) * 20  -- Market size factor
    , 1) as opportunity_score,
    
    -- Strategic Assessment
    CASE 
        WHEN avg_daily_growth > 0.005 AND total_growth > 0.2 THEN 'HIGH OPPORTUNITY'
        WHEN avg_daily_growth > 0.002 AND total_growth > 0.1 THEN 'MODERATE OPPORTUNITY'
        WHEN avg_daily_growth > 0 THEN 'STABLE MARKET'
        ELSE 'DECLINING MARKET'
    END as market_assessment
    
FROM market_segments
ORDER BY opportunity_score DESC;

-- =====================================================
-- QUERY 2: COMPETITIVE POSITIONING MATRIX
-- Business Question: Where do we stand vs competitors across key metrics?
-- =====================================================

WITH competitive_metrics AS (
    SELECT 
        cf.symbol,
        cf.company,
        cf.sector,
        cf.market_cap,
        
        -- Financial performance
        AVG(sp.daily_change) as avg_return,
        STDDEV(sp.daily_change) as volatility,
        (MAX(sp.close_price) - MIN(sp.close_price)) / MIN(sp.close_price) as total_return,
        
        -- Market position
        AVG(sp.volume * sp.close_price) as avg_dollar_volume,
        AVG(sp.volume_ratio) as market_attention,
        
        -- Stability metrics
        COUNT(CASE WHEN sp.daily_change > 0 THEN 1 END) * 100.0 / COUNT(*) as positive_days_pct,
        MAX(sp.daily_change) as best_single_day,
        MIN(sp.daily_change) as worst_single_day
        
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    AND cf.symbol IN ('LNVGY', 'AAPL', 'MSFT', 'HPQ', 'DELL', 'IBM', 'INTC', 'AMD', 'NVDA')
    GROUP BY cf.symbol, cf.company, cf.sector, cf.market_cap
),
percentile_ranks AS (
    SELECT 
        *,
        -- Percentile rankings for each metric
        NTILE(100) OVER (ORDER BY market_cap) as market_cap_percentile,
        NTILE(100) OVER (ORDER BY avg_return) as performance_percentile,
        NTILE(100) OVER (ORDER BY volatility DESC) as stability_percentile,  -- Lower volatility = higher rank
        NTILE(100) OVER (ORDER BY avg_dollar_volume) as liquidity_percentile,
        NTILE(100) OVER (ORDER BY positive_days_pct) as consistency_percentile
    FROM competitive_metrics
)
SELECT 
    symbol,
    company,
    sector,
    ROUND(market_cap/1000000000, 2) as market_cap_billions,
    market_cap_percentile,
    
    ROUND(avg_return * 100, 3) as avg_daily_return_pct,
    performance_percentile,
    
    ROUND(volatility * 100, 2) as volatility_pct,
    stability_percentile,
    
    ROUND(avg_dollar_volume/1000000, 1) as avg_volume_millions,
    liquidity_percentile,
    
    ROUND(positive_days_pct, 1) as positive_days_pct,
    consistency_percentile,
    
    -- Overall Competitive Score (weighted average)
    ROUND(
        (market_cap_percentile * 0.25) +      -- Market position: 25%
        (performance_percentile * 0.30) +     -- Performance: 30%
        (stability_percentile * 0.20) +       -- Stability: 20%
        (liquidity_percentile * 0.15) +       -- Liquidity: 15%
        (consistency_percentile * 0.10)       -- Consistency: 10%
    , 1) as competitive_score,
    
    -- Strategic Position
    CASE 
        WHEN 
            (market_cap_percentile * 0.25 + performance_percentile * 0.30 + 
             stability_percentile * 0.20 + liquidity_percentile * 0.15 + 
             consistency_percentile * 0.10) >= 80 THEN 'MARKET LEADER'
        WHEN 
            (market_cap_percentile * 0.25 + performance_percentile * 0.30 + 
             stability_percentile * 0.20 + liquidity_percentile * 0.15 + 
             consistency_percentile * 0.10) >= 60 THEN 'STRONG COMPETITOR'
        WHEN 
            (market_cap_percentile * 0.25 + performance_percentile * 0.30 + 
             stability_percentile * 0.20 + liquidity_percentile * 0.15 + 
             consistency_percentile * 0.10) >= 40 THEN 'MARKET PARTICIPANT'
        ELSE 'CHALLENGER'
    END as market_position
    
FROM percentile_ranks
ORDER BY competitive_score DESC;

-- =====================================================
-- QUERY 3: INVESTMENT TIMING ANALYSIS
-- Business Question: What are the optimal timing patterns for strategic moves?
-- =====================================================

WITH timing_analysis AS (
    SELECT 
        -- Time-based patterns
        strftime('%m', sp.date) as month_num,
        CASE strftime('%m', sp.date)
            WHEN '01' THEN 'January'   WHEN '02' THEN 'February'
            WHEN '03' THEN 'March'     WHEN '04' THEN 'April'
            WHEN '05' THEN 'May'       WHEN '06' THEN 'June'
            WHEN '07' THEN 'July'      WHEN '08' THEN 'August'
            WHEN '09' THEN 'September' WHEN '10' THEN 'October'
            WHEN '11' THEN 'November'  WHEN '12' THEN 'December'
        END as month_name,
        
        strftime('%w', sp.date) as day_of_week,
        
        sp.symbol,
        sp.daily_change,
        sp.volume,
        sp.volume_ratio,
        sp.close_price,
        
        -- Market conditions
        CASE 
            WHEN sp.daily_change > 0.03 THEN 'Strong Up'
            WHEN sp.daily_change > 0.01 THEN 'Moderate Up'
            WHEN sp.daily_change > -0.01 THEN 'Flat'
            WHEN sp.daily_change > -0.03 THEN 'Moderate Down'
            ELSE 'Strong Down'
        END as market_condition
        
    FROM stock_prices sp
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    AND sp.symbol IN ('LNVGY', 'AAPL', 'MSFT', 'GOOGL', 'NVDA')  -- Focus on major tech
),
pattern_analysis AS (
    SELECT 
        month_name,
        month_num,
        COUNT(*) as trading_days,
        COUNT(DISTINCT symbol) as companies_tracked,
        
        -- Performance patterns
        AVG(daily_change) as avg_daily_return,
        STDDEV(daily_change) as volatility,
        COUNT(CASE WHEN market_condition = 'Strong Up' THEN 1 END) as strong_up_days,
        COUNT(CASE WHEN market_condition = 'Strong Down' THEN 1 END) as strong_down_days,
        
        -- Volume patterns
        AVG(volume) as avg_volume,
        AVG(volume_ratio) as avg_volume_intensity,
        
        -- Market sentiment
        COUNT(CASE WHEN daily_change > 0 THEN 1 END) * 100.0 / COUNT(*) as positive_sentiment_pct
        
    FROM timing_analysis
    GROUP BY month_name, month_num
),
day_of_week_analysis AS (
    SELECT 
        CASE day_of_week
            WHEN '1' THEN 'Monday'    WHEN '2' THEN 'Tuesday'
            WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'
            WHEN '5' THEN 'Friday'
        END as weekday,
        day_of_week,
        
        COUNT(*) as trading_occurrences,
        AVG(daily_change) as avg_return,
        STDDEV(daily_change) as volatility,
        AVG(volume_ratio) as avg_volume_intensity,
        COUNT(CASE WHEN daily_change > 0.02 THEN 1 END) as strong_positive_days,
        COUNT(CASE WHEN daily_change > 0 THEN 1 END) * 100.0 / COUNT(*) as positive_pct
        
    FROM timing_analysis
    WHERE day_of_week BETWEEN '1' AND '5'  -- Weekdays only
    GROUP BY weekday, day_of_week
)
-- Monthly patterns
SELECT 
    'MONTHLY PATTERNS' as analysis_type,
    month_name as period,
    trading_days,
    ROUND(avg_daily_return * 100, 3) as avg_daily_return_pct,
    ROUND(volatility * 100, 2) as volatility_pct,
    strong_up_days,
    strong_down_days,
    ROUND(positive_sentiment_pct, 1) as positive_sentiment_pct,
    ROUND(avg_volume_intensity, 2) as market_activity_level,
    
    -- Strategic timing recommendation
    CASE 
        WHEN avg_daily_return > 0.003 AND volatility < 0.03 THEN 'OPTIMAL TIMING'
        WHEN positive_sentiment_pct > 60 THEN 'FAVORABLE CONDITIONS'
        WHEN strong_down_days > strong_up_days THEN 'CAUTION ADVISED'
        ELSE 'NEUTRAL TIMING'
    END as timing_recommendation
    
FROM pattern_analysis
ORDER BY month_num

UNION ALL

-- Weekly patterns  
SELECT 
    'WEEKLY PATTERNS' as analysis_type,
    weekday as period,
    trading_occurrences as trading_days,
    ROUND(avg_return * 100, 3) as avg_daily_return_pct,
    ROUND(volatility * 100, 2) as volatility_pct,
    strong_positive_days,
    NULL as strong_down_days,
    ROUND(positive_pct, 1) as positive_sentiment_pct,
    ROUND(avg_volume_intensity, 2) as market_activity_level,
    
    CASE 
        WHEN avg_return > 0.002 AND positive_pct > 55 THEN 'BEST DAY FOR ANNOUNCEMENTS'
        WHEN avg_return > 0 AND volatility < 0.025 THEN 'GOOD TIMING'
        WHEN positive_pct < 45 THEN 'AVOID MAJOR ANNOUNCEMENTS'
        ELSE 'NEUTRAL DAY'
    END as timing_recommendation
    
FROM day_of_week_analysis
ORDER BY day_of_week;

-- =====================================================
-- QUERY 4: STRATEGIC DASHBOARD FOR EXECUTIVES
-- Business Question: What are the key insights for the C-suite?
-- =====================================================

WITH executive_summary AS (
    SELECT 
        -- Portfolio Overview
        COUNT(DISTINCT cf.symbol) as companies_tracked,
        COUNT(DISTINCT cf.sector) as sectors_covered,
        SUM(cf.market_cap)/1000000000 as total_market_value_billions,
        
        -- Performance Metrics (90-day)
        AVG(sp.daily_change * 100) as avg_daily_return_pct,
        STDDEV(sp.daily_change * 100) as daily_volatility_pct,
        (SELECT COUNT(*) FROM stock_prices sp2 WHERE sp2.daily_change > 0.05 AND sp2.date >= DATE('2025-09-01', '-90 days')) as high_volatility_events,
        
        -- Market Position
        (SELECT COUNT(*) FROM company_fundamentals WHERE market_cap > 100000000000) as mega_cap_companies,
        (SELECT symbol FROM company_fundamentals WHERE market_cap = (SELECT MAX(market_cap) FROM company_fundamentals)) as largest_holding,
        
        -- Risk Indicators
        MIN(sp.daily_change * 100) as worst_single_day_pct,
        MAX(sp.daily_change * 100) as best_single_day_pct,
        AVG(CASE WHEN sp.daily_change < 0 THEN sp.daily_change * 100 END) as avg_loss_day_pct
        
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
),
top_performers AS (
    SELECT 
        cf.symbol,
        cf.company,
        AVG(sp.daily_change * 100) as avg_return_pct,
        (MAX(sp.close_price) - MIN(sp.close_price)) / MIN(sp.close_price) * 100 as total_return_pct
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    GROUP BY cf.symbol, cf.company
    ORDER BY avg_return_pct DESC
    LIMIT 3
),
risk_assets AS (
    SELECT 
        cf.symbol,
        cf.company,
        STDDEV(sp.daily_change * 100) as volatility_pct,
        MIN(sp.daily_change * 100) as worst_day_pct
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    GROUP BY cf.symbol, cf.company
    ORDER BY volatility_pct DESC
    LIMIT 3
)
SELECT 
    'EXECUTIVE DASHBOARD - MARKET INTELLIGENCE SUMMARY' as report_title,
    '90-Day Analysis Period' as period,
    
    -- Portfolio composition
    companies_tracked || ' companies across ' || sectors_covered || ' sectors' as portfolio_scope,
    '$' || ROUND(total_market_value_billions, 1) || 'B total market value' as portfolio_size,
    mega_cap_companies || ' mega-cap companies ($100B+)' as large_cap_exposure,
    
    -- Performance summary
    ROUND(avg_daily_return_pct, 3) || '% average daily return' as performance,
    ROUND(daily_volatility_pct, 2) || '% daily volatility' as risk_level,
    ROUND(avg_daily_return_pct * 252, 1) || '% annualized return estimate' as yearly_projection,
    
    -- Risk metrics
    ROUND(worst_single_day_pct, 2) || '% worst single day' as maximum_drawdown,
    high_volatility_events || ' high volatility events (>5% moves)' as tail_risk,
    ROUND(avg_loss_day_pct, 2) || '% average loss on down days' as downside_risk,
    
    -- Strategic insights
    largest_holding || ' (largest market cap position)' as market_leader,
    
    -- Overall assessment
    CASE 
        WHEN avg_daily_return_pct > 0.1 AND daily_volatility_pct < 3.0 THEN 'STRONG PERFORMANCE, MODERATE RISK'
        WHEN avg_daily_return_pct > 0.05 THEN 'POSITIVE PERFORMANCE'
        WHEN daily_volatility_pct > 4.0 THEN 'HIGH RISK ENVIRONMENT'
        ELSE 'STABLE MARKET CONDITIONS'
    END as market_assessment
    
FROM executive_summary;

-- =====================================================
-- KEY PERFORMANCE INDICATORS (KPIs) FOR TRACKING
-- =====================================================

CREATE VIEW IF NOT EXISTS v_kpi_dashboard AS
WITH kpi_calculations AS (
    SELECT 
        DATE('now') as report_date,
        COUNT(DISTINCT cf.symbol) as active_positions,
        SUM(cf.market_cap)/1000000000 as total_exposure_billions,
        AVG(sp.daily_change * 100) as daily_return_pct,
        STDDEV(sp.daily_change * 100) as volatility_pct,
        COUNT(CASE WHEN sp.daily_change > 0.03 THEN 1 END) as strong_up_days,
        COUNT(CASE WHEN sp.daily_change < -0.03 THEN 1 END) as strong_down_days,
        AVG(sp.volume * sp.close_price)/1000000 as avg_dollar_volume_millions
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-30 days')  -- Last 30 days
)
SELECT 
    report_date,
    active_positions as "Active Positions",
    ROUND(total_exposure_billions, 1) as "Total Exposure ($B)",
    ROUND(daily_return_pct, 3) as "Avg Daily Return (%)",
    ROUND(volatility_pct, 2) as "Daily Volatility (%)",
    strong_up_days as "Strong Up Days",
    strong_down_days as "Strong Down Days", 
    ROUND(avg_dollar_volume_millions, 1) as "Avg Volume ($M)",
    ROUND(daily_return_pct * 252, 1) as "Annualized Return Est (%)"
FROM kpi_calculations;

-- =====================================================
-- BUSINESS INTELLIGENCE SUMMARY
-- 
-- These queries provide executive-level insights for:
-- 1. Strategic market opportunity identification
-- 2. Competitive positioning analysis
-- 3. Optimal timing for business decisions
-- 4. Executive dashboard and KPI tracking
-- 
-- Perfect for demonstrating:
-- - Business acumen and strategic thinking
-- - Advanced SQL analytical capabilities  
-- - Executive communication skills
-- - Data-driven decision making
-- =====================================================