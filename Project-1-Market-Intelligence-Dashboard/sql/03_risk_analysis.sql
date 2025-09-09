-- =====================================================
-- RISK ANALYSIS AND PORTFOLIO OPTIMIZATION
-- Salomón Santiago Esquivel - Data Analyst Portfolio
-- =====================================================

-- Advanced SQL queries for financial risk analysis and portfolio management
-- Business Focus: Risk assessment for investment and strategic decisions

-- =====================================================
-- QUERY 1: VALUE AT RISK (VaR) ANALYSIS
-- Business Question: What's the maximum expected loss at 95% confidence level?
-- =====================================================

WITH daily_returns AS (
    SELECT 
        sp.symbol,
        cf.company,
        cf.sector,
        sp.date,
        sp.daily_change as daily_return,
        sp.close_price,
        -- Calculate portfolio weights based on market cap
        cf.market_cap * 1.0 / (SELECT SUM(market_cap) FROM company_fundamentals) as portfolio_weight
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    AND cf.market_cap > 0
),
return_statistics AS (
    SELECT 
        symbol,
        company,
        sector,
        portfolio_weight,
        COUNT(*) as trading_days,
        AVG(daily_return) as mean_return,
        STDDEV(daily_return) as volatility,
        MIN(daily_return) as worst_day_loss,
        MAX(daily_return) as best_day_gain,
        
        -- Calculate percentiles for VaR
        -- Approximation using standard deviation (assuming normal distribution)
        AVG(daily_return) - (1.645 * STDDEV(daily_return)) as var_95_percent,
        AVG(daily_return) - (2.326 * STDDEV(daily_return)) as var_99_percent
        
    FROM daily_returns
    GROUP BY symbol, company, sector, portfolio_weight
    HAVING COUNT(*) >= 60
)
SELECT 
    symbol,
    company,
    sector,
    ROUND(portfolio_weight * 100, 2) as portfolio_weight_pct,
    ROUND(mean_return * 100, 3) as avg_daily_return_pct,
    ROUND(volatility * 100, 2) as daily_volatility_pct,
    ROUND(worst_day_loss * 100, 2) as worst_single_day_loss_pct,
    ROUND(best_day_gain * 100, 2) as best_single_day_gain_pct,
    ROUND(var_95_percent * 100, 2) as var_95_daily_loss_pct,
    ROUND(var_99_percent * 100, 2) as var_99_daily_loss_pct,
    
    -- Risk-Adjusted Return (Sharpe Ratio approximation)
    ROUND(mean_return / NULLIF(volatility, 0), 3) as risk_adjusted_return,
    
    -- Risk Classification
    CASE 
        WHEN volatility * 100 <= 2.0 THEN 'Low Risk'
        WHEN volatility * 100 <= 4.0 THEN 'Medium Risk'
        WHEN volatility * 100 <= 6.0 THEN 'High Risk'
        ELSE 'Very High Risk'
    END as risk_category
    
FROM return_statistics
ORDER BY risk_adjusted_return DESC;

-- =====================================================
-- QUERY 2: SECTOR RISK CONCENTRATION ANALYSIS
-- Business Question: Are we too concentrated in high-risk sectors?
-- =====================================================

