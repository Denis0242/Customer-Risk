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
    st.header("Dashboard Filters")
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
].copy()

filtered_claims = claims[claims["customer_id"].isin(filtered["customer_id"])].copy()

total_customers = filtered["customer_id"].nunique()
total_loss = filtered["total_loss"].sum()
avg_loss = filtered["total_loss"].mean() if total_customers else 0
high_risk_pct = filtered["risk_category"].eq("High-risk").mean() * 100 if total_customers else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Customers", f"{total_customers:,.0f}")
k2.metric("Avg Loss per Customer", f"${avg_loss:,.0f}")
k3.metric("Total Loss", f"${total_loss:,.0f}")
k4.metric("High Risk Customer %", f"{high_risk_pct:.2f}%")

st.divider()

c1, c2, c3 = st.columns([1.25, 1, 1])

with c1:
    st.subheader("Claims vs Loss Segmentation")

    claim_threshold = 4
    loss_threshold = 15000

    fig = px.scatter(
        filtered,
        x="total_claims",
        y="total_loss",
        color="risk_category",
        size="total_loss",
        size_max=24,
        hover_data={
            "customer_id": True,
            "region": True,
            "policy_type": True,
            "customer_age_band": True,
            "risk_category": True,
            "total_claims": True,
            "total_loss": ":,.0f",
            "risk_score": ":.2f",
        },
        labels={
            "total_claims": "Claim Frequency",
            "total_loss": "Total Loss Exposure",
            "risk_category": "Risk Category",
        },
        color_discrete_map={
            "High-risk": "#E45756",
            "Medium-risk": "#F28E2B",
            "Low-risk": "#4E79A7",
        },
    )

    fig.add_vline(
        x=claim_threshold,
        line_dash="dash",
        line_color="gray",
        annotation_text="Claim Threshold",
        annotation_position="top left",
    )

    fig.add_hline(
        y=loss_threshold,
        line_dash="dash",
        line_color="gray",
        annotation_text="Loss Threshold",
        annotation_position="bottom right",
    )

    fig.update_layout(
        height=430,
        showlegend=False,
        margin=dict(l=20, r=20, t=35, b=20),
        xaxis_title="Claim Frequency",
        yaxis_title="Total Loss Exposure",
    )

    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Customer Risk Segmentation")

    risk_counts = (
        filtered.groupby("risk_category", as_index=False)
        .agg(customers=("customer_id", "nunique"), loss=("total_loss", "sum"))
    )

    risk_counts["share"] = risk_counts["customers"] / risk_counts["customers"].sum()

    fig = px.pie(
        risk_counts,
        names="risk_category",
        values="customers",
        hole=0.62,
        color="risk_category",
        color_discrete_map={
            "High-risk": "#E45756",
            "Medium-risk": "#F28E2B",
            "Low-risk": "#4E79A7",
        },
    )

    fig.update_traces(
        textposition="outside",
        textinfo="label+percent",
        pull=[0.04 if x == "High-risk" else 0 for x in risk_counts["risk_category"]],
    )

    fig.update_layout(
        height=430,
        showlegend=False,
        margin=dict(l=10, r=10, t=35, b=10),
        annotations=[
            dict(
                text=f"<b>Total Customers</b><br>{total_customers:,.0f}",
                x=0.5,
                y=0.5,
                font_size=15,
                showarrow=False,
            )
        ],
    )

    st.plotly_chart(fig, use_container_width=True)

with c3:
    st.subheader("Claims Frequency by Age Band")

    age_freq = (
        filtered_claims.groupby("customer_age_band", as_index=False)
        .agg(claims=("claim_id", "count"))
        .sort_values("claims", ascending=False)
    )

    fig = px.bar(
        age_freq,
        x="customer_age_band",
        y="claims",
        text="claims",
        labels={"claims": "Claims", "customer_age_band": "Age Band"},
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(height=430, showlegend=False, margin=dict(l=10, r=10, t=35, b=20))
    st.plotly_chart(fig, use_container_width=True)

c4, c5 = st.columns(2)

with c4:
    st.subheader("Customer Allocation by Risk Category")

    alloc = (
        filtered.groupby("risk_category", as_index=False)
        .agg(customers=("customer_id", "nunique"))
        .sort_values("customers", ascending=False)
    )

    fig = px.bar(
        alloc,
        x="risk_category",
        y="customers",
        color="risk_category",
        text="customers",
        color_discrete_map={
            "High-risk": "#E45756",
            "Medium-risk": "#F28E2B",
            "Low-risk": "#4E79A7",
        },
    )

    fig.update_layout(showlegend=False, height=360)
    st.plotly_chart(fig, use_container_width=True)

with c5:
    st.subheader("Loss Contribution by Risk Segment")

    loss_seg = (
        filtered.groupby("risk_category", as_index=False)
        .agg(total_loss=("total_loss", "sum"))
        .sort_values("total_loss", ascending=True)
    )

    fig = px.bar(
        loss_seg,
        x="total_loss",
        y="risk_category",
        orientation="h",
        color="risk_category",
        text="total_loss",
        color_discrete_map={
            "High-risk": "#E45756",
            "Medium-risk": "#F28E2B",
            "Low-risk": "#4E79A7",
        },
        labels={"total_loss": "Total Loss", "risk_category": "Risk Segment"},
    )

    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(showlegend=False, height=360)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer Risk Detail Table")

detail_cols = [
    "customer_id",
    "region",
    "policy_type",
    "customer_age_band",
    "total_claims",
    "total_loss",
    "avg_loss",
    "risk_category",
    "risk_score",
]

st.dataframe(
    filtered[detail_cols].sort_values("total_loss", ascending=False).head(top_n),
    use_container_width=True,
)

st.divider()

st.markdown("## Executive Decision Summary")

st.markdown("""
<style>
.summary-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-top: 20px;
}
.summary-title {
    font-size: 30px;
    font-weight: 800;
    margin-bottom: 18px;
    color: #303342;
}
.summary-card {
    padding: 24px;
    border-radius: 10px;
    font-size: 18px;
    line-height: 1.6;
    min-height: 210px;
}
.insight-card {
    background-color: #E8F2FF;
    color: #0057B8;
}
.action-card {
    background-color: #FFFDE7;
    color: #8A6500;
}
.recommendation-card {
    background-color: #E6F7EC;
    color: #087B32;
}
.decision-card {
    background-color: #FDE7E9;
    color: #B3262E;
}
</style>

<div class="summary-container">

<div>
    <div class="summary-title">🔎 Insight</div>
    <div class="summary-card insight-card">
        High-risk customers represent <b>36.23%</b> of the customer base and contribute <b>65.54%</b> of total loss exposure.
    </div>
</div>

<div>
    <div class="summary-title">⚙️ Action</div>
    <div class="summary-card action-card">
        Monitor customers with claim frequency above <b>5</b> or claim losses above <b>$2,914</b>.
    </div>
</div>

<div>
    <div class="summary-title">✅ Recommendation</div>
    <div class="summary-card recommendation-card">
        Strengthen underwriting reviews for <b>Property</b> policies and prioritize risk-control actions in the <b>South</b> region.
    </div>
</div>

<div>
    <div class="summary-title">⭐ Decision</div>
    <div class="summary-card decision-card">
        Prioritize high-risk customers for review, monitor medium-risk customers closely, and launch risk-mitigation programs to reduce future claim exposure.
    </div>
</div>

</div>
""", unsafe_allow_html=True)