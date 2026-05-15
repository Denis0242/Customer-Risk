import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Customer Risk Analysis Dashboard", layout="wide")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "customer_risk_customer_summary.csv"
CLAIMS_PATH = Path(__file__).resolve().parents[1] / "data" / "customer_risk_claims_cleaned.csv"

@st.cache_data
def load_data():
    customers = pd.read_csv(DATA_PATH, parse_dates=["latest_claim_date"])
    claims = pd.read_csv(CLAIMS_PATH, parse_dates=["claim_date"])
    return customers, claims

customers, claims = load_data()

st.title("Customer Risk Analysis Dashboard")
st.caption("Insurance customer risk segmentation using claim frequency, loss exposure, region, policy type, and age band.")

with st.sidebar:
    st.header("Filters")
    regions = st.multiselect("Region", sorted(customers["region"].dropna().unique()), default=sorted(customers["region"].dropna().unique()))
    policies = st.multiselect("Policy Type", sorted(customers["policy_type"].dropna().unique()), default=sorted(customers["policy_type"].dropna().unique()))
    age_bands = st.multiselect("Customer Age Band", sorted(customers["customer_age_band"].dropna().unique()), default=sorted(customers["customer_age_band"].dropna().unique()))
    risk_categories = st.multiselect("Risk Category", sorted(customers["risk_category"].dropna().unique()), default=sorted(customers["risk_category"].dropna().unique()))
    top_n = st.slider("Top N Customers", min_value=5, max_value=25, value=10)

filtered = customers[
    customers["region"].isin(regions)
    & customers["policy_type"].isin(policies)
    & customers["customer_age_band"].isin(age_bands)
    & customers["risk_category"].isin(risk_categories)
]
filtered_claims = claims[claims["customer_id"].isin(filtered["customer_id"])]

total_customers = filtered["customer_id"].nunique()
total_loss = filtered["total_loss"].sum()
avg_loss = filtered["total_loss"].mean() if total_customers else 0
high_risk_pct = (filtered["risk_category"].eq("High-risk").mean() * 100) if total_customers else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Customers", f"{total_customers:,.0f}")
k2.metric("Avg Loss per Customer", f"${avg_loss:,.0f}")
k3.metric("Total Loss", f"${total_loss:,.0f}")
k4.metric("High Risk Customer %", f"{high_risk_pct:.2f}%")

st.divider()

c1, c2, c3 = st.columns([1.2, 1, 1])

with c1:
    st.subheader("Claims vs Loss Segmentation")
    fig = px.scatter(
        filtered,
        x="total_claims",
        y="total_loss",
        color="risk_category",
        size="risk_score",
        hover_data=["customer_id", "region", "policy_type", "customer_age_band"],
        labels={"total_claims": "Total Claims", "total_loss": "Total Loss"},
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Customer Risk Segmentation")
    risk_counts = filtered.groupby("risk_category", as_index=False)["customer_id"].nunique()
    fig = px.pie(risk_counts, names="risk_category", values="customer_id", hole=0.55)
    fig.update_traces(textinfo="label+percent")
    st.plotly_chart(fig, use_container_width=True)

with c3:
    st.subheader("Claims Frequency by Age Band")
    age_freq = filtered_claims.groupby("customer_age_band", as_index=False)["claim_id"].count()
    fig = px.bar(age_freq, x="customer_age_band", y="claim_id", text="claim_id", labels={"claim_id": "Claims", "customer_age_band": "Age Band"})
    st.plotly_chart(fig, use_container_width=True)

c4, c5 = st.columns(2)
with c4:
    st.subheader("Customer Allocation by Risk Category")
    alloc = filtered.groupby("risk_category", as_index=False)["customer_id"].nunique().sort_values("customer_id", ascending=False)
    fig = px.bar(alloc, x="risk_category", y="customer_id", text="customer_id", labels={"customer_id": "Customers"})
    st.plotly_chart(fig, use_container_width=True)

with c5:
    st.subheader("Loss Contribution by Risk Segment")
    loss_seg = filtered.groupby("risk_category", as_index=False)["total_loss"].sum().sort_values("total_loss", ascending=True)
    fig = px.bar(loss_seg, x="total_loss", y="risk_category", orientation="h", text="total_loss", labels={"total_loss": "Total Loss", "risk_category": "Risk Segment"})
    fig.update_traces(texttemplate="$%{text:,.0f}")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer Risk Detail Table")
detail_cols = ["customer_id", "region", "policy_type", "customer_age_band", "total_claims", "total_loss", "avg_loss", "risk_category", "risk_score"]
st.dataframe(filtered[detail_cols].sort_values("total_loss", ascending=False).head(top_n), use_container_width=True)

st.divider()
st.header("Executive Decision Summary")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("### Insight")
    st.write("High-risk customers create concentrated financial exposure and require deeper underwriting review.")
with col2:
    st.markdown("### Action")
    st.write("Monitor customers crossing claim frequency and loss thresholds by region, policy type, and age band.")
with col3:
    st.markdown("### Recommendation")
    st.write("Adjust pricing, strengthen underwriting, and launch targeted risk mitigation for high-risk and medium-risk customers.")
with col4:
    st.markdown("### Decision")
    st.write("Prioritize high-risk customer review immediately and strengthen underwriting controls for high-loss segments.")
