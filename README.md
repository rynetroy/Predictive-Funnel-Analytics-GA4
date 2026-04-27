![Predictive Funnel Analytics Banner](visualizations/header.png)

# Predictive Funnel Analytics (PFA-GA4)

### GA4-Aligned Session Scoring & Revenue Opportunity Framework

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange) ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-yellow) ![Status](https://img.shields.io/badge/Project-Completed-green)

**Author:** Troy Dela Rosa  
**Tools:** Python · pandas · NumPy · scikit-learn · XGBoost · SHAP · Matplotlib · Seaborn · Jupyter  
**Focus:** Ecommerce Analytics · Conversion Propensity · Revenue Forecasting

---

## Executive Summary

This project answers a core ecommerce question:

> **Which user sessions should we prioritize to maximize expected revenue while reducing unnecessary discounting?**

Using a two-stage modeling framework, sessions are scored by conversion likelihood and predicted spend, enabling more targeted promotion, bidding, and merchandising decisions.

**Key outcome:**  
High-scoring sessions in the top decile converted at approximately **3x the baseline rate**, showing that the model can rank revenue-generating traffic more effectively than random targeting.

Evaluation was performed on a held-out test split of simulated ecommerce sessions.

---

## Key Results Snapshot

- **Test ROC-AUC:** 0.8014
- **Top-decile lift:** 3.0x base conversion rate
- **Calibrated revenue forecast:** $1.97M expected vs $1.74M actual
- **Overestimation bias:** +13.4% after calibration
- **Calibration impact:** Average predicted conversion corrected from 35.91% before calibration to 5.14% after calibration, closely matching the actual 5.16% test conversion rate
- **At-risk opportunity:** 102.9K sessions representing approximately $5.4M in expected revenue
- **Primary use cases:** promotion targeting, paid media bidding, merchandising prioritization

---

## What This Project Does

This project builds a two-stage session scoring system that assigns:

- Probability of conversion
- Predicted spend if the session converts
- Expected revenue value per session

This enables:

- Identification of high-value users before purchase
- Targeted intervention on potentially recoverable mid-propensity sessions
- Smarter allocation of marketing spend
- Revenue-based prioritization with discount-aware decisioning

The notebook includes full model diagnostics, calibration analysis, SHAP explainability, feature importance, pipeline integrity checks, and implementation details.

---

## Key Idea

> **Expected Revenue = P(Convert) × Predicted Spend**

Rather than optimizing for conversion rate alone, this framework estimates economic value per session.

---

## Why It Matters

In most ecommerce funnels:

- The majority of sessions do not convert
- Marketing spend is often applied uniformly
- Discounts may be given to users who would have converted anyway

This leads to:

- Missed high-intent opportunities
- Overspending on low-value traffic
- Unnecessary margin pressure from poorly targeted promotions

This framework identifies:

- **Who is likely to convert**
- **Who is potentially persuadable with intervention**
- **Who is unlikely to justify spend**
- **Who should not receive unnecessary discounts**

---

## Approach

### Stage 1: Conversion Propensity

- **Model:** XGBoost Classifier
- **Output:** Probability of purchase
- **Performance:** Test ROC-AUC of 0.8014 with 3.0x top-decile lift
- **Selection rationale:** XGBoost provided strong ranking performance, high buyer recall, and SHAP explainability while performing similarly to the strongest baseline models.

### Stage 2: Spend Estimation

- **Method:** Customer-level historical average spend lookup
- **Design choice:** Session behavior was useful for predicting conversion intent, but customer purchase history was much stronger for estimating spend magnitude.
- **Insight:** Behaviour predicts intent more reliably than spend amount.

### Final Output

- Session-level conversion probability
- Predicted spend estimate
- Calibrated expected revenue
- Actionable segmentation for marketing, pricing, and merchandising decisions

---

## Revenue Reconciliation

After probability calibration using Platt scaling, the model produced the following held-out estimate:

| Metric | Value |
|---|---:|
| Expected revenue calibrated | $1,972,962.80 |
| Actual revenue | $1,739,605.48 |
| Overestimation | +$233,357.32 |
| Overestimation bias (%) | +13.4% |

Calibration reduced overconfidence in predicted probabilities while preserving ranking performance. Revenue outputs should be interpreted as planning estimates, not guaranteed outcomes.

---

## Business Interpretation

- Useful for ranking sessions and allocating marketing resources under budget constraints
- Most effective when used to prioritize mid-propensity sessions
- Helps avoid unnecessary discounts for high-certainty buyers
- Enables more efficient promotion targeting and budget allocation
- Spend estimation can be upgraded independently without retraining the full classification system
- Best used as a prioritization layer within a broader experimentation framework rather than a standalone decision engine

> **Important:** Propensity scores estimate likelihood of purchase, not incremental treatment effect. In production, A/B testing or uplift modeling should be used to measure true intervention impact.

---

## Example Model Output Illustrative

| Session ID | P(Convert) | Predicted Spend | Expected Revenue | Segment | Recommended Action |
|---|---:|---:|---:|---|---|
| S-10492 | 0.86 | $124.50 | $107.07 | High Certainty | Avoid discounting; likely to convert anyway |
| S-21984 | 0.58 | $96.20 | $55.80 | At Risk | Apply targeted incentive, such as 10 to 15% discount or free shipping |
| S-33871 | 0.12 | $42.00 | $5.04 | Low Interest | Suppress paid remarketing to reduce wasted spend |

*Illustrative values used to demonstrate the framework.*

---

## Segmentation Logic

| Segment | Probability | Recommended Action |
|---|---|---|
| **High Certainty** | >80% | Protect margin / avoid unnecessary incentives |
| **At Risk** | 40 to 70% | Apply targeted incentives to recover demand |
| **Low Interest** | <40% | Reduce spend / suppress conversion-focused remarketing |

*Thresholds are heuristic and can be tuned based on margin sensitivity, campaign cost, and business constraints.*

---

## Business Value Analysis

On the held-out test set, the final scoring pipeline produced the following segment-level opportunity view:

| Segment | Sessions | Expected Revenue | Actual Conversion Rate |
|---|---:|---:|---:|
| High Certainty >80% | 2,824 | $221,547.41 | 16.8% |
| At Risk 40 to 70% | 102,930 | $5,402,214.51 | 6.7% |
| Low Interest <40% | 211,972 | $2,297,951.58 | 0.9% |

The **at-risk segment** represents the largest actionable opportunity because these users show moderate purchase intent but may still need a targeted nudge to convert.

---

## Targeting Lift

The model was evaluated against random targeting on the held-out test set.

| Metric | Value |
|---|---:|
| Base conversion rate | 5.16% |
| Random 10% targeting conversion rate | 5.13% |
| Model top 10% targeting conversion rate | 15.33% |
| Lift over baseline | 3.0x |
| Expected revenue, model top 10% | $2,953,630.04 |
| Expected revenue, random 10% | $1,381,257.44 |
| Revenue lift from model | $1,572,372.60 |

This shows that the model is strongest as a **ranking and prioritization tool**.

---

## Data Structure

The dataset consists of five relational tables:

- `customers`: one row per user
- `events`: one row per interaction, such as clicks or views
- `transactions`: one row per completed purchase
- `products`: one row per product with metadata
- `campaigns`: marketing campaign attributes

Sessions were constructed by aggregating event-level data into session-level features aligned with GA4-style sessionization logic.

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

While not run on a live GA4 property, the workflow was designed for transferability after validating:

- Event quality
- Session logic
- Identity stitching
- Revenue attribution
- Leakage safeguards

---

## Leakage Prevention

Because this project uses funnel data, leakage prevention was a major part of the modeling process.

The following fields were excluded from the final model:

- `event_purchase`
- `purchase_to_cart_ratio`
- Non-time-aware spend aggregates
- Raw funnel event counts that directly reconstructed conversion behavior
- Target variables such as `is_converted` and `purchase_amount`

The final model avoided suspiciously perfect performance and produced a realistic test ROC-AUC of approximately 0.80.

> A key lesson from this project: **a perfect model score is often a bug, not a breakthrough.**

---

## Model Validation

The final notebook includes:

- Train / validation / test split
- Feature leakage audit
- Column alignment checks
- Numeric feature validation
- Classification metrics
- Regression comparison
- Propensity decile analysis
- SHAP explainability
- Revenue reconciliation
- Probability calibration using Platt scaling
- Saved production artifacts

---

## Production Considerations

In live GA4 data, additional validation would be required for:

- Session fragmentation from timeouts, campaign resets, and cross-device behavior
- Event duplication and deduplication logic
- Attribution windows and revenue crediting
- Identity stitching across devices and identifiers
- Product-level margin and discount-cost modeling
- Incrementality testing through A/B tests or uplift modeling
- Model drift monitoring after deployment

---

## Dataset

**Source:** Marketing & E-Commerce Analytics Dataset from Kaggle

- 100,000 customers
- 2M+ interaction events
- 5 relational tables

**Note:** This is a synthetic dataset and does not reflect all real-world tracking noise, such as missing events, attribution ambiguity, or inconsistent identity stitching. The raw dataset is too large to store directly in this repository, so it must be downloaded separately and placed in the local `data/` folder to reproduce the notebook.

---

## Core Insight

> **Clicks signal intent, not wallet.**

Session behaviour predicts **whether** a user will buy.  
Customer history predicts **how much** they will spend.

Separating these signals improves targeting efficiency, pricing strategy, and marketing ROI.

---

## Project Origin

This project originated from coursework in the Data Science & Machine Learning program at Red River College Polytechnic and was expanded into a business-focused analytics case study.
