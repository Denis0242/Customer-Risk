
WITH risk_summary AS (
    SELECT
        risk_category,
        COUNT(*) AS total_customers,
        SUM(loss_amount) AS total_loss
    FROM customer_risk
    GROUP BY risk_category
)

SELECT *
FROM risk_summary
ORDER BY total_loss DESC;
