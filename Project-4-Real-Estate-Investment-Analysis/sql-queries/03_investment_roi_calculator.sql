-- Real Estate Investment Analysis - Query 3: Investment ROI Calculator
-- Difficulty Level: MEDIUM
-- Purpose: Calculate return on investment metrics for rental properties

-- Description: Comprehensive ROI analysis including cash-on-cash return,
-- cap rates, and investment scoring for rental property evaluation

WITH investment_metrics AS (
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
        property_taxes,
        
        -- Basic investment calculations
        (estimated_rental_income * 12) as annual_rental_income,
        (price * 0.20) as down_payment_20_percent,
        (price * 0.80 * 0.045 / 12) as monthly_mortgage_payment, -- Assuming 4.5% interest
        (property_taxes / 12) as monthly_property_taxes,
        (estimated_rental_income * 0.08) as monthly_maintenance_reserve, -- 8% for maintenance
        
        -- Price per square foot
        ROUND(price / NULLIF(square_feet, 0), 2) as price_per_sqft
        
    FROM properties 
    WHERE price > 0 
      AND estimated_rental_income > 0 
      AND property_taxes > 0
      AND square_feet > 0
)

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
    price_per_sqft,
    
    -- Rental metrics
    estimated_rental_income as monthly_rent,
    annual_rental_income,
    
    -- Investment calculations
    down_payment_20_percent,
    monthly_mortgage_payment,
    monthly_property_taxes,
    monthly_maintenance_reserve,
    
    -- Total monthly expenses
    (monthly_mortgage_payment + monthly_property_taxes + monthly_maintenance_reserve) as total_monthly_expenses,
    
    -- Monthly cash flow
    (estimated_rental_income - (monthly_mortgage_payment + monthly_property_taxes + monthly_maintenance_reserve)) as monthly_cash_flow,
    
    -- Annual cash flow
    ((estimated_rental_income - (monthly_mortgage_payment + monthly_property_taxes + monthly_maintenance_reserve)) * 12) as annual_cash_flow,
    
    -- Cash-on-Cash Return (Annual cash flow / Down payment)
    ROUND(
        ((estimated_rental_income - (monthly_mortgage_payment + monthly_property_taxes + monthly_maintenance_reserve)) * 12) 
        / NULLIF(down_payment_20_percent, 0) * 100, 2
    ) as cash_on_cash_return_percent,
    
    -- Cap Rate (Annual rental income / Purchase price)
    ROUND(annual_rental_income / NULLIF(price, 0) * 100, 2) as cap_rate_percent,
    
    -- Rent-to-Price Ratio (Monthly rent / Purchase price)
    ROUND(estimated_rental_income / NULLIF(price, 0) * 100, 4) as rent_to_price_ratio

FROM investment_metrics
WHERE estimated_rental_income > (monthly_mortgage_payment + monthly_property_taxes + monthly_maintenance_reserve) -- Only profitable properties
ORDER BY cash_on_cash_return_percent DESC
LIMIT 25;