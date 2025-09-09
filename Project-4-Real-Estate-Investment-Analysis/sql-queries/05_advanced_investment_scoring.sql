-- Real Estate Investment Analysis - Query 5: Advanced Investment Scoring Algorithm
-- Difficulty Level: MEDIUM-HARD  
-- Purpose: Create comprehensive investment scoring system with risk assessment

-- Description: Multi-factor investment scoring algorithm that combines financial metrics,
-- location desirability, market conditions, and risk factors to rank investment opportunities

WITH property_metrics AS (
    SELECT 
        p.*,
        m.avg_area_price,
        m.market_trend,
        m.area_appreciation_rate,
        e.unemployment_rate,
        e.crime_rate,
        e.school_rating,
        
        -- Financial metrics
        (p.estimated_rental_income * 12) as annual_rental_income,
        (p.price * 0.20) as down_payment,
        (p.estimated_rental_income * 12 / NULLIF(p.price, 0) * 100) as cap_rate,
        
        -- Location metrics  
        (p.price / NULLIF(m.avg_area_price, 0)) as price_to_area_avg_ratio,
        
        -- Cash flow calculations
        (p.estimated_rental_income - 
         (p.price * 0.80 * 0.045 / 12) -  -- Mortgage payment
         (p.property_taxes / 12) -         -- Monthly taxes
         (p.estimated_rental_income * 0.10) -- Maintenance/vacancy reserve
        ) as monthly_cash_flow
        
    FROM properties p
    LEFT JOIN market_data m ON p.zip_code = m.zip_code
    LEFT JOIN economic_indicators e ON p.zip_code = e.zip_code
    WHERE p.price > 0 
      AND p.estimated_rental_income > 0
      AND p.square_feet > 0
),

scored_properties AS (
    SELECT 
        *,
        
        -- Scoring components (0-100 scale each)
        
        -- 1. Cash Flow Score (25% weight)
        CASE 
            WHEN monthly_cash_flow <= 0 THEN 0
            WHEN monthly_cash_flow >= 1000 THEN 100
            ELSE ROUND(monthly_cash_flow / 10, 0)
        END as cash_flow_score,
        
        -- 2. Cap Rate Score (20% weight) 
        CASE 
            WHEN cap_rate <= 3 THEN 20
            WHEN cap_rate >= 12 THEN 100
            ELSE ROUND(20 + (cap_rate - 3) * 80 / 9, 0)
        END as cap_rate_score,
        
        -- 3. Location Desirability Score (25% weight)
        ROUND(
            (CASE WHEN school_rating IS NOT NULL THEN school_rating ELSE 5 END * 10) +  -- School rating (0-10 scale)
            (CASE 
                WHEN crime_rate <= 2 THEN 30
                WHEN crime_rate <= 5 THEN 20  
                WHEN crime_rate <= 8 THEN 10
                ELSE 0 
            END) +  -- Crime safety score
            (CASE 
                WHEN unemployment_rate <= 3 THEN 20
                WHEN unemployment_rate <= 6 THEN 15
                WHEN unemployment_rate <= 10 THEN 10
                ELSE 5
            END), 0  -- Economic stability score
        ) as location_score,
        
        -- 4. Market Conditions Score (15% weight)
        CASE 
            WHEN market_trend = 'Strong Growth' THEN 90
            WHEN market_trend = 'Moderate Growth' THEN 70
            WHEN market_trend = 'Stable' THEN 50
            WHEN market_trend = 'Declining' THEN 20
            ELSE 40
        END as market_score,
        
        -- 5. Value Score - Price relative to area (15% weight)
        CASE 
            WHEN price_to_area_avg_ratio <= 0.8 THEN 100  -- 20% below area average
            WHEN price_to_area_avg_ratio <= 0.9 THEN 80   -- 10% below area average  
            WHEN price_to_area_avg_ratio <= 1.1 THEN 60   -- Within 10% of average
            WHEN price_to_area_avg_ratio <= 1.2 THEN 40   -- 20% above average
            ELSE 20  -- More than 20% above average
        END as value_score
        
    FROM property_metrics
    WHERE monthly_cash_flow IS NOT NULL
),

final_scoring AS (
    SELECT 
        property_id,
        address,
        city,
        state,
        zip_code,
        price,
        bedrooms,
        bathrooms,
        square_feet,
        estimated_rental_income,
        monthly_cash_flow,
        cap_rate,
        
        -- Individual scores
        cash_flow_score,
        cap_rate_score, 
        location_score,
        market_score,
        value_score,
        
        -- Weighted composite score
        ROUND(
            (cash_flow_score * 0.25) +
            (cap_rate_score * 0.20) +
            (location_score * 0.25) +
            (market_score * 0.15) +
            (value_score * 0.15), 1
        ) as composite_investment_score,
        
        -- Risk assessment
        CASE 
            WHEN monthly_cash_flow < 200 THEN 'High Risk'
            WHEN cap_rate < 5 THEN 'Medium-High Risk'
            WHEN location_score < 40 THEN 'Medium Risk'
            WHEN market_score < 50 THEN 'Medium Risk'
            ELSE 'Low-Medium Risk'
        END as risk_level,
        
        -- Investment recommendation
        CASE 
            WHEN monthly_cash_flow > 400 AND cap_rate > 7 AND location_score > 60 THEN 'Strong Buy'
            WHEN monthly_cash_flow > 200 AND cap_rate > 6 AND location_score > 50 THEN 'Buy' 
            WHEN monthly_cash_flow > 100 AND cap_rate > 5 THEN 'Consider'
            WHEN monthly_cash_flow > 0 THEN 'Marginal'
            ELSE 'Avoid'
        END as investment_recommendation
        
    FROM scored_properties
)

SELECT 
    property_id,
    address,
    city,
    state,
    zip_code,
    CONCAT('$', FORMAT(price, 0)) as formatted_price,
    bedrooms,
    bathrooms,
    square_feet,
    CONCAT('$', FORMAT(estimated_rental_income, 0)) as monthly_rent,
    CONCAT('$', FORMAT(monthly_cash_flow, 0)) as monthly_cash_flow,
    ROUND(cap_rate, 2) as cap_rate_percent,
    composite_investment_score,
    risk_level,
    investment_recommendation,
    
    -- Score breakdown for transparency
    CONCAT(
        'CF:', cash_flow_score, ' ',
        'CR:', cap_rate_score, ' ', 
        'LOC:', location_score, ' ',
        'MKT:', market_score, ' ',
        'VAL:', value_score
    ) as score_breakdown
    
FROM final_scoring
WHERE composite_investment_score > 50  -- Only show decent opportunities
ORDER BY composite_investment_score DESC, monthly_cash_flow DESC
LIMIT 30;