![Predictive Funnel Analytics Banner](visualizations/header.png)

# Predictive Funnel Analytics (PFA-GA4)

### GA4-Aligned Session Scoring & Revenue Opportunity Framework

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-yellow)
![Status](https://img.shields.io/badge/Project-Completed-green)

**Author:** Troy Dela Rosa  
**Tools:** Python · pandas · NumPy · scikit-learn · XGBoost · SHAP · Matplotlib · Seaborn · Jupyter  
**Focus:** Ecommerce Analytics · Conversion Propensity · Revenue Forecasting · Promotion Targeting



## Executive Summary

This project answers a practical ecommerce question:

> **Which user sessions should we prioritize for marketing intervention without wasting discounts on users who would likely convert anyway?**

Using a two-stage predictive funnel framework, the project scores sessions by:

1. **Conversion probability** — how likely a session is to result in a purchase  
2. **Predicted spend** — how much the user is expected to spend if they convert  
3. **Expected revenue** — the combined business value of the session  

The final model ranked sessions effectively on a held-out test set. Sessions in the top decile converted at approximately **3x the baseline conversion rate**, showing that the model can prioritize higher-intent traffic better than random targeting.

This project was built using a synthetic ecommerce dataset structured similarly to a GA4-style event workflow.


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

The model is strongest as a **ranking and prioritization tool**. Probability calibration improved its usefulness for revenue planning by reducing overconfident conversion estimates.


## Core Idea

> **Expected Revenue = P(Convert) × Predicted Spend**

Instead of optimizing for conversion rate alone, this framework estimates the economic value of each session.

A session with high purchase probability but low spend may be less valuable than a lower-probability session with much higher expected basket value. The hurdle model combines both signals into one decision-ready metric.


## Why This Project Matters

In many ecommerce funnels:

- Most sessions do not convert
- Marketing spend is often applied too broadly
- Discounts may be given to users who would have converted anyway
- High-potential sessions can be missed because they are not ranked by value

This creates avoidable margin pressure and inefficient campaign spend.

This framework helps identify:

- Users likely to convert without an incentive
- Mid-propensity users who may be worth a targeted nudge
- Low-propensity sessions where paid remarketing may be inefficient
- High-value sessions that deserve prioritization


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


## Final Output

For each session, the pipeline produces:

- Conversion probability
- Predicted spend
- Expected revenue
- Business segment
- Recommended action

| Segment | Probability Range | Recommended Action |
|---|---:|---|
| High Certainty | >80% | Protect margin; avoid unnecessary discounts |
| At Risk | 40–70% | Consider targeted incentive or cart recovery |
| Low Interest | <40% | Reduce conversion-focused spend |

Thresholds are heuristic and can be adjusted based on margin, campaign cost, customer lifetime value, and business risk tolerance.


## Example Model Output

| Session ID | P(Convert) | Predicted Spend | Expected Revenue | Segment | Recommended Action |
|---|---:|---:|---:|---|---|
| S-10492 | 0.86 | $124.50 | $107.07 | High Certainty | Avoid discounting; likely to convert naturally |
| S-21984 | 0.58 | $96.20 | $55.80 | At Risk | Send targeted incentive or cart recovery message |
| S-33871 | 0.12 | $42.00 | $5.04 | Low Interest | Suppress paid remarketing or use awareness messaging |

*Illustrative values used to demonstrate the framework.*


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


## Business Interpretation

The model can support ecommerce and retail analytics decisions such as:

- Prioritizing sessions for cart recovery campaigns
- Reducing unnecessary discounts for high-certainty buyers
- Ranking audiences for paid media retargeting
- Identifying mid-funnel users who may respond to incentives
- Supporting merchandising decisions using demand signals
- Improving campaign budget allocation

Important note:

> Propensity models estimate likelihood of conversion, not incremental lift.

In production, this type of model should be paired with A/B testing or uplift modeling to measure whether an intervention actually caused additional conversions.


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


## Leakage Prevention

Because this project uses funnel data, leakage prevention was a major part of the workflow.

The following fields were excluded from the final classification model:

- `event_purchase`
- `purchase_to_cart_ratio`
- Non-time-aware spend aggregates
- Raw event counts that directly reconstructed funnel outcomes
- Target variables such as `is_converted` and `purchase_amount`

An early version of the model produced suspiciously perfect performance, which indicated leakage. After removing leakage-prone features, the final model produced a more realistic test ROC-AUC of approximately 0.80.

> A perfect model score is often a bug, not a breakthrough.


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

The current project should be viewed as an analytics case study and prototype, not a ready-to-deploy production system.


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


## Quick Start

To reproduce this project locally, clone the repository, download the Kaggle dataset, install the required libraries, and run the main notebook.

```bash
git clone https://github.com/rynetroy/Predictive-Funnel-Analytics-GA4.git
cd Predictive-Funnel-Analytics-GA4
pip install -r requirements.txt
```

Download the Marketing & E-Commerce Analytics Dataset from Kaggle and place the CSV files inside the `data/` folder.

Then open and run:

```text
notebooks/PFA_GA4.ipynb
```
