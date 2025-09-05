-- =================================================================
-- CUSTOMER PURCHASE PATTERNS [MEDIUM-HARD]
-- =================================================================
-- Business Question: How many times do customers make purchases?
-- Strategic Value: Understand customer purchase behavior patterns

-- Customer purchase frequency
SELECT 
    customer_id,
    COUNT(*) as total_purchases,
    SUM(purchase_amount) as total_spent,
    AVG(purchase_amount) as avg_purchase
FROM customer_purchases
GROUP BY customer_id
ORDER BY total_purchases DESC;

-- Purchase frequency categories
SELECT 
    customer_id,
    COUNT(*) as total_purchases,
    CASE 
        WHEN COUNT(*) >= 5 THEN 'Frequent Buyer'
        WHEN COUNT(*) >= 3 THEN 'Regular Buyer'
        WHEN COUNT(*) = 2 THEN 'Occasional Buyer'
        ELSE 'One-time Buyer'
    END as purchase_pattern
FROM customer_purchases
GROUP BY customer_id
ORDER BY total_purchases DESC;

-- Count customers by purchase pattern
SELECT 
    CASE 
        WHEN COUNT(*) >= 5 THEN 'Frequent Buyer'
        WHEN COUNT(*) >= 3 THEN 'Regular Buyer'
        WHEN COUNT(*) = 2 THEN 'Occasional Buyer'
        ELSE 'One-time Buyer'
    END as purchase_pattern,
    COUNT(DISTINCT customer_id) as customer_count
FROM customer_purchases
GROUP BY customer_id, CASE 
    WHEN COUNT(*) >= 5 THEN 'Frequent Buyer'
    WHEN COUNT(*) >= 3 THEN 'Regular Buyer'
    WHEN COUNT(*) = 2 THEN 'Occasional Buyer'
    ELSE 'One-time Buyer'
END
ORDER BY customer_count DESC;

-- Monthly purchase trends
SELECT 
    YEAR(purchase_date) as purchase_year,
    MONTH(purchase_date) as purchase_month,
    COUNT(*) as total_purchases,
    COUNT(DISTINCT customer_id) as unique_customers
FROM customer_purchases
GROUP BY YEAR(purchase_date), MONTH(purchase_date)
ORDER BY purchase_year, purchase_month;

-- =================================================================
-- KEY INSIGHTS: Shows customer purchase frequency and seasonal trends
-- =================================================================