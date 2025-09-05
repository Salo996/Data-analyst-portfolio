-- =================================================================
-- CUSTOMER ACTIVITY ANALYSIS [MEDIUM]
-- =================================================================
-- Business Question: Which customers haven't bought anything recently?
-- Strategic Value: Find inactive customers to re-engage

-- Customer last order dates
SELECT 
    customer_id,
    MAX(order_date) as last_order_date,
    COUNT(*) as total_orders,
    SUM(order_amount) as total_spent
FROM customer_orders
GROUP BY customer_id
ORDER BY last_order_date DESC;

-- Customers who haven't ordered this year
SELECT 
    customer_id,
    MAX(order_date) as last_order_date,
    SUM(order_amount) as total_spent
FROM customer_orders
WHERE MAX(order_date) < '2024-01-01'
GROUP BY customer_id
ORDER BY total_spent DESC;

-- Customer activity levels
SELECT 
    customer_id,
    SUM(order_amount) as total_spent,
    CASE 
        WHEN MAX(order_date) >= '2024-06-01' THEN 'Active'
        WHEN MAX(order_date) >= '2024-01-01' THEN 'Inactive'
        ELSE 'Very Inactive'
    END as activity_level
FROM customer_orders
GROUP BY customer_id
ORDER BY total_spent DESC;

-- Count customers by activity level
SELECT 
    CASE 
        WHEN MAX(order_date) >= '2024-06-01' THEN 'Active'
        WHEN MAX(order_date) >= '2024-01-01' THEN 'Inactive'
        ELSE 'Very Inactive'
    END as activity_level,
    COUNT(*) as customer_count
FROM customer_orders
GROUP BY customer_id, CASE 
    WHEN MAX(order_date) >= '2024-06-01' THEN 'Active'
    WHEN MAX(order_date) >= '2024-01-01' THEN 'Inactive'
    ELSE 'Very Inactive'
END
ORDER BY customer_count DESC;

-- =================================================================
-- KEY INSIGHTS: Shows which customers need re-engagement campaigns
-- =================================================================