WITH sector_metrics AS (
    SELECT 
        cf.sector,
        COUNT(DISTINCT cf.symbol) as companies_count,
        SUM(cf.market_cap) as total_market_cap,
        AVG(sp.daily_change) as avg_sector_return,
        STDDEV(sp.daily_change) as sector_volatility,
        SUM(cf.market_cap) / (SELECT SUM(market_cap) FROM company_fundamentals) as sector_weight,
        
        -- Downside risk metrics
        AVG(CASE WHEN sp.daily_change < 0 THEN sp.daily_change END) as avg_down_day_loss,
        COUNT(CASE WHEN sp.daily_change < -0.05 THEN 1 END) as extreme_loss_days,
        COUNT(*) as total_observations
        
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    AND cf.market_cap > 0
    GROUP BY cf.sector
),
sector_correlation AS (
    SELECT 
        s1.sector as sector1,
        s2.sector as sector2,
        COUNT(*) as common_days,
        -- Simplified correlation calculation between sectors
        (AVG(sp1.daily_change * sp2.daily_change) - 
         AVG(sp1.daily_change) * AVG(sp2.daily_change)) /
        (STDDEV(sp1.daily_change) * STDDEV(sp2.daily_change)) as correlation
    FROM stock_prices sp1
    JOIN company_fundamentals s1 ON sp1.symbol = s1.symbol
    JOIN stock_prices sp2 ON sp1.date = sp2.date
    JOIN company_fundamentals s2 ON sp2.symbol = s2.symbol
    WHERE sp1.date >= DATE('2025-09-01', '-90 days')
    AND s1.sector != s2.sector
    AND s1.sector < s2.sector  -- Avoid duplicates
    GROUP BY s1.sector, s2.sector
    HAVING COUNT(*) >= 30
)
SELECT 
    sm.sector,
    sm.companies_count,
    ROUND(sm.total_market_cap/1000000000, 1) as market_cap_billions,
    ROUND(sm.sector_weight * 100, 1) as portfolio_weight_pct,
    ROUND(sm.avg_sector_return * 100, 3) as avg_daily_return_pct,
    ROUND(sm.sector_volatility * 100, 2) as volatility_pct,
    ROUND(sm.avg_down_day_loss * 100, 2) as avg_loss_day_pct,
    sm.extreme_loss_days,
    ROUND((sm.extreme_loss_days * 100.0) / (sm.total_observations/sm.companies_count), 1) as extreme_loss_frequency_pct,
    
    -- Risk-adjusted metrics
    ROUND(sm.avg_sector_return / sm.sector_volatility, 3) as sector_sharpe_ratio,
    
    -- Concentration risk warning
    CASE 
        WHEN sm.sector_weight > 0.4 THEN 'HIGH CONCENTRATION RISK'
        WHEN sm.sector_weight > 0.25 THEN 'MEDIUM CONCENTRATION RISK'
        ELSE 'ACCEPTABLE CONCENTRATION'
    END as concentration_risk
    
FROM sector_metrics sm
ORDER BY sm.sector_weight DESC;

-- =====================================================
-- QUERY 3: LIQUIDITY RISK ANALYSIS
-- Business Question: Which stocks might be hard to exit during market stress?
-- =====================================================

WITH liquidity_metrics AS (
    SELECT 
        sp.symbol,
        cf.company,
        cf.market_cap,
        AVG(sp.volume) as avg_daily_volume,
        AVG(sp.close_price * sp.volume) as avg_dollar_volume,
        STDDEV(sp.volume) as volume_volatility,
        MIN(sp.volume) as min_daily_volume,
        
        -- Liquidity ratios
        AVG(sp.volume) / NULLIF(AVG(sp.close_price * sp.volume/sp.close_price), 0) as volume_consistency,
        
        -- Days with unusually low volume (liquidity stress indicator)
        COUNT(CASE WHEN sp.volume < (AVG(sp.volume) OVER (PARTITION BY sp.symbol) * 0.5) THEN 1 END) as low_volume_days,
        COUNT(*) as total_days,
        
        -- Price impact estimation (volatility during high/low volume days)
        AVG(CASE WHEN sp.volume_ratio > 2.0 THEN ABS(sp.daily_change) END) as high_volume_volatility,
        AVG(CASE WHEN sp.volume_ratio < 0.5 THEN ABS(sp.daily_change) END) as low_volume_volatility
        
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    GROUP BY sp.symbol, cf.company, cf.market_cap
)
SELECT 
    symbol,
    company,
    ROUND(market_cap/1000000000, 1) as market_cap_billions,
    ROUND(avg_daily_volume/1000000, 1) as avg_volume_millions,
    ROUND(avg_dollar_volume/1000000, 1) as avg_dollar_volume_millions,
    ROUND(volume_volatility/avg_daily_volume * 100, 1) as volume_variability_pct,
    low_volume_days,
    ROUND((low_volume_days * 100.0) / total_days, 1) as low_liquidity_days_pct,
    ROUND(high_volume_volatility * 100, 2) as high_vol_day_volatility_pct,
    ROUND(low_volume_volatility * 100, 2) as low_vol_day_volatility_pct,
    
    -- Liquidity Score (0-100, higher = more liquid)
    ROUND(
        LEAST(100, 
            (LOG(avg_dollar_volume/1000000) * 10) +  -- Dollar volume factor
            (50 - (low_volume_days * 100.0 / total_days)) +  -- Consistency factor
            (50 - LEAST(50, volume_volatility/avg_daily_volume * 100))  -- Stability factor
        ), 1
    ) as liquidity_score,
    
    -- Liquidity Risk Assessment
    CASE 
        WHEN avg_dollar_volume < 10000000 THEN 'HIGH LIQUIDITY RISK'  -- Less than $10M daily
        WHEN avg_dollar_volume < 50000000 THEN 'MEDIUM LIQUIDITY RISK'  -- Less than $50M daily
        WHEN (low_volume_days * 100.0 / total_days) > 20 THEN 'INCONSISTENT LIQUIDITY'
        ELSE 'GOOD LIQUIDITY'
    END as liquidity_risk_level
    
