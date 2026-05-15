# EDA & Data Cleaning — Customer Risk Analysis

## Cleaning Checklist

```python
import pandas as pd
import numpy as np

df = pd.read_csv("../data/raw_customer_risk.csv")
df.head()
df.shape
df.info()
df.describe()
df.isnull().sum()
df.duplicated().sum()
df.columns
```

## Cleaning Steps Completed

1. Loaded raw customer risk dataset.
2. Reviewed shape, preview rows, column names, and data types.
3. Standardized column names to lowercase snake_case.
4. Converted `claim_date` into datetime format.
5. Converted `tenure_years`, `annual_premium`, and `claim_amount` into numeric fields.
6. Checked missing values and duplicate rows.
7. Removed duplicate records where applicable.
8. Validated categorical fields: region, policy type, age band, and claim status.
9. Validated numeric fields for negative or unrealistic values.
10. Created customer-level total claims, total loss, average loss, and risk category.
11. Created `risk_score` for ranking risky customers.
12. Exported cleaned dataset for SQL, Tableau, and Streamlit.

## Feature Engineering

```python
customer_summary = df.groupby("customer_id").agg(
    total_claims=("claim_id", "count"),
    total_loss=("claim_amount", "sum"),
    avg_loss=("claim_amount", "mean")
).reset_index()

claim_threshold = 4
loss_threshold = 15000

customer_summary["risk_category"] = customer_summary.apply(
    lambda r: "High-risk" if r["total_claims"] >= claim_threshold or r["total_loss"] >= loss_threshold
    else "Medium-risk" if r["total_claims"] >= 2 or r["total_loss"] >= 8000
    else "Low-risk",
    axis=1
)
```

## KPI Validation

```text
Total customers: 265
Total loss: $3,736,031
Average loss per customer: $14,098
High-risk customer %: 42.64%
```

## Insight

The dataset supports customer-level risk segmentation using claim frequency and total loss exposure.

## Action

Use thresholds to identify customers requiring underwriting review.

## Recommendation

Monitor high-risk and medium-risk customers through a recurring dashboard refresh.

## Decision

Prioritize high-risk customer review and strengthen risk controls for high-loss segments.
