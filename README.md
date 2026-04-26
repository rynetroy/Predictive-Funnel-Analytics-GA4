![Predictive Funnel Analytics Banner](visualizations/header.png)

# Predictive Funnel Analytics (PFA-GA4)

### GA4 Aligned Session Scoring & Revenue Opportunity Framework

**Author:** Troy Dela Rosa  
**Tools:** Python · pandas · NumPy · scikit-learn · XGBoost · Matplotlib · Seaborn · Jupyter  
**Focus:** Ecommerce Analytics · Conversion Propensity · Revenue Forecasting

---

## Executive Summary

This project answers a core ecommerce question:

> **Which user sessions should we prioritize to maximize expected revenue without eroding margin?**

Using a two stage modeling framework, sessions are scored by conversion likelihood and expected spend, enabling targeted promotion, bidding, and merchandising decisions.

**Key outcome:**  
High scoring sessions in the top decile convert at approximately **3x the baseline rate**, enabling more efficient prioritization of revenue generating traffic.

---

## Key Results Snapshot

- **ROC-AUC:** 0.80 on held-out test set
- **Top-decile lift:** 3x base conversion rate
- **Revenue forecast:** $1.97M expected vs $1.74M actual after calibration
- **Overestimation bias:** +13.4% post-calibration
- **Primary use cases:** promotion targeting, paid media bidding, merchandising prioritization

---

## What This Project Does

This project builds a two stage session scoring system that assigns:

- Probability of conversion
- Expected revenue value per session

This enables:

- Identification of high value users before purchase
- Targeted intervention on potentially recoverable mid propensity sessions
- Smarter allocation of marketing spend
- Revenue based prioritization with margin aware decisioning

The notebook includes full model diagnostics, calibration analysis, feature importance, and implementation details.

---

## Key Idea

> **Expected Revenue = P(Convert) x Expected Spend**

Rather than optimizing for conversion rate alone, this framework estimates economic value per session.

---

## Why It Matters

In most ecommerce funnels:

- The majority of sessions do not convert
- Marketing spend is often applied uniformly

This leads to:

- Missed high intent opportunities
- Overspending on low value traffic

This framework identifies:

- **Who is likely to convert**
- **Who is potentially persuadable with intervention**
- **Who is unlikely to justify spend**

---

## Approach

### Stage 1: Conversion Propensity

- **Model:** XGBoost Classifier
- **Output:** Probability of purchase
- **Performance:** ROC-AUC 0.80 with strong ranking lift

### Stage 2: Spend Estimation

- **Method:** Baseline historical AOV lookup
- **Design choice:** Intentionally simple to isolate propensity signal and allow modular extension to regression based spend models
- **Insight:** Behaviour predicts intent more reliably than spend magnitude

### Final Output

- Session level expected revenue
- Actionable segmentation for marketing and pricing decisions

---

## Revenue Reconciliation

After probability calibration, the model produced the following held-out estimate:

| Metric | Value |
|---|---:|
| Expected revenue (calibrated) | $1,972,962.80 |
| Actual revenue | $1,739,605.48 |
| Overestimation | +$233,357.32 |
| Overestimation (%) | +13.4% |

Calibration reduced overconfidence in predicted probabilities while preserving ranking performance. Revenue outputs should be interpreted as planning estimates, not guaranteed outcomes.

---

## Business Interpretation

- Useful for relative ranking and resource allocation decisions
- Most effective when used to prioritize mid propensity sessions
- Enables more efficient promotion targeting and budget allocation
- Spend model can be upgraded independently without retraining the full system

> **Important:** Propensity scores estimate likelihood of purchase, not incremental treatment effect. In production, A/B testing or uplift modeling should be used to measure true intervention impact.

---

## Example Model Output (Illustrative)

| Session ID | P(Convert) | Expected Spend | Expected Revenue | Segment | Recommended Action |
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
| **Low Interest** | <40% | Reduce spend / suppress remarketing |

*Thresholds are heuristic and can be tuned based on margin sensitivity, campaign cost, and business constraints.*

---

## Data Structure

The dataset consists of five relational tables:

- `customers`: one row per user
- `events`: one row per interaction, such as clicks or views
- `transactions`: one row per completed purchase
- `products`: one row per product with metadata
- `campaigns`: marketing campaign attributes

Sessions were constructed by aggregating event level data into session level features aligned with GA4 style sessionization logic.

---

## GA4 Alignment

This project was designed to approximate a Google Analytics 4 BigQuery export workflow.

| Project Field | Comparable GA4 Field |
|---|---|
| `events.csv` | `events_*` tables |
| `event_type` | `event_name` |
| `customer_id` | `user_pseudo_id` |
| `session_id` | `ga_session_id` |
| `purchase_amount` | `ecommerce.purchase_revenue` |

While not run on a live GA4 property, the workflow was designed for transferability after validating:

- Event quality
- Session logic
- Identity stitching
- Revenue attribution
- Leakage safeguards

---

## Production Considerations

In live GA4 data, additional validation would be required for:

- Session fragmentation from timeouts, campaign resets, and cross device behavior
- Event duplication and deduplication logic
- Attribution windows and revenue crediting
- Identity stitching across devices and identifiers

---

## Dataset

**Source:** Marketing & E-Commerce Analytics Dataset from Kaggle

- 100,000 customers
- 2M+ interaction events
- 5 relational tables

**Note:** This is a synthetic dataset and does not reflect all real world tracking noise, such as missing events, attribution ambiguity, or inconsistent identity stitching. Results may differ in production environments.

---

## Core Insight

> **Clicks signal intent, not wallet.**

Session behaviour predicts **whether** a user will buy.  
Customer history predicts **how much** they will spend.

Separating these signals improves targeting efficiency, pricing strategy, and marketing ROI.

---

## Project Origin

This project originated from coursework in the Data Science & Machine Learning program at Red River College Polytechnic and was expanded into a business focused analytics case study.