FROM liquidity_metrics
ORDER BY liquidity_score DESC;

-- =====================================================
-- QUERY 4: PORTFOLIO STRESS TEST SCENARIOS
-- Business Question: How would the portfolio perform in different market scenarios?
-- =====================================================

WITH portfolio_base AS (
    SELECT 
        sp.symbol,
        cf.company,
        cf.sector,
        sp.date,
        sp.daily_change,
        cf.market_cap / (SELECT SUM(market_cap) FROM company_fundamentals) as weight
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
    AND cf.market_cap > 0
),
stress_scenarios AS (
    SELECT 
        date,
        -- Scenario 1: Market crash (worst 5% of market days)
        CASE WHEN 
            (SELECT AVG(daily_change) FROM portfolio_base pb2 WHERE pb2.date = pb1.date) <=
            (SELECT PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY avg_return) 
             FROM (SELECT date, AVG(daily_change) as avg_return FROM portfolio_base GROUP BY date))
        THEN 1 ELSE 0 END as market_crash_day,
        
        -- Scenario 2: High volatility (top 10% volatility days)
        CASE WHEN 
            (SELECT STDDEV(daily_change) FROM portfolio_base pb3 WHERE pb3.date = pb1.date) >=
            (SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY daily_vol) 
             FROM (SELECT date, STDDEV(daily_change) as daily_vol FROM portfolio_base GROUP BY date))
        THEN 1 ELSE 0 END as high_volatility_day,
        
        -- Portfolio daily return (weighted average)
        SUM(daily_change * weight) as portfolio_return
        
    FROM portfolio_base pb1
    GROUP BY date
),
scenario_analysis AS (
    SELECT 
        'Normal Market Conditions' as scenario,
        COUNT(CASE WHEN market_crash_day = 0 AND high_volatility_day = 0 THEN 1 END) as days_count,
        AVG(CASE WHEN market_crash_day = 0 AND high_volatility_day = 0 THEN portfolio_return END) as avg_return,
        STDDEV(CASE WHEN market_crash_day = 0 AND high_volatility_day = 0 THEN portfolio_return END) as volatility,
        MIN(CASE WHEN market_crash_day = 0 AND high_volatility_day = 0 THEN portfolio_return END) as worst_day
    FROM stress_scenarios
    
    UNION ALL
    
    SELECT 
        'Market Crash Scenario' as scenario,
        COUNT(CASE WHEN market_crash_day = 1 THEN 1 END) as days_count,
        AVG(CASE WHEN market_crash_day = 1 THEN portfolio_return END) as avg_return,
        STDDEV(CASE WHEN market_crash_day = 1 THEN portfolio_return END) as volatility,
        MIN(CASE WHEN market_crash_day = 1 THEN portfolio_return END) as worst_day
    FROM stress_scenarios
    
    UNION ALL
    
    SELECT 
        'High Volatility Scenario' as scenario,
        COUNT(CASE WHEN high_volatility_day = 1 THEN 1 END) as days_count,
        AVG(CASE WHEN high_volatility_day = 1 THEN portfolio_return END) as avg_return,
        STDDEV(CASE WHEN high_volatility_day = 1 THEN portfolio_return END) as volatility,
        MIN(CASE WHEN high_volatility_day = 1 THEN portfolio_return END) as worst_day
    FROM stress_scenarios
)
SELECT 
    scenario,
    days_count,
    ROUND(avg_return * 100, 3) as avg_daily_return_pct,
    ROUND(volatility * 100, 2) as daily_volatility_pct,
    ROUND(worst_day * 100, 2) as worst_single_day_pct,
    ROUND(avg_return * 252 * 100, 1) as annualized_return_pct,  -- 252 trading days
    ROUND(volatility * SQRT(252) * 100, 1) as annualized_volatility_pct,
    
    -- Risk assessment
    CASE 
        WHEN worst_day < -0.1 THEN 'EXTREME RISK'
        WHEN worst_day < -0.05 THEN 'HIGH RISK'
        WHEN worst_day < -0.03 THEN 'MODERATE RISK'
        ELSE 'LOW RISK'
    END as risk_level
    
