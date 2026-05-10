
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Customer Risk Intelligence Platform")

df = pd.read_csv("../data/customer_risk.csv")

st.metric("Total Customers", len(df))

st.dataframe(df.head())
