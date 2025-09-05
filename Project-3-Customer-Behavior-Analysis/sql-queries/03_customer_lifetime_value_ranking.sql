-- =================================================================
-- CUSTOMER LIFETIME VALUE ANALYSIS [MEDIUM]
-- =================================================================
-- Business Question: Which customers spend the most money?
-- Strategic Value: Find our best customers for special treatment

-- Customer total spending
SELECT 
    customer_id,
    SUM(order_amount) as total_spent,
    COUNT(*) as total_orders,
    AVG(order_amount) as avg_order_value
FROM customer_orders
GROUP BY customer_id
ORDER BY total_spent DESC;

-- Top 10 highest spending customers
SELECT 
    customer_id,
    SUM(order_amount) as total_spent,
    COUNT(*) as total_orders
FROM customer_orders
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- Customer value tiers
SELECT 
    customer_id,
    SUM(order_amount) as total_spent,
    CASE 
        WHEN SUM(order_amount) >= 1000 THEN 'Gold Customer'
        WHEN SUM(order_amount) >= 500 THEN 'Silver Customer'
        ELSE 'Bronze Customer'
    END as customer_tier
FROM customer_orders
GROUP BY customer_id
ORDER BY total_spent DESC;

-- Count customers in each tier
SELECT 
    CASE 
        WHEN SUM(order_amount) >= 1000 THEN 'Gold Customer'
        WHEN SUM(order_amount) >= 500 THEN 'Silver Customer'
        ELSE 'Bronze Customer'
    END as customer_tier,
    COUNT(*) as customer_count
FROM customer_orders
GROUP BY customer_id, CASE 
    WHEN SUM(order_amount) >= 1000 THEN 'Gold Customer'
    WHEN SUM(order_amount) >= 500 THEN 'Silver Customer'
    ELSE 'Bronze Customer'
END
ORDER BY customer_count DESC;

-- =================================================================
-- KEY INSIGHTS: Shows our most valuable customers by total spending
-- =================================================================