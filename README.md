![Predictive Funnel Analytics Banner](visualizations/header.png)

# Predictive Funnel Analytics for Ecommerce Revenue Prioritization
### A GA4-Aligned Analytics Project for Session Scoring, Revenue Opportunity, and Marketing Decision Support

**Repository:** [Predictive-Funnel-Analytics-GA4](https://github.com/rynetroy/Predictive-Funnel-Analytics-GA4)
**Live Demo:** [Launch the PFA-GA4 Streamlit App](https://rynetroy-predictive-funnel-analytics-ga-appstreamlit-app-dcavuj.streamlit.app/)

**Non-technical overview:** [Business Summary](BUSINESS_SUMMARY.md)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-yellow)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Project-v2.1-green)

**Author:** Troy Dela Rosa
**Tools:** Python, pandas, scikit-learn, XGBoost, SHAP, Streamlit
**Dataset:** Synthetic, GA4-structured ([Marketing & E-Commerce Analytics Dataset](data/README.md)). See [Data & Scope](#data--scope).

> **Which notebook is the source of record?** Revenue, calibration and segment figures come from the capstone notebook, [`delarosa_troy_SML_model_deployment.ipynb`](notebooks/delarosa_troy_SML_model_deployment.ipynb). A Nov 2026 self-audit of the portfolio notebook (`01_modeling_pfa_ga4.ipynb`) found that its customer-history spend lookup included the purchase being predicted and that its revenue reconciliation matched predictions to the wrong rows, so its revenue cells are not used here. The conversion model and ranking results are the same in both notebooks.

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
| Sessions modeled | ~2.0M |
| Baseline conversion rate | 5.16% |
| Top decile conversion rate | 15.33% |
| Lift, top decile vs. baseline | 3.0x |
| ROC-AUC (conversion model, test set) | 0.80 |
| Top 20% of sessions, share of revenue | ~55% |
| Brier score, before → after calibration | 0.130 → 0.046 |
| Calibrated expected revenue vs. actual (test set) | $1.98M vs $1.74M (+13.6%) |
| Spend from session behavior (R²) | ≈ 0 |

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

That is approximately 3.0x the baseline conversion rate. The bottom three deciles converted at close to 0%.

This suggests that purchase intent is concentrated within a relatively small portion of sessions. Instead of treating every visitor the same, marketing teams could focus attention on the sessions showing the strongest signals.

**Business takeaway:** prioritize retargeting and other conversion-focused activity toward higher-ranked sessions instead of spreading resources evenly across all traffic.

### 2. The algorithm didn't matter; the features did

Four classifiers were compared and all landed at the same ROC-AUC on the validation set:

| Model | ROC-AUC |
|---|---:|
| Random Forest | 0.8015 |
| XGBoost | 0.8015 |
| Logistic Regression | 0.8011 |
| Random Forest (balanced) | 0.7955 |

Hyperparameter tuning moved none of them by more than 0.01. The signal is in the features (campaign expected uplift, click-to-view ratio and cart-to-view ratio were the strongest), not in the choice of algorithm.

![Classification Model Comparison](visualizations/classification_leaderboard.png)

### 3. Clicks signal intent, not wallet

A session with a high probability of converting is not necessarily the most valuable session.

For example, a customer with a 70% chance of purchasing a $20 order may be less valuable than a customer with a 50% chance of purchasing a $200 order.

PFA-GA4 combines purchase intent with predicted customer spend:

```text
Expected Revenue = P(Conversion) × Predicted Spend
```

The key finding: in-session behavior predicts **whether** someone buys, but not **how much** they spend. Spend models built on session behavior (Ridge and XGBoost) had an R² of about −0.01, no better than guessing the average basket. Spend is therefore estimated from customer purchase history instead (see Stage 2).

This separates two different signals:

- **Session intent:** what the customer is doing right now
- **Customer value:** what the customer has spent before

### 4. The middle of the funnel is the strongest testing opportunity

Sessions with very high purchase probability may not need a discount or additional incentive. Offering a discount to someone who was already likely to buy could simply reduce margin.

At the other end, sessions with very weak signals may not be worth spending additional conversion-focused budget on.

The middle segment is more interesting. These sessions show meaningful intent but are not yet highly committed. They could be candidates for testing actions such as:

- Cart recovery
- Personalized messaging
- Limited-time offers
- Product recommendations
- Retargeting

The model does not claim that these actions will increase conversion. That would require controlled A/B testing.

### 5. Ranking well is not the same as forecasting well

The raw XGBoost scores ranked sessions well, but they were not usable as probabilities: they averaged 35.9% against a 5.16% actual conversion rate, which would overstate any revenue plan by several times.

Platt scaling, fit on the validation set, rescales the scores into probabilities without changing the ranking (ROC-AUC stays at 0.80). On the test set:

| Measure | Before calibration | After Platt scaling |
|---|---:|---:|
| Mean predicted conversion | 35.9% | 5.14% (actual 5.16%) |
| Brier score (lower is better) | 0.130 | 0.046 |
| Expected revenue vs. $1.74M actual | ≈ $13.7M | $1.98M (+13.6%) |

A naive model that predicts the base rate for everyone scores a Brier of 0.049, so the raw scores were worse than guessing and the calibrated scores are better. The remaining 13.6% overshoot comes from the spend side: the spend estimate predicts close to the average basket, and the training average sits slightly above the test average.

---

## Business Segmentation Framework

Sessions are grouped by their decile on calibrated scores (D10 = highest). The cut points are a business choice, not a model output.

| Segment | Deciles | Share of sessions | Actual conversion | Share of revenue | Recommended Action | Primary Stakeholder |
|---|---|---:|---:|---:|---|---|
| High Certainty (Protect) | D10 | 10% | 15.4% | ~30% | Protect margin and avoid unnecessary discounts | Marketing, Pricing |
| At-Risk (Nudge) | D7 to D9 | 30% | 6% to 13% | ~56% | Test selective incentives or recovery messaging | Marketing, CRM |
| Monitor | D4 to D6 | 27% | 2% to 4% | ~14% | Wait for stronger behavioral signals | Digital Analytics |
| Low Interest (Brand only) | D1 to D3 | 33% | 0% | 0% | Reduce conversion-focused ad spend | Paid Media, Growth |

*Test set, capstone notebook section 7.4. Revenue by decile is estimated as conversions × the average actual basket. Decile sizes are uneven because many sessions share the same lowest score. The Streamlit demo still uses the earlier fixed-probability thresholds and will be updated to match.*

---

## How It Works

### Stage 1: Conversion Propensity

An XGBoost classifier predicts the probability that a session will result in a purchase.

The model uses 25 features (11 before one-hot encoding) from three families that passed the leakage audit:

- **Behavioral (in-session):** session duration, event velocity, cart-to-view ratio, click-to-view ratio
- **Customer:** age, loyalty tier, acquisition channel, device type
- **Campaign:** channel, objective, expected uplift

### Stage 2: Spend Estimation

The second stage estimates how much a session is likely to spend if it converts. Two approaches were tested:

| Spend approach | R² | Status |
|---|---:|---|
| Session behavior (Linear Regression, Decision Tree, Ridge, XGBoost) | ≈ 0 | Used for the revenue figures (capstone notebook) |
| Customer historical average | Being corrected | An earlier version scored R² 0.65, but its average included the purchase being predicted |

Because session behavior predicts spend no better than the average basket, the $1.98M figure is effectively calibrated probability × an average basket. A leak-free customer-history estimate (only purchases made before each session) is the planned improvement.

The exported lookup (`models/customer_spend_lookup.csv`) averages all of a customer's past purchases. That is appropriate for scoring new sessions; it is only a problem when used to evaluate past sessions.

### Stage 3: Scoring and Segmentation

The two stages are combined to calculate expected revenue:

```text
Expected Revenue = P(Conversion) × Predicted Spend
```

Sessions are then ranked and assigned to one of four business segments.

*A direct comparison between expected-revenue ranking and conversion-probability ranking is an important next validation step. This will help determine how much additional ranking value the spend-estimation stage provides.*

---

## Model Validation

- 60/20/20 train, validation, and test split, stratified on conversion and performed before any encoding or imputation
- Leakage audit: an early model scored ROC-AUC 1.00; four rounds of feature removal brought it to 0.80
- Imputers and encoders fit on the training split only
- Model comparison: Logistic Regression, Random Forest (with and without class balancing), and XGBoost
- Manual hyperparameter tuning for XGBoost and Random Forest
- Probability calibration with Platt scaling, fit on validation and evaluated on test (Brier score and reliability diagram)
- Revenue reconciliation: expected vs. actual revenue in total and by decile
- Decile lift analysis and SHAP explainability, including a review of missed buyers (false negatives)
- Self-audit (Nov 2026): found spend-lookup leakage and a row-alignment error in the portfolio notebook's revenue cells; revenue figures now come from the capstone notebook
- Planned: compare expected-revenue ranking against conversion-probability ranking

---

## Design Decisions

Each choice below is one I'd expect to be asked about, so here is the reasoning behind it.

**Rank by expected revenue, not conversion probability alone.**
Probability answers "who will buy?" Expected revenue answers "which session is worth acting on?", which is the question a marketing team actually has. Whether this ranking beats probability alone on this data has not been tested yet; that comparison is the next validation step.

**Two stages, because revenue is mostly zeros.**
About 95% of sessions generate no revenue, and a few generate a lot. Modeling revenue directly blends two different questions, so the model answers them separately: will this session convert (Stage 1), and if it does, how much (Stage 2). This is known as a hurdle model.

**Judged on ROC-AUC and decile lift, not accuracy.**
Only 5.16% of test sessions converted. A model that predicts "no purchase" for everyone would be about 95% accurate and useless. The baseline Random Forest did exactly that at the default threshold: 95% accuracy, zero buyers found. ROC-AUC measures how well the model ranks buyers above non-buyers, and decile lift shows whether the top of the ranking really converts more.

**XGBoost kept, but not because it won.**
All four classifiers scored about 0.80. XGBoost was kept for the pipeline, but Logistic Regression would have done the same job and is easier to explain to a business audience.

**Leakage checks before trusting any score.**
The first model scored a ROC-AUC of 1.00, which was the signal that features were leaking the answer. Four rounds of removal followed: the purchase event itself, all-time spend aggregates, time-gated spend history, and raw event counts, which reconstructed the funnel in this synthetic dataset. That brought the model to a realistic 0.80. One remaining check: event velocity was calculated from all session events, including the purchase. It is not a top feature, but it will be recalculated without purchase events and the ROC-AUC reported either way.

**Spend from customer history, not session behavior.**
In-session behavior did not predict basket size at all (R² ≈ 0), so the better source of spend is what a customer has spent before. The first version of a history lookup averaged every purchase, including the one being predicted, which made it look far more accurate (R² 0.65) than it can be. The published revenue figures use the session-based estimate instead; a leak-free history lookup is the next step.

**Calibrate before planning with the scores.**
Raw scores averaged 35.9% against 5.16% actual: fine for ranking, misleading for any revenue plan. Platt scaling, fit on the validation set, brought the mean to 5.14% and the Brier score from 0.130 to 0.046, without changing the ranking.

**Segments by rank, not fixed probability cut-offs.**
After calibration, the highest-scoring sessions sit around 17%, so fixed thresholds like "40 to 70%" would leave every segment empty. Grouping sessions by decile keeps every segment usable, and the cut points can be moved to match a team's capacity or budget.

**Stop at expected revenue, not expected profit.**
The dataset has no margin, shipping or discount cost, so profit can't be estimated honestly. That is the first change before real use, along with an A/B test, because the model shows where action may pay off but does not prove the action causes extra sales.

**Synthetic data with a GA4 structure.**
A synthetic dataset shaped like GA4 event data means the workflow (events to sessions to scores) could later be pointed at a real GA4 BigQuery export. The results show the method works on this data; they are not evidence about any real store.

---

## Data & Scope

The dataset is the synthetic Marketing & E-Commerce Analytics Dataset (Kaggle), structured to resemble a GA4 BigQuery export: 100K customers, 2M+ events, about 2.0M sessions across five tables (customers, events, transactions, products, campaigns). The raw files are not included because of size; see [`data/README.md`](data/README.md). Profiling reports for each table are in [`reports/`](reports/).

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

Limitations:

- The dataset is synthetic
- The model ranks sessions but does not prove causal impact
- Recommended interventions require A/B testing to measure incremental lift
- Expected revenue is not the same as expected profit
- Margin, shipping costs, and discount costs are not currently included
- Spend is estimated close to the average basket, which causes the +13.6% revenue overshoot
- Calibration was fit once and will drift as traffic changes
- Event velocity currently includes purchase events (fix in progress)

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
│   ├── feature_names.csv
│   └── customer_spend_lookup.csv
│
├── data/
│   ├── README.md                      (how to download the raw dataset)
│   └── processed/
│       └── scored_sample_sessions.csv
│
├── notebooks/
│   ├── data-audit.ipynb               (ydata-profiling of the raw tables)
│   ├── delarosa_troy_SML_model_deployment.ipynb   (capstone notebook: source of revenue and calibration figures)
│   ├── 01_modeling_pfa_ga4.ipynb      (portfolio notebook: modeling, leakage audit, SHAP)
│   └── predictive-funnel-analytics-GA4-Stakeholder-Report.ipynb
│
├── reports/                           (profiling reports per table)
│
├── visualizations/
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

Sort the data by `conversion_probability` and compare the highest- and lowest-ranked sessions.

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
