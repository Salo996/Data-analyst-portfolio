-- =================================================================
-- CUSTOMER ACTIVITY SEGMENTATION ANALYSIS [EASY]
-- =================================================================
-- Business Question: How can we group customers by their spending behavior?
-- Strategic Value: Create different customer groups for marketing

-- Customer spending totals
SELECT 
    customer_id,
    SUM(order_amount) as total_spent,
    COUNT(*) as total_orders
FROM customer_orders
GROUP BY customer_id
ORDER BY total_spent DESC;

-- Customer segmentation by spending
SELECT 
    customer_id,
    SUM(order_amount) as total_spent,
    CASE 
        WHEN SUM(order_amount) >= 500 THEN 'VIP Customer'
        WHEN SUM(order_amount) >= 200 THEN 'Regular Customer'
        ELSE 'Budget Customer'
    END as customer_segment
FROM customer_orders
GROUP BY customer_id
ORDER BY total_spent DESC;

-- Count customers in each segment
SELECT 
    CASE 
        WHEN SUM(order_amount) >= 500 THEN 'VIP Customer'
        WHEN SUM(order_amount) >= 200 THEN 'Regular Customer'
        ELSE 'Budget Customer'
    END as customer_segment,
    COUNT(*) as customer_count
FROM customer_orders
GROUP BY customer_id, CASE 
    WHEN SUM(order_amount) >= 500 THEN 'VIP Customer'
    WHEN SUM(order_amount) >= 200 THEN 'Regular Customer'
    ELSE 'Budget Customer'
END
ORDER BY customer_count DESC;

-- =================================================================
-- KEY INSIGHTS: Groups customers by spending levels for marketing
-- =================================================================