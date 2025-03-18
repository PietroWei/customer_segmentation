SELECT
    c.customer_id,
    NOW() - MAX(s.sale_date) AS recency,
    COUNT(DISTINCT s.invoice_no) AS frequency,
    SUM(s.total_amount) AS monetary
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
GROUP BY c.customer_id;