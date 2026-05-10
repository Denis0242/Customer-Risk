
SELECT
    customer_id,
    region,
    policy_type,
    loss_amount,
    RANK() OVER(ORDER BY loss_amount DESC) AS customer_rank
FROM customer_risk;
