# Customer Risk Analysis Dashboard

![Dashboard Preview](screenshots/customer_risk_dashboard_preview.png)

## 1. Executive Summary

This project analyzes insurance customer risk by combining claim frequency, total loss exposure, customer age band, policy type, and region into a decision-ready dashboard. The goal is to help underwriting, pricing, and claims teams identify high-risk customers, monitor medium-risk customers, and prioritize risk mitigation before loss exposure grows.

**Portfolio positioning:** Data Analyst (Healthcare & Tech) with Product Analytics Skills.

## 2. Business Problem

Insurance teams need a clear way to separate low-risk, medium-risk, and high-risk customers. Without a customer-level risk view, pricing and underwriting teams may treat all customers the same even when a small group creates a large share of claim losses.

## 3. KPI Goals

- Total Customers
- Average Loss per Customer
- Total Loss
- High-Risk Customer %
- Claims Frequency by Age Band
- Customer Allocation by Risk Category
- Loss Contribution by Risk Segment
- Customer Risk Detail Table

## 4. Dataset Overview

- Rows after cleaning: **1,000**
- Columns after cleaning: **15**
- Unique customers: **265**
- Source type: simulated insurance claims/customer risk dataset
- Key fields: `claim_id`, `claim_date`, `customer_id`, `region`, `policy_type`, `customer_age_band`, `tenure_years`, `annual_premium`, `claim_status`, `claim_amount`

## 5. Data Cleaning & EDA

The EDA includes column standardization, date conversion, numeric validation, missing value checks, duplicate checks, categorical validation, outlier review, and customer-level feature engineering.

Main engineered fields:

```text
claim_month = month extracted from claim_date
total_claims = claim count per customer
total_loss = total claim amount per customer
avg_loss = average claim amount per customer
risk_category = High-risk / Medium-risk / Low-risk based on claim and loss thresholds
risk_score = weighted customer risk score
```

## 6. SQL Transformations

SQL queries are included in `sql/customer_risk_analysis.sql` and cover KPI summary, risk segmentation, claims frequency, loss contribution, customer details, and regional/policy risk analysis.

## 7. Metrics Engineering

```text
Total Customers = COUNT(DISTINCT customer_id)
Average Loss per Customer = SUM(claim_amount) / COUNT(DISTINCT customer_id)
Total Loss = SUM(claim_amount)
High-Risk Customer % = High-risk customers / Total customers
Claim Frequency = COUNT(claim_id)
Loss Contribution = SUM(claim_amount) by risk category
```

## 8. Tableau Dashboard Preview

The Tableau dashboard shows executive KPI cards, risk segmentation visuals, claims frequency by age band, loss contribution by segment, and a customer-level risk table.

## 9. Streamlit Dashboard Recreation

The Streamlit app recreates the dashboard with:

- Sidebar filters
- KPI cards
- Risk segmentation donut chart
- Claims vs loss scatter plot
- Claims frequency by age band
- Customer allocation by risk category
- Loss contribution by risk segment
- Customer risk detail table
- Insight, Action, Recommendation, and Decision section

Run locally:

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## 10. Product Insights

- High-risk customers represent **42.64%** of the customer base using the project risk rules.
- **Property** policies contribute the highest total loss in the cleaned dataset.
- **South** is the highest-loss region and should receive underwriting and pricing review priority.
- Customers with higher claim frequency and higher loss amounts should be monitored as early-warning risk accounts.

## 11. Insight, Action, Recommendation, Decision

### Insight
High-risk customers create concentrated financial exposure and require deeper underwriting review.

### Action
Monitor customers crossing claim frequency and loss thresholds, especially by region, policy type, and age band.

### Recommendation
Adjust pricing, strengthen underwriting, and launch targeted risk mitigation for high-risk and medium-risk customers.

### Decision
Prioritize high-risk customer review immediately, monitor medium-risk customers closely, and strengthen underwriting controls for high-loss segments.

## 12. Business Impact

This dashboard helps insurance teams reduce avoidable loss exposure, improve pricing discipline, target underwriting reviews, and support executive risk decisions with customer-level evidence.

## 13. Future Improvements

- Add predictive risk scoring model
- Add customer lifetime value overlay
- Add automated data refresh pipeline
- Add underwriting decision rules
- Add cohort-based claim frequency tracking