FROM scenario_analysis
WHERE days_count > 0
ORDER BY avg_return DESC;

-- =====================================================
-- EXECUTIVE RISK SUMMARY DASHBOARD
-- One-page risk overview for senior management
-- =====================================================

WITH risk_summary AS (
    SELECT 
        COUNT(DISTINCT cf.symbol) as total_companies,
        COUNT(DISTINCT cf.sector) as sectors_covered,
        SUM(cf.market_cap)/1000000000 as total_market_cap_billions,
        AVG(sp.daily_change * 100) as avg_portfolio_return_pct,
        STDDEV(sp.daily_change * 100) as portfolio_volatility_pct,
        MIN(sp.daily_change * 100) as worst_single_day_pct,
        MAX(sp.daily_change * 100) as best_single_day_pct,
        COUNT(CASE WHEN sp.daily_change < -0.05 THEN 1 END) as extreme_loss_events,
        COUNT(*) as total_observations
    FROM stock_prices sp
    JOIN company_fundamentals cf ON sp.symbol = cf.symbol
    WHERE sp.date >= DATE('2025-09-01', '-90 days')
)
SELECT 
    'PORTFOLIO RISK SUMMARY' as report_title,
    total_companies || ' companies across ' || sectors_covered || ' sectors' as portfolio_composition,
    ROUND(total_market_cap_billions, 1) || 'B total market cap' as portfolio_size,
    ROUND(avg_portfolio_return_pct, 3) || '% avg daily return' as performance,
    ROUND(portfolio_volatility_pct, 2) || '% daily volatility' as risk_level,
    ROUND(worst_single_day_pct, 2) || '% worst single day' as maximum_loss,
    extreme_loss_events || ' extreme loss events (' || 
    ROUND((extreme_loss_events * 100.0) / (total_observations/total_companies), 1) || '% frequency)' as tail_risk,
    
    -- Overall risk rating
    CASE 
        WHEN portfolio_volatility_pct > 5.0 THEN 'HIGH RISK PORTFOLIO'
        WHEN portfolio_volatility_pct > 3.0 THEN 'MODERATE RISK PORTFOLIO'
        ELSE 'CONSERVATIVE PORTFOLIO'
    END as overall_risk_assessment
    
FROM risk_summary;

-- =====================================================
-- PORTFOLIO INSIGHTS FOR BUSINESS DECISIONS
-- 
-- These advanced risk analysis queries provide:
-- 1. Quantitative risk assessment (VaR, volatility)
-- 2. Portfolio optimization insights
-- 3. Liquidity risk management
-- 4. Stress testing scenarios
-- 5. Executive-level risk summaries
-- 
-- Business Applications:
-- - Investment committee presentations
-- - Risk management reporting
-- - Strategic asset allocation
-- - Regulatory compliance reporting
-- - Client risk disclosure
-- =====================================================