-- Real Estate Investment Analysis - Query 4: Market Trends Analysis
-- Difficulty Level: MEDIUM
-- Purpose: Analyze historical market trends and seasonal patterns

-- Description: Time series analysis of housing prices, market velocity,
-- and seasonal trends to identify optimal buying/selling periods

-- Historical price trends by quarter
WITH quarterly_trends AS (
    SELECT 
        EXTRACT(YEAR FROM listing_date) as year,
        EXTRACT(QUARTER FROM listing_date) as quarter,
        COUNT(*) as listings_count,
        AVG(price) as avg_price,
        AVG(days_on_market) as avg_days_on_market,
        AVG(price_per_sqft) as avg_price_per_sqft
    FROM properties 
    WHERE listing_date IS NOT NULL 
      AND price > 0 
      AND days_on_market > 0
      AND listing_date >= '2020-01-01'  -- Focus on recent trends
    GROUP BY EXTRACT(YEAR FROM listing_date), EXTRACT(QUARTER FROM listing_date)
)

SELECT 
    year,
    quarter,
    CONCAT('Q', quarter, ' ', year) as period,
    listings_count,
    ROUND(avg_price, 0) as avg_price,
    ROUND(avg_days_on_market, 1) as avg_days_on_market,
    ROUND(avg_price_per_sqft, 2) as avg_price_per_sqft,
    
    -- Quarter-over-quarter price change
    ROUND(
        (avg_price - LAG(avg_price) OVER (ORDER BY year, quarter)) 
        / NULLIF(LAG(avg_price) OVER (ORDER BY year, quarter), 0) * 100, 2
    ) as qoq_price_change_percent,
    
    -- Market velocity indicator (inverse of days on market)
    ROUND(1.0 / NULLIF(avg_days_on_market, 0) * 1000, 2) as market_velocity_index
    
FROM quarterly_trends
ORDER BY year DESC, quarter DESC;

-- Seasonal analysis: Best months to buy/sell
WITH monthly_analysis AS (
    SELECT 
        EXTRACT(MONTH FROM listing_date) as month,
        CASE 
            WHEN EXTRACT(MONTH FROM listing_date) IN (12, 1, 2) THEN 'Winter'
            WHEN EXTRACT(MONTH FROM listing_date) IN (3, 4, 5) THEN 'Spring'
            WHEN EXTRACT(MONTH FROM listing_date) IN (6, 7, 8) THEN 'Summer'
            WHEN EXTRACT(MONTH FROM listing_date) IN (9, 10, 11) THEN 'Fall'
        END as season,
        COUNT(*) as listings_count,
        AVG(price) as avg_price,
        AVG(days_on_market) as avg_days_on_market,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) as median_price
    FROM properties 
    WHERE listing_date IS NOT NULL 
      AND price > 0 
      AND days_on_market > 0
      AND listing_date >= '2022-01-01'
    GROUP BY EXTRACT(MONTH FROM listing_date)
)

SELECT 
    month,
    season,
    listings_count,
    ROUND(avg_price, 0) as avg_price,
    ROUND(median_price, 0) as median_price,
    ROUND(avg_days_on_market, 1) as avg_days_on_market,
    
    -- Seasonal buying opportunity score (lower price + faster sales = better for buyers)
    ROUND(
        (1.0 / NULLIF(avg_days_on_market, 0)) * 
        (1.0 / NULLIF(avg_price, 0)) * 1000000, 2
    ) as buyer_opportunity_score
    
FROM monthly_analysis
ORDER BY month;

-- Market heat analysis by region
SELECT 
    state,
    city,
    COUNT(*) as total_listings,
    AVG(days_on_market) as avg_days_on_market,
    AVG(price) as avg_price,
    
    -- Market classification
    CASE 
        WHEN AVG(days_on_market) <= 30 THEN 'Hot Market'
        WHEN AVG(days_on_market) <= 60 THEN 'Warm Market'  
        WHEN AVG(days_on_market) <= 90 THEN 'Balanced Market'
        ELSE 'Cold Market'
    END as market_temperature,
    
    -- Supply-demand indicator
    ROUND(COUNT(*) / NULLIF(AVG(days_on_market), 0), 2) as supply_demand_ratio
    
FROM properties 
WHERE listing_date >= CURRENT_DATE - INTERVAL '12 months'
  AND days_on_market > 0
GROUP BY state, city
HAVING COUNT(*) >= 10  -- Only cities with significant data
ORDER BY avg_days_on_market ASC
LIMIT 20;