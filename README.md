![Predictive Funnel Analytics Banner](visualizations/header.png)

# Predictive Funnel Analytics for Ecommerce Revenue Prioritization

### A GA4-Aligned Analytics Project for Session Scoring, Revenue Opportunity, and Marketing Decision Support

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

## TL;DR

Built a GA4-style ecommerce scoring system that ranks sessions by **expected revenue**, not just conversion probability.

The top 10% of scored sessions converted at **15.33%**, roughly **3.0x higher** than the baseline conversion rate of **5.16%**.

The project shows how behavioral analytics can support **marketing prioritization, margin protection, and revenue-focused decision-making**.

---

## Business Context

Ecommerce teams often know how much traffic they receive, but not all traffic deserves the same level of marketing attention.

Some sessions may convert without an incentive. Others may need a targeted nudge. Low-intent sessions can consume budget that could be better used elsewhere.

This project helps answer:

> **Which sessions should marketing, pricing, and ecommerce teams prioritize without wasting discounts on customers who are likely to buy anyway?**

The goal is to connect:

```text
Behavior → Revenue → Business Action
```

---

## Executive Summary

This project developed a two-stage ecommerce scoring framework that ranks sessions by **expected revenue**.

The model identified a clear concentration of purchase intent in the highest-ranked sessions. While the overall test conversion rate was **5.16%**, the top 10% of scored sessions converted at **15.33%**, representing roughly **3.0x lift over baseline**.

The strongest use case is not simply predicting who will buy. The stronger use case is helping teams decide:

- Which sessions deserve attention
- Which customers should be protected from unnecessary discounting
- Which mid-funnel users may respond to selective incentives
- Which low-intent sessions should be deprioritized

### Key Results Snapshot

| Metric | Result |
|---|---:|
| Baseline conversion rate | 5.16% |
| Top 10% conversion rate | 15.33% |
| Lift over baseline | 3.0x |
| ROC-AUC | 0.80 |
| Calibrated expected revenue | $1.97M |
| Actual test revenue | $1.74M |
| Revenue variance | +13.4% over actual |

### Main Business Takeaway

The model is strongest as a **ranking and prioritization layer**.

It translates ecommerce behavior into operational decisions for marketing, pricing, merchandising, and retention teams.

---

## North Star Metrics

| Metric Area | Business Question |
|---|---|
| Conversion rate | Are sessions turning into purchases? |
| Propensity lift | Can high-intent sessions be identified earlier? |
| Expected revenue | Which sessions are likely to be worth the most? |
| Segment actionability | What should the business do with each scored session? |
| Calibration accuracy | Can scores be trusted for planning and prioritization? |

---

## Key Insights

### 1. High-ranked sessions converted at roughly 3x the baseline rate

The model successfully separated high-intent sessions from general traffic.

The overall conversion rate was **5.16%**, while the top decile converted at **15.33%**.

![Propensity Decile Analysis](visualizations/propensity_decile.png)

**Business meaning:**  
Marketing teams can focus campaign spend, retargeting, and recovery actions on sessions with stronger buying signals.

---

### 2. Conversion probability alone is not enough for revenue decisions

A session with high purchase probability is not always the best revenue opportunity.

This project separates:

- **Session behavior**, which signals purchase intent
- **Customer history**, which signals wallet potential

Then combines both signals:

```text
Expected Revenue = Probability of Conversion x Predicted Spend
```

**Business meaning:**  
The decision shifts from “Who is likely to buy?” to “Which session is worth prioritizing?”

---

### 3. The most actionable opportunity sits in the middle of the funnel

High-certainty users may already be likely to convert, so aggressive discounting can reduce margin. Low-interest users may not be worth conversion-focused spend.

The strongest opportunity sits in the middle, where users show enough intent to be worth engaging but may still need a nudge.

![Revenue Opportunity](visualizations/revenue_opportunity.png)

**Business meaning:**  
Mid-propensity users are often the best audience for cart recovery, remarketing, limited-time incentives, or personalized offers.

---

### 4. Calibration made the score more useful for business planning

The initial model was useful for ranking sessions, but its raw probabilities were too high for financial planning.

After probability calibration, expected revenue became more realistic:

| Revenue Measure | Amount |
|---|---:|
| Calibrated expected revenue | $1.97M |
| Actual test revenue | $1.74M |
| Variance | +$233K |
| Percent variance | +13.4% |

**Business meaning:**  
If scores are used for planning or prioritization, calibration helps prevent overconfident revenue estimates.

---

## Recommendations

### 1. Protect margin on high-certainty sessions

High-certainty sessions may already be likely to convert, making aggressive discounting potentially margin-destructive.

**Recommended action:**  
Suppress unnecessary promotions and prioritize non-price messaging such as urgency, reassurance, or product reminders.

---

### 2. Prioritize mid-propensity users for targeted intervention

The At-Risk segment shows buying signals but may still need a reason to complete the purchase.

**Recommended action:**  
Use this group for cart recovery, remarketing, selective incentives, or personalized product messaging.

---

### 3. Use expected revenue instead of conversion probability alone

Conversion probability identifies likely buyers. Expected revenue provides a stronger business ranking.

**Recommended action:**  
Prioritize sessions using expected revenue when budget, incentive cost, or campaign capacity is limited.

---

### 4. Extend the framework to margin before production use

Expected revenue should be paired with product margin, discount cost, and campaign cost.

**Recommended action:**  
Move from expected revenue to expected profit or incremental margin before production deployment.

---

### 5. Validate impact through A/B testing

