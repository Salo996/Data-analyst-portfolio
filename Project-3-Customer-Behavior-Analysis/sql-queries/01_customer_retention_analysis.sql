-- =================================================================
-- CUSTOMER RETENTION ANALYSIS [EASY]
-- =================================================================
-- Business Question: How many customers return after their first purchase?
-- Strategic Value: Identify one-time vs repeat customers

-- Basic customer purchase count
SELECT 
    customer_id,
    COUNT(*) as total_purchases
FROM customer_purchases
GROUP BY customer_id
ORDER BY total_purchases DESC;

-- Customer retention categories
SELECT 
    customer_id,
    COUNT(*) as total_purchases,
    CASE 
        WHEN COUNT(*) = 1 THEN 'One-time Customer'
        WHEN COUNT(*) = 2 THEN 'Returning Customer'
        ELSE 'Loyal Customer'
    END as customer_type
FROM customer_purchases
GROUP BY customer_id
ORDER BY total_purchases DESC;

-- Summary of customer types
SELECT 
    CASE 
        WHEN COUNT(*) = 1 THEN 'One-time Customer'
        WHEN COUNT(*) = 2 THEN 'Returning Customer'
        ELSE 'Loyal Customer'
    END as customer_type,
    COUNT(DISTINCT customer_id) as customer_count
FROM customer_purchases
GROUP BY customer_id, CASE 
    WHEN COUNT(*) = 1 THEN 'One-time Customer'
    WHEN COUNT(*) = 2 THEN 'Returning Customer'
    ELSE 'Loyal Customer'
END
ORDER BY customer_count DESC;

-- =================================================================
-- KEY INSIGHTS: Shows how many customers buy once vs multiple times
-- =================================================================