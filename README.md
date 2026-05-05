![Predictive Funnel Analytics Banner](visualizations/header.png)

# Predictive Funnel Analytics (PFA-GA4)

### GA4-Aligned Session Scoring, Revenue Prioritization & Demand Signal Framework

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-yellow)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red)
![Status](https://img.shields.io/badge/Project-Completed-green)

**Author:** Troy Dela Rosa  
**Tools:** Python · pandas · NumPy · scikit-learn · XGBoost · SHAP · Matplotlib · Seaborn · Streamlit · Jupyter  
**Focus:** Ecommerce Analytics · Conversion Propensity · Revenue Prioritization · Demand Signals · Retail Decision Support

---

## Executive Summary

This project answers a practical ecommerce analytics question:

> **Which user sessions should be prioritized for marketing intervention without wasting discounts on users who would likely convert anyway?**

Using a two-stage predictive funnel framework, the project scores ecommerce sessions by:

1. **Conversion probability** — how likely a session is to result in a purchase  
2. **Predicted spend** — how much the customer is expected to spend if they convert  
3. **Expected revenue** — the estimated business value of the session  

The final model ranked sessions effectively on a held-out test set. Sessions in the top decile converted at approximately **3x the baseline conversion rate**, showing that the model can prioritize higher-intent traffic better than random targeting.

The project was also deployed as a **Streamlit business demo**, turning the model into an interactive decision-support tool for session scoring, business segmentation, and demand signal prioritization.

This project was built using a synthetic ecommerce dataset structured similarly to a GA4-style event workflow.

---

## Live Demo

This project includes a Streamlit app:

```text
app/streamlit_app.py
```

The app allows users to:

- Load a sample deployment dataset
- Upload GA4-style session data
- Score sessions by conversion probability
- Segment sessions into business action groups
- View demand signal summaries
- Download scored session output

To run locally:

```bash
python -m streamlit run app/streamlit_app.py
```

---

## Key Results

| Metric | Result |
|---|---:|
| Test ROC-AUC | 0.8014 |
| Baseline conversion rate | 5.16% |
| Model top 10% conversion rate | 15.33% |
| **Top-decile lift** | **3.0x** |
| Calibrated expected revenue | $1.97M |
| Actual test revenue | $1.74M |
| Revenue overestimation after calibration | +13.4% |
| Average predicted conversion before calibration | 35.91% |
| Average predicted conversion after calibration | 5.14% |
| Actual test conversion rate | 5.16% |

The model is strongest as a **ranking and prioritization layer**. Probability calibration improved its usefulness for revenue planning by reducing overconfident conversion estimates.

---

## Core Idea

> **Expected Revenue = P(Convert) × Predicted Spend**

Instead of optimizing for conversion rate alone, this framework estimates the economic value of each session.

A session with high purchase probability but low spend may be less valuable than a lower-probability session with much higher expected basket value. The hurdle model combines both signals into one decision-ready metric.

---

## Why This Project Matters

In many ecommerce funnels:

- Most sessions do not convert
- Marketing spend is often applied too broadly
- Discounts may be given to users who would have converted anyway
- High-potential sessions can be missed because they are not ranked by value
- Digital behaviour is often analyzed separately from revenue and operational planning

This creates avoidable margin pressure and inefficient campaign spend.

This framework helps identify:

- Users likely to convert without an incentive
- Mid-propensity users who may be worth a targeted nudge
- Low-propensity sessions where paid remarketing may be inefficient
- High-value sessions that deserve prioritization
- Behavioural demand signals that can support merchandising or replenishment decisions

---

## Project Workflow

```text
Raw Ecommerce Data
        ↓
GA4-Style Event Aggregation
        ↓
Session-Level Feature Engineering
        ↓
Stage 1: Conversion Propensity Model
        ↓
Stage 2: Customer Spend Estimation
        ↓
Expected Revenue Scoring
        ↓
Business Segmentation
        ↓
Streamlit Decision-Support App
```

---

## Approach

### Stage 1: Conversion Propensity Model

The first stage predicts whether a session will convert.

| Item | Description |
|---|---|
| Model | XGBoost Classifier |
| Target | `is_converted` |
| Output | Probability of purchase |
| Test ROC-AUC | 0.8014 |
| Business use | Rank sessions by likelihood to buy |

The classifier was evaluated against baseline models including Random Forest and Logistic Regression. XGBoost was selected for its strong ranking performance, high buyer recall, and compatibility with SHAP explainability.

---

### Stage 2: Spend Estimation

The second stage estimates how much a user is likely to spend if they convert.

A key finding from the project:

> **Session behaviour predicts intent. Customer history predicts wallet.**

In-session behavioural features performed poorly for spend prediction, while customer-level historical spend was much more useful for estimating basket value.

| Method | Result |
|---|---:|
| Behavioural XGBoost Regressor | R² ≈ -0.01 |
| Segment / customer-history spend estimator | R² ≈ 0.65 |
| Customer-history spend estimator MAE | ≈ $28.57 |

This supports the final two-stage design: use session behaviour for conversion scoring and customer history for spend estimation.

---

## Final Output

For each session, the pipeline produces:

- Conversion probability
- Predicted spend
- Expected revenue
- Business segment
- Demand signal
- Recommended action

| Segment | Meaning | Recommended Action |
|---|---|---|
| High Certainty | Top-ranked sessions by predicted conversion probability | Protect margin; avoid broad discounting |
| At-Risk | Mid-to-high ranked sessions worth prioritizing | Prioritize targeted nudges or selective incentives |
| Monitor | Middle-zone behaviour needing more evidence | Watch for stronger signals before intervening |
| Low Interest | Lower-ranked sessions with weaker purchase signals | Deprioritize paid incentives |

The deployed demo uses a balanced sample to show how the scoring framework separates sessions into decision groups. In production, thresholds should be adjusted based on margin, campaign cost, customer lifetime value, and business risk tolerance.

---

## Streamlit App

The project includes a deployed-app structure:

```text
app/
  streamlit_app.py

models/
  pfa_ga4_propensity_model.joblib
  feature_names.joblib
  customer_spend_lookup.csv

data/
  processed/
    scored_sample_sessions.csv
```

The app demonstrates how the model can be used as a business-facing tool rather than only a notebook experiment.

### App Features

| Feature | Purpose |
|---|---|
| Input data preview | Shows GA4-style session-level data |
| Model output summary | Displays scored sessions, average probability, and segment counts |
| Segment summary | Groups sessions by action category |
| Business interpretation | Converts model output into recommended actions |
| Demand signal view | Reframes session behaviour as early demand signal |
| Download button | Exports scored sessions for business use |

---

## Demand Signal / Replenishment Relevance

Although this project began as a conversion propensity model, it also connects to retail replenishment and inventory analytics.

The logic is:

> **Clicks signal intent. Aggregated over time, they become demand signals.**

Session-level behavioural signals such as product views, add-to-cart activity, campaign source, and conversion probability can help estimate where demand is forming before it appears fully in sales data.

This makes the project relevant to:

- Demand signal monitoring
- Inventory risk prioritization
- Category-level opportunity analysis
- Replenishment exception review
- Marketing and merchandising alignment
- Retail decision support

For replenishment or inventory-control roles, the project demonstrates how clean data pipelines, model scoring, and business rules can support better prioritization.

---

## Example Model Output

| Session ID | P(Convert) | Predicted Spend | Expected Revenue | Segment | Recommended Action |
|---|---:|---:|---:|---|---|
| S-10492 | 0.86 | $124.50 | $107.07 | High Certainty | Avoid broad discounting |
| S-21984 | 0.58 | $96.20 | $55.80 | At-Risk | Send targeted incentive or cart recovery message |
| S-33871 | 0.12 | $42.00 | $5.04 | Low Interest | Suppress paid remarketing or use awareness messaging |

*Illustrative values used to demonstrate the framework.*

---

## Revenue Reconciliation

The original model probabilities were useful for ranking but were not well-calibrated for revenue forecasting. Before calibration, the average predicted conversion rate was much higher than the actual conversion rate.

To correct this, Platt scaling was applied to calibrate predicted probabilities.

| Metric | Value |
|---|---:|
| Average predicted conversion before calibration | 35.91% |
| Average predicted conversion after calibration | 5.14% |
| Actual test conversion rate | 5.16% |
| Calibrated expected revenue | $1,972,962.80 |
| Actual test revenue | $1,739,605.48 |
| Overestimation | +$233,357.32 |
| Overestimation bias | +13.4% |

Calibration reduced overconfidence while preserving ranking performance. Revenue estimates should be interpreted as planning estimates, not guaranteed outcomes.

---

## Targeting Lift

The model was tested against random targeting on the held-out test set.

| Metric | Value |
|---|---:|
| Base conversion rate | 5.16% |
| Random 10% targeting conversion rate | 5.13% |
| Model top 10% targeting conversion rate | 15.33% |
| **Lift over baseline** | **3.0x** |
| Expected revenue, model top 10% | $2,953,630.04 |
| Expected revenue, random 10% | $1,381,257.44 |
| Revenue lift from model ranking | $1,572,372.60 |

This shows that the model is most useful as a prioritization layer for marketing, merchandising, and revenue operations.

---

## Business Interpretation

The model can support ecommerce and retail analytics decisions such as:

- Prioritizing sessions for cart recovery campaigns
- Reducing unnecessary discounts for high-certainty buyers
- Ranking audiences for paid media retargeting
- Identifying mid-funnel users who may respond to incentives
- Supporting merchandising decisions using demand signals
- Improving campaign budget allocation
- Creating a bridge between customer behaviour and replenishment planning

Important note:

> **Propensity models estimate likelihood of conversion, not incremental lift.**

In production, this type of model should be paired with A/B testing or uplift modeling to measure whether an intervention actually caused additional conversions.

---

## GA4 Alignment

This project was designed to approximate a Google Analytics 4 BigQuery export workflow.

| Project Field | Comparable GA4 Field |
|---|---|
| `events.csv` | `events_*` tables |
| `event_type` | `event_name` |
| `customer_id` | `user_pseudo_id` |
| `session_id` | `ga_session_id` |
| `traffic_source` | `traffic_source.medium` / `session_source` |
| `campaign_id` / `channel` | `session_campaign` / `session_medium` |
| `device_type` | `device.category` |
| `purchase_amount` | `ecommerce.purchase_revenue` |

The dataset is synthetic, but the workflow demonstrates how session-level scoring could be adapted to real GA4-style ecommerce data after validating:

- Event quality
- Session logic
- Identity stitching
- Revenue attribution
- Leakage safeguards
- Experimentation design

---

## Data Structure

The dataset contains five relational tables:

| Table | Description |
|---|---|
| `customers` | Customer-level attributes |
| `events` | User interactions such as views, clicks, cart actions, and purchases |
| `transactions` | Completed purchase records |
| `products` | Product metadata |
| `campaigns` | Campaign and channel attributes |

Raw events were aggregated into session-level records using `customer_id` and `session_id`.

---

## Leakage Prevention

Because this project uses funnel data, leakage prevention was a major part of the workflow.

The following fields were excluded from the final classification model:

- `event_purchase`
- `purchase_to_cart_ratio`
- Non-time-aware spend aggregates
- Raw event counts that directly reconstructed funnel outcomes
- Target variables such as `is_converted` and `purchase_amount`

An early version of the model produced suspiciously perfect performance, which indicated leakage. After removing leakage-prone features, the final model produced a more realistic test ROC-AUC of approximately 0.80.

> **A perfect model score is often a bug, not a breakthrough.**

---

## Model Validation

The final notebook includes:

- Train / validation / test split
- Feature leakage audit
- Column alignment checks
- Numeric feature validation
- Classification model comparison
- Threshold tuning
- Regression comparison
- Propensity decile analysis
- SHAP explainability
- Probability calibration using Platt scaling
- Revenue reconciliation
- Saved model artifacts
- Streamlit deployment preparation

---

## Production Considerations

Before deploying this type of model on live ecommerce data, additional validation would be needed for:

- Session fragmentation from timeouts, campaign resets, and cross-device behaviour
- Event duplication and deduplication logic
- Attribution windows and revenue crediting
- Identity stitching across devices and identifiers
- Product-level margin and discount-cost modeling
- Time-aware customer history features
- Incrementality testing through A/B tests or uplift modeling
- Model drift monitoring after deployment
- Forecast and replenishment integration if used for inventory planning

The current project should be viewed as an analytics case study and prototype, not a ready-to-deploy production system.

---

## Dataset

**Source:** Marketing & E-Commerce Analytics Dataset from Kaggle

Dataset scale:

- 100,000 customers
- 2M+ interaction events
- 5 relational tables

The raw dataset is not stored directly in this repository because of file size. To reproduce the notebook, download the dataset separately and place the files in the local `data/` folder.

Expected structure:

```text
data/
  customers.csv
  events.csv
  transactions.csv
  products.csv
  campaigns.csv
```

---

## Repository Structure

```text
Predictive-Funnel-Analytics-GA4/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   └── processed/
│       └── scored_sample_sessions.csv
│
├── models/
│   ├── pfa_ga4_propensity_model.joblib
│   ├── feature_names.joblib
│   ├── customer_spend_lookup.csv
│   └── feature_names.csv
│
├── notebooks/
│   ├── 01_modeling_pfa_ga4.ipynb
│   ├── 02_deployment_prep.ipynb
│   ├── data-audit.ipynb
│   └── predictive-funnel-analytics-GA4-Stakeholder-Report.ipynb
│
├── reports/
│   ├── campaigns_report.html
│   ├── customers_report.html
│   ├── events_sample_report.html
│   ├── products_report.html
│   └── transactions_sample_report.html
│
├── visualizations/
│   ├── header.png
│   ├── propensity_decile.png
│   ├── revenue_opportunity.png
│   └── xgboost_performance.png
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Quick Start

Clone the repository and install the required libraries:

```bash
git clone https://github.com/rynetroy/Predictive-Funnel-Analytics-GA4.git
cd Predictive-Funnel-Analytics-GA4
pip install -r requirements.txt
```

To reproduce the full modeling workflow, download the Marketing & E-Commerce Analytics Dataset from Kaggle and place the CSV files inside the `data/` folder.

Then open and run:

```text
notebooks/01_modeling_pfa_ga4.ipynb
```

To run the deployment demo:

```bash
python -m streamlit run app/streamlit_app.py
```

---

## Project Takeaway

This project shows how ecommerce clickstream data can be transformed into decision-ready business signals.

The key lesson:

> **Clicks signal intent. History signals wallet. Combined properly, they support smarter prioritization.**

PFA-GA4 is not just a model that predicts conversion. It is a framework for turning session behaviour into marketing, revenue, and demand-prioritization decisions.