The model identifies where action may be valuable, but it does not prove incremental lift from intervention.

**Recommended action:**  
Use holdout testing to measure whether targeted actions increase conversion, revenue, or margin.

---

## Business Segmentation Framework

Each scored session is mapped to a recommended action.

| Segment | Meaning | Recommended Action | Primary Stakeholder |
|---|---|---|---|
| High Certainty | Strong likelihood to convert | Protect margin and avoid unnecessary discounts | Marketing, Pricing |
| At-Risk | Persuadable session with meaningful opportunity | Use selective incentives or recovery messaging | Marketing, CRM |
| Monitor | Some signal, but not enough for immediate action | Wait for stronger behavior before spending | Digital Analytics |
| Low Interest | Weak conversion signal | Reduce conversion-focused spend | Paid Media, Growth |

---

## Analytical Work Performed

This project combines business analysis, data preparation, machine learning, validation, and deployment.

Key work completed:

- Cleaned and structured event, customer, transaction, product, and campaign data
- Aggregated ecommerce events into session-level records
- Engineered behavioral, customer-history, traffic-source, and funnel-stage features
- Built and compared Logistic Regression, Random Forest, and XGBoost models
- Selected XGBoost based on ranking performance and buyer identification
- Separated purchase intent from customer wallet potential
- Created an expected revenue scoring framework
- Performed leakage checks, train / validation / test splitting, calibration, and decile lift analysis
- Used SHAP explainability to interpret model drivers
- Translated model outputs into business segments and recommended actions
- Developed a Streamlit app for session scoring and business exploration

---

## How It Works

### Stage 1: Conversion Propensity

The first stage estimates whether a session is likely to convert.

- **Model:** XGBoost classifier
- **Output:** Probability of purchase
- **Purpose:** Rank sessions by purchase intent

### Stage 2: Spend Estimation

The second stage estimates how much the customer may spend if they convert.

- Uses customer history instead of only session behavior
- Estimates expected basket value
- Separates purchase intent from wallet potential

### Final Output

Each session receives:

- Conversion probability
- Predicted spend
- Expected revenue
- Business segment
- Recommended action

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

> Suggested visual addition: convert this workflow into a simple architecture diagram and save it as `visualizations/project_workflow.png`.

---

## Stakeholder Use Cases

| Stakeholder | How This Project Helps |
|---|---|
| Marketing | Prioritize retargeting and cart recovery audiences |
| Pricing | Avoid unnecessary discounting for high-certainty buyers |
| Merchandising | Detect product or category demand signals from session behavior |
| CRM | Identify users who may respond to personalized nudges |
| Ecommerce Analytics | Build a repeatable scoring layer for session-level decision support |
| Operations Planning | Use demand signals to support inventory and replenishment awareness |

---

## Streamlit Decision Tool

A Streamlit app was built to make the scoring system easier to explore.

The app allows users to:

- Load sample session data
- Score sessions by conversion probability
- Estimate expected revenue
- Assign business segments
- Review recommended actions
- Download scored output for further analysis

![Streamlit App Demo](visualizations/streamlit_app_demo.png)

---

## How to Review This Project

You can validate this project through either the scored sample file or the interactive Streamlit app.

### Option 1: Review the scored sample file

Open:

```text
data/processed/scored_sample_sessions.csv
```

Sort by:

```text
expected_revenue
```

Compare top-ranked sessions against bottom-ranked sessions.

Look for:

- Higher conversion concentration in top-ranked sessions
- Revenue concentrated in higher-priority segments
- Clear mapping from model score to recommended business action
- Difference between purchase intent and predicted spend
- Impact of calibration on expected revenue planning

### Option 2: Run the Streamlit app

```bash
python -m streamlit run app/streamlit_app.py
```

The app opens at:

```text
http://localhost:8501
```

Then:

1. Click **Load Sample Data**
2. View session scoring, segmentation, and demand signals
3. Compare expected revenue by segment
4. Download the scored output

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

The dataset is synthetic, but its structure is intended to mirror a workflow that could be adapted to GA4 BigQuery export data after validation.

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

## Input Data Requirement

The Streamlit app expects the same feature set used during model training.

Required features are stored in:

```text
models/feature_names.joblib
```

The included sample file is already formatted correctly:

```text
data/processed/scored_sample_sessions.csv
```

If an uploaded file is missing required columns, the app will stop and show which features are missing.

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
│   ├── 02_deployment_prep.ipynb
│   └── predictive-funnel-analytics-GA4-Stakeholder-Report.ipynb
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

---

## Important Notes

- This project uses a synthetic GA4-style ecommerce dataset
- It is designed as an analytics prototype, not a production-ready system
- This is a ranking and prioritization system
- Measuring incremental lift from interventions would require A/B testing
- Expected revenue should be extended to expected profit before production use

---

## Production Considerations

Before real deployment, this system would require:

- GA4 BigQuery export validation
- Identity stitching across devices
- Event quality validation
- Attribution logic
- Campaign cost integration
- Product margin and discount-cost logic
- Model drift monitoring
- Automated scoring pipeline
- Experimentation framework for measuring incrementality

---

## Final Takeaway

Most junior analytics portfolios stop at charts, notebooks, or model scores.

This project is different because it translates analytics into operational decisions.

Most ecommerce models ask:

> “Will this customer buy?”

This project asks:

> “What is this session worth, and what should the business do about it?”

By combining conversion probability with spend potential, the project turns behavioral data into a practical decision system for revenue prioritization, marketing efficiency, and margin-aware targeting.

**Clicks signal intent. History signals wallet.**
