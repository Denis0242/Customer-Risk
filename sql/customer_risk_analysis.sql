-- Customer Risk Analysis SQL
-- Assumes table name: customer_risk_claims_cleaned

-- 1. KPI Summary
SELECT
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(claim_amount) AS total_loss,
    SUM(claim_amount) / COUNT(DISTINCT customer_id) AS avg_loss_per_customer,
    100.0 * COUNT(DISTINCT CASE WHEN risk_category = 'High-risk' THEN customer_id END) / COUNT(DISTINCT customer_id) AS high_risk_customer_pct
FROM customer_risk_claims_cleaned;

-- 2. Customer Risk Segmentation
SELECT
    risk_category,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(claim_amount) AS total_loss,
    AVG(risk_score) AS avg_risk_score
FROM customer_risk_claims_cleaned
GROUP BY risk_category
ORDER BY total_loss DESC;

-- 3. Claims Frequency by Age Band
SELECT
    customer_age_band,
    COUNT(claim_id) AS claim_count,
    SUM(claim_amount) AS total_loss
FROM customer_risk_claims_cleaned
GROUP BY customer_age_band
ORDER BY claim_count DESC;

-- 4. Claims vs Loss Customer Detail
SELECT
    customer_id,
    region,
    policy_type,
    customer_age_band,
    MAX(total_claims) AS total_claims,
    MAX(total_loss) AS total_loss,
    MAX(risk_category) AS risk_category,
    MAX(risk_score) AS risk_score
FROM customer_risk_claims_cleaned
GROUP BY customer_id, region, policy_type, customer_age_band
ORDER BY total_loss DESC;

-- 5. Regional Loss Exposure
SELECT
    region,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(claim_amount) AS total_loss,
    AVG(claim_amount) AS avg_claim_amount
FROM customer_risk_claims_cleaned
GROUP BY region
ORDER BY total_loss DESC;

-- 6. Policy Type Risk Analysis
SELECT
    policy_type,
    risk_category,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(claim_amount) AS total_loss
FROM customer_risk_claims_cleaned
GROUP BY policy_type, risk_category
ORDER BY total_loss DESC;

-- 7. Monthly Claim Loss Trend
SELECT
    claim_month,
    COUNT(claim_id) AS total_claims,
    SUM(claim_amount) AS total_loss
FROM customer_risk_claims_cleaned
GROUP BY claim_month
ORDER BY claim_month;
