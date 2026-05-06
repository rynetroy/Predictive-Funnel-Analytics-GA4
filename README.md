![Predictive Funnel Analytics Banner](visualizations/header.png)

# Predictive Funnel Analytics (PFA-GA4)

### Revenue & Conversion Analytics Project  
### A Decision System for Session Scoring, Revenue Prioritization & Demand Signals

**Repository:** [Predictive-Funnel-Analytics-GA4](https://github.com/rynetroy/Predictive-Funnel-Analytics-GA4)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-yellow)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Project-v2.0.0-green)

**Author:** Troy Dela Rosa  
**Tools:** Python · pandas · scikit-learn · XGBoost · SHAP · Streamlit  
**Focus:** Ecommerce Analytics · Revenue Prioritization · Conversion Propensity · Demand Signals · Retail Decision Support

---

## Project Summary

Analyzed GA4-style ecommerce session data to build a revenue-based scoring system that prioritizes high-value traffic and supports marketing, pricing, and demand decisions.

Instead of only predicting whether a session will convert, the model ranks sessions by expected revenue and maps each session to a recommended business action.

The goal is to help answer:

> Which sessions deserve attention, which should be protected from unnecessary discounting, and which should be deprioritized?

This project is designed as an analytics prototype that connects:

```text
Behavior → Revenue → Business Action
```

---

## Analytical Work Performed

This project combines business analysis, data preparation, machine learning, validation, and deployment into one end-to-end workflow.

Key work completed:

- Cleaned and structured event, customer, transaction, product, and campaign data for analysis
- Aggregated raw ecommerce events into session-level records for scoring
- Engineered behavioural, customer-history, traffic-source, and funnel-stage features
- Built and compared conversion models using Logistic Regression, Random Forest, and XGBoost
- Selected the final XGBoost classifier based on ranking performance and buyer identification
- Tested spend-estimation approaches and separated purchase intent from customer wallet potential
- Created an expected revenue scoring framework using conversion probability and predicted spend
- Performed leakage checks, train / validation / test splitting, probability calibration, and decile lift analysis
- Used SHAP explainability to interpret model drivers
- Translated model outputs into business segments and recommended actions
- Developed a Streamlit app for session scoring, reporting, and business exploration

---

## How to Test This Project

You can validate this project quickly through either the scored sample file or the interactive Streamlit app.

### Option 1 — No Setup

1. Open:

```text
data/processed/scored_sample_sessions.csv
```

2. Sort by:

```text
expected_revenue
```

3. Compare top-ranked sessions against bottom-ranked sessions.

You should see how high-value sessions are prioritized over low-intent traffic.

---

### Option 2 — Interactive App

Run the Streamlit app locally:

```bash
python -m streamlit run app/streamlit_app.py
```

The app opens at:

```text
http://localhost:8501
```

![Streamlit App Demo](visualizations/streamlit_app_demo.png)

*Example: session scoring, revenue prioritization, business segmentation, and recommended actions in the Streamlit app.*

Then:

- Click **Load Sample Data**
- View session scoring, segmentation, and demand signals
- Download the scored output

---

### Input Data Requirement

The Streamlit app expects the same feature set used during model training.

For uploaded data, the file must include the required session-level features listed in:

```text
models/feature_names.joblib
```

If the uploaded file is missing required columns, the app will stop and show which features are missing.

The included sample file is already formatted correctly:

```text
data/processed/scored_sample_sessions.csv
```

This mirrors a real deployment requirement: production scoring data must follow the same feature schema used during training.

---

### What to Look For

- Higher conversion concentration in top-ranked sessions
- Revenue concentrated in top segments
- Clear mapping from model output to business action

---

## The Business Problem

In e-commerce, most sessions do not convert.

That creates a practical business problem:

- Marketing spend can be applied too broadly
- Discounts may be given to users who would have converted anyway
- Mid-funnel users who might respond to a nudge can be missed
- Low-value sessions can consume budget that could be better used elsewhere

The result is inefficient spending, weaker margin control, and missed revenue opportunities.

---

## The Solution

This project builds a two-stage scoring framework that ranks sessions by **expected revenue**, not just conversion probability.

> **Expected Revenue = P(Convert) × Predicted Spend**

This shifts decision-making from:

> “Will this session convert?”

to:

> “How valuable is this session, and what action should the business take?”

The workflow is designed to approximate a GA4-style ecommerce event pipeline, where raw event interactions are aggregated into session-level features for scoring and prioritization.

---

## Key Results

| Metric | Result |
|---|---:|
| Baseline conversion rate | 5.16% |
| Top 10% conversion rate | 15.33% |
| Lift over baseline | 3.0× |
| ROC-AUC | 0.80 |
| Calibrated expected revenue | $1.97M |
| Actual test revenue | $1.74M |

The model is strongest as a **ranking and prioritization layer**. It helps identify where marketing, merchandising, or recovery actions may deserve attention first.

Top-ranked sessions captured a disproportionate share of expected revenue, showing how the framework could improve targeting efficiency and reduce wasted marketing spend.

---

## How It Works

### Stage 1 — Conversion Propensity

The first stage estimates whether a session is likely to convert.

- **Model:** XGBoost classifier
- **Output:** Probability of purchase
- **Purpose:** Rank sessions by purchase intent

### Stage 2 — Spend Estimation

The second stage estimates how much the customer may spend if they convert.

- Uses customer history instead of only session behaviour
- Predicts expected basket value
- Separates purchase intent from customer wallet potential

### Final Output

Each session receives:

- Conversion probability
- Predicted spend
- Expected revenue
- Business segment
- Recommended action

---

## Business Output

| Segment | Meaning | Recommended Action |
|---|---|---|
| High Certainty | Likely to convert | Protect margin; avoid unnecessary discounts |
| At-Risk | Persuadable users | Target with selective incentives or recovery actions |
| Monitor | Unclear intent | Wait for stronger signals before intervening |
| Low Interest | Low likelihood | Reduce conversion-focused spend |

This makes the output easier to use because the model does not stop at a score. It translates that score into a business decision.

---

## Why This Matters

Most analytics projects stop at prediction.

This project focuses on what comes after prediction:

```text
Model Output → Prioritization → Business Action
```

It can support decisions such as:

- Prioritizing sessions for cart recovery
- Reducing unnecessary discounts for high-certainty buyers
- Ranking audiences for paid media retargeting
- Identifying mid-funnel users who may respond to incentives
- Using session behaviour as an early demand signal
- Connecting marketing activity with merchandising and replenishment planning

---

## Key Insight

> **Clicks signal intent. History signals wallet.**

Session behaviour helps estimate whether someone is likely to buy. Customer history helps estimate how much they may spend.

Separating those signals and recombining them creates a more useful view of customer value.

---

## GA4 Alignment

This project is built around a GA4-style ecommerce workflow.

| Project Concept | GA4-Style Equivalent |
|---|---|
| Event-level user behavior | GA4 event data |
| Session aggregation | Session-level analytics table |
| Customer/session identifier | User and session keys |
| Traffic and campaign signals | Source, medium, campaign fields |
| Purchase revenue | Ecommerce purchase revenue |
| Session scoring | Downstream modeling / activation layer |

The dataset used in this project is synthetic, but its structure is intended to mirror the workflow that could be adapted to GA4 BigQuery export data after validation.

---

## Project Workflow

```text
Raw Data
  ↓
Event Aggregation
  ↓
Feature Engineering
  ↓
Conversion Model
  ↓
Spend Estimation
  ↓
Expected Revenue
  ↓
Business Segmentation
  ↓
Recommended Action
  ↓
Streamlit App
```

---

## Repository Structure

```text
Predictive-Funnel-Analytics-GA4/
│
├── app/
│   └── streamlit_app.py
│
├── models/
│   ├── pfa_ga4_propensity_model.joblib
│   ├── feature_names.joblib
│   └── customer_spend_lookup.csv
│
├── data/
│   └── processed/
│       └── scored_sample_sessions.csv
│
├── notebooks/
│   ├── 01_modeling_pfa_ga4.ipynb
│   └── 02_deployment_prep.ipynb
│
├── visualizations/
│   ├── header.png
│   ├── streamlit_app_demo.png
│   ├── propensity_decile.png
│   └── revenue_opportunity.png
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Quick Start

Clone the repository:

```bash
git clone https://github.com/rynetroy/Predictive-Funnel-Analytics-GA4.git
cd Predictive-Funnel-Analytics-GA4
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python -m streamlit run app/streamlit_app.py
```

The app opens at:

```text
http://localhost:8501
```

---

## Model Validation Highlights

- Train / validation / test split
- Leakage detection and removal
- Model comparison: Logistic Regression, Random Forest, XGBoost
- Probability calibration using Platt scaling
- Decile lift analysis
- SHAP explainability
- Revenue reconciliation

---

## Important Notes

- This project uses a synthetic GA4-style ecommerce dataset
- It is designed as a prototype / analytics case study, not a production-ready system
- This is a ranking and prioritization system. Measuring incremental lift from interventions would be the next phase using A/B testing.

---

## Production Considerations

Before real deployment, this system would require:

- Designed to integrate with GA4 BigQuery export data after validation
- Identity stitching across devices
- Event quality validation
- Attribution logic
- Campaign cost integration
- Product margin and discount-cost logic
- Model drift monitoring
- Experimentation framework for measuring incrementality

---

## About Me

I’m a retail leader transitioning into data analytics, focused on solving real business problems using data.

This project reflects my approach:

> **Not just building models — building decision systems.**
