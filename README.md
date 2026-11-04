![Predictive Funnel Analytics Banner](visualizations/header.png)

# Predictive Funnel Analytics for Ecommerce Revenue Prioritization
### A GA4-Aligned Analytics Project for Session Scoring, Revenue Opportunity, and Marketing Decision Support

**Repository:** [Predictive-Funnel-Analytics-GA4](https://github.com/rynetroy/Predictive-Funnel-Analytics-GA4)
**Live Demo:** [Launch the PFA-GA4 Streamlit App](https://rynetroy-predictive-funnel-analytics-ga-appstreamlit-app-dcavuj.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-yellow)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Project-v2.0.0-green)

**Author:** Troy Dela Rosa
**Tools:** Python, pandas, scikit-learn, XGBoost, SHAP, Streamlit
**Dataset:** Synthetic, GA4-structured. See [Data & Scope](#data--scope).

---

## Overview

Most ecommerce models focus on one question:

> **Will this customer buy?**

This project asks a different question:

> **What is this session worth, and what should the business do about it?**

PFA-GA4 uses a two-stage scoring approach:

**Conversion Probability × Predicted Spend = Expected Revenue**

The goal is to rank GA4-style ecommerce sessions by potential value and connect those scores to practical business actions.

The underlying dataset is synthetic. The results in this README demonstrate how the framework works and should not be interpreted as production results. The data structure and scoring approach are designed to map to a real GA4 BigQuery export.

### Results at a Glance

| Metric | Result |
|---|---:|
| Baseline conversion rate | 5.16% |
| Top decile conversion rate | 15.33% |
| Lift, top decile vs. baseline | 3.0x |
| ROC-AUC (conversion model) | 0.80 |
| Spend estimator R² (customer history) | 0.65 |
| Calibrated expected revenue (test set) | $1.97M |
| Actual test-set revenue | $1.74M |
| Revenue variance after calibration | +13.4% |

![Propensity Decile Analysis](visualizations/propensity_decile.png)

---

## Business Context

Ecommerce teams can see how much traffic they receive, but traffic volume alone does not tell them which sessions deserve attention.

Some visitors are already highly likely to purchase. Others show some buying intent but may need additional engagement. Some sessions have very little indication of purchase intent.

The goal of this project is to separate those groups and give marketing, pricing, CRM, and analytics teams a way to prioritize sessions based on **expected revenue**, rather than relying only on traffic volume or conversion probability.

```text
Behavior → Revenue → Business Action
```

---

## Key Insights

### 1. Conversion opportunity is concentrated

The top 10% of ranked sessions converted at 15.33%, compared with a 5.16% overall conversion rate.

That is approximately 3.0x the baseline conversion rate.

This suggests that purchase intent is concentrated within a relatively small portion of sessions. Instead of treating every visitor the same, marketing teams could focus attention on the sessions showing the strongest signals.

**Business takeaway:** prioritize retargeting and other conversion-focused activity toward higher-value sessions instead of spreading resources evenly across all traffic.

### 2. Clicks signal intent, not wallet

A session with a high probability of converting is not necessarily the most valuable session.

For example, a customer with a 70% chance of purchasing a $20 order may be less valuable than a customer with a 50% chance of purchasing a $200 order.

PFA-GA4 combines purchase intent with predicted customer spend:

```text
Expected Revenue = P(Conversion) × Predicted Spend
```

The key finding: in-session behavior predicts **whether** someone buys, but not **how much** they spend. A spend model built on session behavior had an R² of about −0.01 (no better than guessing the average). A customer's historical average spend reached an R² of about 0.65.

This separates two different signals:

- **Session intent:** what the customer is doing right now
- **Customer value:** what the customer has historically spent

**Business takeaway:** ranking sessions by expected revenue can provide a different prioritization than ranking by conversion probability alone.

### 3. The middle of the funnel is the strongest testing opportunity

Sessions with very high purchase probability may not need a discount or additional incentive. Offering a discount to someone who was already likely to buy could simply reduce margin.

At the other end, sessions with very weak signals may not be worth spending additional conversion-focused budget on.

The middle segment is more interesting. These sessions show meaningful intent but are not yet highly committed. They could be candidates for testing actions such as:

- Cart recovery
- Personalized messaging
- Limited-time offers
- Product recommendations
- Retargeting

The model does not claim that these actions will increase conversion. That would require controlled A/B testing.

![Revenue Opportunity](visualizations/revenue_opportunity.png)

### 4. Calibration matters before using model scores for planning

The raw model ranked sessions well, but its probabilities were far too high: summed expected revenue came to about $13.7M against $1.74M actual.

After applying Platt scaling, calibrated expected revenue was $1.97M.

| Revenue Measure | Amount |
|---|---:|
| Expected revenue before calibration | ≈ $13.7M |
| Calibrated expected revenue | $1.97M |
| Actual test revenue | $1.74M |
| Variance after calibration | +$233K (+13.4%) |

Calibration does not change the ranking (ROC-AUC stays at 0.80), but it makes the probabilities usable for revenue planning and prioritization.

---

## Business Segmentation Framework

| Segment | Meaning | Recommended Action | Primary Stakeholder |
|---|---|---|---|
| High Certainty | Strong likelihood to convert | Protect margin and avoid unnecessary discounts | Marketing, Pricing |
| At-Risk | Moderate intent and strongest testing opportunity | Test selective incentives or recovery messaging | Marketing, CRM |
| Monitor | Some signal but not yet actionable | Wait for stronger behavioral signals | Digital Analytics |
| Low Interest | Weak intent and low wallet potential | Reduce conversion-focused ad spend | Paid Media, Growth |

<!-- [CONFIRM] The stakeholder report uses 3 segments (>80%, 40-70%, <40%), which leaves 70-80% unassigned, and this README uses 4. Check which version the Streamlit app uses, whether thresholds apply to calibrated or raw scores, and make the report, app and README match. -->

---

## How It Works

### Stage 1: Conversion Propensity

An XGBoost classifier predicts the probability that a session will result in a purchase.

The model uses three feature families that passed the leakage audit:

- **Behavioral (in-session):** session duration, event velocity, cart-to-view ratio, click-to-view ratio
- **Customer:** age, loyalty tier, acquisition channel, device type
- **Campaign:** channel, objective, expected uplift

XGBoost was compared with Logistic Regression and Random Forest (balanced). It achieved a test-set ROC-AUC of 0.80 and showed stronger decile ranking performance.

### Stage 2: Spend Estimation

The second stage estimates how much a session is likely to spend if it converts, using a customer-level lookup:

```text
models/customer_spend_lookup.csv
```

The lookup holds each customer's historical average spend, calculated only from purchases made **before** the session started. Customers with no purchase history fall back to the overall average.

| Spend approach | R² | MAE |
|---|---:|---:|
| In-session behavior | ≈ −0.01 | n/a |
| Customer historical average | ≈ 0.65 | ≈ $28.57 |

### Stage 3: Scoring and Segmentation

The two stages are combined to calculate expected revenue:

```text
Expected Revenue = P(Conversion) × Predicted Spend
```

Sessions are then ranked and assigned to one of four business segments based on conversion likelihood and potential customer value.

*A direct comparison between expected-revenue ranking and conversion-probability ranking is an important next validation step. This will help determine how much additional ranking value the spend-estimation stage provides.*

---

## Model Validation

The project includes several validation steps:

- 60/20/20 train, validation, and test split, performed before any encoding or imputation
- Leakage audit: an initial ROC-AUC of 1.00 flagged leaking features; four rounds of removal brought it to 0.80
- Imputers and encoders fit on the training split only
- Time-aware spend history (only purchases before each session)
- Model comparison between Logistic Regression, Random Forest, and XGBoost
- Probability calibration using Platt scaling
- Decile lift analysis
- SHAP explainability
- Revenue reconciliation against the actual test set
- Planned comparison of expected-revenue ranking versus conversion-probability ranking

---

## Design Decisions

Each choice below is one I'd expect to be asked about, so here is the reasoning behind it.

**Rank by expected revenue, not conversion probability alone.**
Probability answers "who will buy?" Expected revenue answers "which session is worth acting on?", which is the question a marketing team actually has. Whether this ranking beats probability alone on this data has not been tested yet; that comparison is the next validation step listed above.

**Two stages, because revenue is mostly zeros.**
About 95% of sessions generate no revenue, and a few generate a lot. Modeling revenue directly blends two different questions, so the model answers them separately: will this session convert (Stage 1), and if it does, how much (Stage 2). This is known as a hurdle model.

**Judged on ROC-AUC and decile lift, not accuracy.**
Only 5.16% of test sessions converted. A model that predicts "no purchase" for everyone would be about 95% accurate and useless. ROC-AUC measures how well the model ranks buyers above non-buyers, and decile lift shows whether the top of the ranking really converts more.

**XGBoost over Logistic Regression and Random Forest.**
All three were compared. XGBoost was selected because it showed the strongest decile ranking and the highest ROC-AUC. Logistic Regression stayed useful as a simple baseline to confirm the extra complexity was worth it.
<!-- [CONFIRM] Add each model's ROC-AUC from 01_modeling_pfa_ga4.ipynb, e.g. "LogReg 0.XX, RF 0.XX, XGBoost 0.80", or delete this comment. -->

**Leakage checks before trusting any score.**
The first model scored a ROC-AUC of 1.00, which was the signal that features were leaking the answer. Four rounds of feature removal brought it to a realistic 0.80. Purchase-event counts are never used as features, the 60/20/20 split happens before any encoding, and imputers and encoders are fit on the training split only.

**Spend from customer history, not session behavior.**
In-session behavior did not predict basket size at all (R² ≈ −0.01). A customer's historical average spend did much better (R² ≈ 0.65, MAE ≈ $28.57). History is built with `merge_asof` so it only counts purchases made strictly before the session starts, which keeps the spend estimate from seeing the outcome.

**Calibrate probabilities with Platt scaling.**
Before calibration, summed expected revenue was about $13.7M against $1.74M actual: fine for ranking, misleading for planning. Platt scaling, fit on the validation set, brought it to $1.97M (+13.4%). That is close enough for prioritization, not for a budget forecast.

**Four action segments instead of one cutoff.**
A single "buy / won't buy" threshold hides the most useful group: mid-propensity sessions that show intent but may still need a nudge. Four segments give each team a clear action, including the one most models miss: not discounting customers who would buy anyway.

**Stop at expected revenue, not expected profit.**
The dataset has no margin, shipping or discount cost, so profit can't be estimated honestly. That is the first change before real use, along with an A/B test, because the model shows where action may pay off but does not prove the action causes extra sales.

**Synthetic data with a GA4 structure.**
A synthetic dataset shaped like GA4 event data means the workflow (events to sessions to scores) could later be pointed at a real GA4 BigQuery export. The results show the method works on this data; they are not evidence about any real store.

---

## Data & Scope

The dataset is synthetic and structured to resemble a GA4 BigQuery export (100K customers, 2M+ events).

The intended data flow is:

```text
Event Logs
    ↓
Session Aggregation
    ↓
User / Session Keys
    ↓
Attribution Metrics
    ↓
Transaction Value
    ↓
Predictive Scoring
```

This project is a ranking and prioritization prototype. It demonstrates how a scoring framework could work with GA4-style ecommerce data, but it has not been validated against a real GA4 BigQuery export.

There are also several important limitations:

- The dataset is synthetic
- The model ranks sessions but does not prove causal impact
- Recommended interventions require A/B testing to measure incremental lift
- Expected revenue is not the same as expected profit
- Margin, shipping costs, and discount costs are not currently included
- Customers with no purchase history fall back to the overall average spend
- Calibration was fit once and will drift as traffic changes

### Before Production Use

A production implementation would need:

- Validation against native GA4 BigQuery event tables
- Cross-device identity resolution
- Event quality checks
- Attribution rules
- Product margin and discount-cost integration
- Automated scoring and monitoring
- Model drift and calibration monitoring
- An experimentation framework to measure incremental lift

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

## Try It Yourself

### Option 1: Review the Scored Sample

Open:

```text
data/processed/scored_sample_sessions.csv
```

Sort the data by `expected_revenue` and compare the highest- and lowest-ranked sessions.

Look for:

- Conversion probability differences
- Predicted spend differences
- Expected revenue differences
- Conversion concentration among highly ranked sessions

### Option 2: Run the Streamlit App

```bash
git clone https://github.com/rynetroy/Predictive-Funnel-Analytics-GA4.git
cd Predictive-Funnel-Analytics-GA4
pip install -r requirements.txt
python -m streamlit run app/streamlit_app.py
```

The app will open at:

```text
http://localhost:8501
```

Load the sample data, review session scoring and segmentation, and download the scored output.

The app expects the feature set listed in:

```text
models/feature_names.joblib
```

The included sample CSV is already formatted correctly. If you upload your own data, the app will flag any missing required columns.

---

## Stakeholder Use Cases

| Stakeholder | How This Helps |
|---|---|
| Marketing | Prioritize retargeting and cart-recovery audiences by expected value |
| Pricing | Suppress promotional discounts on high-certainty traffic to protect margin |
| Merchandising | Surface category demand signals from session behavior |
| CRM | Identify segments for personalized lifecycle messaging |
| Ecommerce Analytics | Provide a repeatable scoring layer for session-level decisions |
| Operations Planning | Provide demand signals that can complement inventory and replenishment planning |

---

## From Score to Decision

PFA-GA4 connects the model to a business decision:

```text
Probability × Spend
        ↓
Expected Revenue
        ↓
Session Ranking
        ↓
Business Segment
        ↓
Recommended Action
```

The goal is not simply to predict who might buy.

It is to help answer:

> Where should the business focus its attention, and why?

**Clicks signal intent. History signals wallet.**
