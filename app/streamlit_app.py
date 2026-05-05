import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data" / "processed"

# Page Config
st.set_page_config(
    page_title="PFA-GA4 Session Scoring",
    layout="wide"
)

# Load Artifacts
@st.cache_resource
def load_model():
    return joblib.load(MODELS_DIR / "pfa_ga4_propensity_model.joblib")

@st.cache_data
def load_feature_names():
    return joblib.load(MODELS_DIR / "feature_names.joblib")

@st.cache_data
def load_sample_data():
    return pd.read_csv(DATA_DIR / "scored_sample_sessions.csv")

model = load_model()
feature_names = load_feature_names()

# Helper Functions
def assign_segment(probability):
    if probability >= 0.80:
        return "High Certainty"
    elif 0.40 <= probability <= 0.70:
        return "At-Risk"
    elif probability < 0.40:
        return "Low Interest"
    else:
        return "Monitor"

def assign_business_action(segment):
    actions = {
        "High Certainty": "Protect margin; avoid unnecessary discounting",
        "At-Risk": "Prioritize targeted nudge or selective incentive",
        "Monitor": "Watch for stronger demand signals before intervening",
        "Low Interest": "Deprioritize paid incentive; keep in awareness flow"
    }
    return actions.get(segment, "Review manually")

def assign_demand_signal(probability):
    if probability >= 0.80:
        return "Strong"
    elif probability >= 0.40:
        return "Medium"
    else:
        return "Weak"

# Header
st.title("PFA-GA4: Predictive Funnel Analytics")
st.caption("GA4-aligned session scoring, conversion probability, expected revenue, and demand signal prioritization")

st.markdown("""
This app turns GA4-style e-commerce behavior into business-ready session scores.  
It estimates conversion probability, segments sessions into action groups, and shows how digital behavior can support marketing, pricing, and replenishment decisions.
""")

# Sidebar
st.sidebar.header("About this demo")

st.sidebar.markdown("""
**PFA-GA4** scores e-commerce sessions using a calibrated propensity model.

Core logic:

`Expected Revenue = P(Convert) × Expected Spend`

Use case:
- Prioritize high-value sessions
- Identify at-risk conversion opportunities
- Protect margin on high-certainty buyers
- Translate clickstream behavior into demand signals
""")

st.sidebar.divider()

uploaded_file = st.sidebar.file_uploader(
    "Upload GA4-style session data",
    type=["csv"]
)

use_sample = uploaded_file is None

if use_sample:
    df = load_sample_data()
    st.sidebar.success("Using sample deployment dataset")
else:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Using uploaded dataset")

# Input Preview
st.subheader("Input Data Preview")
st.dataframe(df.head(20), use_container_width=True)

# Validate Features
missing_cols = [col for col in feature_names if col not in df.columns]

if missing_cols:
    st.error("The uploaded data is missing required model features.")
    st.write(missing_cols)
    st.stop()

# Score Sessions
df = df.copy()
X = df[feature_names].copy()

if "conversion_probability" not in df.columns:
    df["conversion_probability"] = model.predict_proba(X)[:, 1]

if "segment" not in df.columns:
    df["segment"] = df["conversion_probability"].apply(assign_segment)

df["business_action"] = df["segment"].apply(assign_business_action)
df["demand_signal"] = df["conversion_probability"].apply(assign_demand_signal)

# Optional expected revenue support
if "expected_spend" in df.columns and "expected_revenue" not in df.columns:
    df["expected_revenue"] = df["conversion_probability"] * df["expected_spend"]

# KPI Summary
st.subheader("Model Output Summary")

sessions_scored = len(df)
avg_probability = df["conversion_probability"].mean()
at_risk_sessions = (df["segment"] == "At-Risk").sum()
high_certainty_sessions = (df["segment"] == "High Certainty").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Sessions Scored", f"{sessions_scored:,}")
col2.metric("Avg. Conversion Probability", f"{avg_probability:.2%}")
col3.metric("At-Risk Sessions", f"{at_risk_sessions:,}")
col4.metric("High-Certainty Sessions", f"{high_certainty_sessions:,}")

if "expected_revenue" in df.columns:
    col5, col6 = st.columns(2)
    col5.metric("Total Expected Revenue", f"${df['expected_revenue'].sum():,.0f}")
    col6.metric("Avg. Expected Revenue / Session", f"${df['expected_revenue'].mean():,.2f}")

# Segment Summary
st.subheader("Segment Summary")

segment_order = ["High Certainty", "At-Risk", "Monitor", "Low Interest"]

segment_summary = (
    df.groupby("segment")
    .agg(
        sessions=("segment", "count"),
        avg_conversion_probability=("conversion_probability", "mean")
    )
    .reset_index()
)

if "expected_revenue" in df.columns:
    revenue_summary = (
        df.groupby("segment")
        .agg(expected_revenue=("expected_revenue", "sum"))
        .reset_index()
    )
    segment_summary = segment_summary.merge(revenue_summary, on="segment", how="left")

segment_summary["segment"] = pd.Categorical(
    segment_summary["segment"],
    categories=segment_order,
    ordered=True
)

segment_summary = segment_summary.sort_values("segment")

st.dataframe(segment_summary, use_container_width=True)

# Business Interpretation
st.subheader("Business Interpretation")

st.markdown("""
| Segment | Meaning | Recommended Action |
|---|---|---|
| High Certainty | Strong likelihood of purchase | Protect margin; avoid unnecessary discounts |
| At-Risk | Meaningful intent but not guaranteed | Prioritize targeted nudges or selective incentives |
| Monitor | Middle-zone behavior | Watch for stronger signals before intervening |
| Low Interest | Lower immediate purchase likelihood | Deprioritize paid incentives |
""")

st.info(
    "The model is best used as a ranking and prioritization layer, not as a perfect revenue prediction engine."
)

# Demand Signal / Replenishment View
st.subheader("Demand Signal View")

st.markdown("""
This section reframes session scoring as an early demand signal.  
For replenishment or inventory-control roles, this helps connect customer behavior to future product/category demand.
""")

demand_summary = (
    df.groupby("demand_signal")
    .agg(
        sessions=("demand_signal", "count"),
        avg_conversion_probability=("conversion_probability", "mean")
    )
    .reset_index()
    .sort_values("avg_conversion_probability", ascending=False)
)

st.dataframe(demand_summary, use_container_width=True)

# Scored Output
st.subheader("Scored Sessions")

display_cols = [
    "conversion_probability",
    "segment",
    "demand_signal",
    "business_action"
]

if "expected_spend" in df.columns:
    display_cols.append("expected_spend")

if "expected_revenue" in df.columns:
    display_cols.append("expected_revenue")

display_cols += feature_names[:8]
display_cols = [col for col in display_cols if col in df.columns]

st.dataframe(
    df[display_cols].head(100),
    use_container_width=True
)

# Download
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Scored Sessions",
    data=csv,
    file_name="pfa_ga4_scored_sessions.csv",
    mime="text/csv"
)