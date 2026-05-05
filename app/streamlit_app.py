import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models"
DATA_DIR = PROJECT_ROOT / "data" / "processed"

# Load artifacts
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

# App
st.set_page_config(
    page_title="PFA-GA4 Session Scoring",
    layout="wide"
)

st.title("PFA-GA4: Predictive Funnel Analytics")
st.caption("GA4-aligned session scoring, conversion probability, and revenue prioritization")

st.markdown("""
This app scores e-commerce sessions by conversion probability and segments them into business actions.
It demonstrates how GA4-style behavioral data can support marketing, pricing, and replenishment decisions.
""")

# Data input
uploaded_file = st.file_uploader(
    "Upload GA4-style session data, or use the sample deployment dataset",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = load_sample_data()

st.subheader("Input Data Preview")
st.dataframe(df.head(20), use_container_width=True)

# Scoring
missing_cols = [col for col in feature_names if col not in df.columns]

if missing_cols:
    st.error("The uploaded data is missing required model features.")
    st.write(missing_cols)
else:
    X = df[feature_names].copy()

    if "conversion_probability" not in df.columns:
        df["conversion_probability"] = model.predict_proba(X)[:, 1]

    def assign_segment(prob):
        if prob >= 0.80:
            return "High Certainty"
        elif 0.40 <= prob <= 0.70:
            return "At-Risk"
        elif prob < 0.40:
            return "Low Interest"
        else:
            return "Monitor"

    if "segment" not in df.columns:
        df["segment"] = df["conversion_probability"].apply(assign_segment)

    # KPIs
    st.subheader("Model Output Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Sessions Scored",
        f"{len(df):,}"
    )

    col2.metric(
        "Average Conversion Probability",
        f"{df['conversion_probability'].mean():.2%}"
    )

    col3.metric(
        "At-Risk Sessions",
        f"{(df['segment'] == 'At-Risk').sum():,}"
    )

    # Segment Summary
    st.subheader("Segment Summary")

    segment_summary = (
        df.groupby("segment")
        .agg(
            sessions=("segment", "count"),
            avg_conversion_probability=("conversion_probability", "mean")
        )
        .reset_index()
        .sort_values("sessions", ascending=False)
    )

    st.dataframe(segment_summary, use_container_width=True)

    # Business Actions
    st.subheader("Business Interpretation")

    st.markdown("""
    - **High Certainty**: Likely to convert without heavy incentives. Protect margin.
    - **At-Risk**: Strongest intervention group. Consider targeted nudges or selective incentives.
    - **Low Interest**: Lower immediate conversion likelihood. Deprioritize paid incentives.
    - **Monitor**: Middle-zone sessions that may need further review.
    """)


    # Scored Output
    st.subheader("Scored Sessions")

    display_cols = ["conversion_probability", "segment"] + feature_names[:8]
    display_cols = [col for col in display_cols if col in df.columns]

    st.dataframe(
        df[display_cols].head(100),
        use_container_width=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Scored Sessions",
        data=csv,
        file_name="pfa_ga4_scored_sessions.csv",
        mime="text/csv"
    )