![Predictive Funnel Analytics Banner](visualizations/header.png)

# Predictive Funnel Analytics (PFA-GA4)

### GA4-Aligned Session Scoring & Revenue Opportunity Framework

**Author:** Troy Dela Rosa  
**Tools:** Python · pandas · NumPy · scikit-learn · XGBoost · Matplotlib · Seaborn · Jupyter  
**Focus:** Ecommerce Analytics · Conversion Propensity · Revenue Forecasting

---

## Key Results Snapshot

- **ROC-AUC:** ~0.80 on held-out test set  
- **Top-decile lift:** ~3× base conversion rate  
- **Revenue forecast:** $1.97M expected vs $1.74M actual after calibration  
- **Variance:** +13.4% (directionally useful planning estimate)  
- **Business use case:** promotions, bidding, merchandising, funnel prioritization  

---

## What This Project Does

This project builds a two-stage session scoring system designed to assign a **probability of conversion** and **expected revenue value** to each user session.

The framework enables:

- Identification of high-value users before they convert  
- Targeted intervention on at-risk sessions  
- Smarter allocation of marketing spend and promotions  
- Revenue-based prioritization with margin-aware decisioning  

The notebook includes full model diagnostics, calibration checks, feature analysis, and implementation details.

---

## Key Idea

> **Expected Revenue = P(Convert) × Expected Spend**

Instead of treating all sessions equally, this framework estimates **how much each session may be worth**.

---

## Why It Matters

In typical ecommerce funnels, most sessions do not convert. This creates two costly problems:

- High-intent users may drop off without intervention  
- Low-value traffic can consume marketing budget  

This project addresses both by identifying:

- **Who is likely to convert**  
- **Who may need a nudge**  
- **Who is not worth targeting heavily**  

---

## Approach

### Stage 1 — Conversion Propensity

- **Model:** XGBoost Classifier  
- **Output:** Probability of purchase  
- **Performance:** ROC-AUC ≈ 0.80 with strong ranking lift  

### Stage 2 — Spend Estimation

- **Method:** Baseline historical AOV lookup  
- **Design Choice:** Intentionally simple for interpretability and modular extension to regression-based spend modeling  
- **Insight:** Behaviour predicts intent more reliably than spend magnitude  

### Final Output

- Session-level expected revenue  
- Actionable segmentation for marketing, pricing, and merchandising  

---

## Revenue Reconciliation

After probability calibration, the model produced the following held-out test-set estimate:

| Metric | Value |
|---|---:|
| Expected revenue (calibrated) | $1,972,962.80 |
| Actual revenue | $1,739,605.48 |
| Variance | +$233,357.32 |
| Variance (%) | +13.4% |

Calibration corrected overconfidence in the raw probabilities while preserving ranking performance. Revenue outputs should be interpreted as **planning estimates**, not guaranteed realized outcomes.

---

## Business Interpretation

- Strong enough for session ranking and prioritization  
- Useful for promotion targeting and budget allocation  
- Revenue estimates are directionally informative  
- Spend layer can be upgraded independently without rebuilding the full pipeline  

> **Note:** Propensity scores estimate likelihood of purchase, not incremental treatment effect. In production, experimentation or uplift modeling would strengthen intervention decisions.

---

## Example Model Output (Illustrative)

| Session ID | P(Convert) | Expected Spend | Expected Revenue | Segment | Recommended Action |
|---|---:|---:|---:|---|---|
| S-10492 | 0.86 | $124.50 | $107.07 | High-Certainty | Protect margin |
| S-21984 | 0.58 | $96.20 | $55.80 | At-Risk | Trigger incentive |
| S-33871 | 0.12 | $42.00 | $5.04 | Low Interest | Suppress remarketing |

*Illustrative values used to demonstrate the hurdle framework. Actual scores are generated at inference time.*

---

## Segmentation Logic

| Segment | Probability | Recommended Action |
|---|---|---|
| **High-Certainty** | >80% | Protect margin / no discount |
| **At-Risk** | 40–70% | Trigger incentive / recover demand |
| **Low Interest** | <40% | Reduce spend / suppress remarketing |

---

## GA4 Alignment

This project was structured to approximate a Google Analytics 4 BigQuery export workflow.

| Project Field | Comparable GA4 Field |
|---|---|
| `events.csv` | `events_*` tables |
| `event_type` | `event_name` |
| `customer_id` | `user_pseudo_id` |
| `session_id` | `ga_session_id` |
| `purchase_amount` | `ecommerce.purchase_revenue` |

While not run on a live GA4 property, the workflow was designed to transfer to GA4-style event data after validating:

- Event quality  
- Session logic  
- Identity stitching  
- Revenue fields  
- Leakage safeguards  

---

## Dataset

**Source:** Marketing & E-Commerce Analytics Dataset (Kaggle)  

- ~100,000 customers  
- 2M+ interaction events  
- 5 relational tables: customers, campaigns, events, products, transactions  

**Note:** Data files are excluded from the repository due to size. Download from Kaggle and place in `data/raw/`. Processed files regenerate through the notebook pipeline.

---

## Core Insight

> **Clicks signal intent — not wallet.**  
> Session behaviour helps predict *whether* someone buys.  
> Customer history helps predict *how much* they spend.

That distinction is critical for pricing, bidding, and promotional efficiency.

---

## Project Origin

This repository is a portfolio-enhanced version of the Predictive Funnel Analytics project originally developed for the Supervised Machine Learning course in the Data Science & Machine Learning program at Red River College Polytechnic.

The academic version focused on model development and evaluation. This version reframes the work as a business-facing GA4-aligned ecommerce analytics case study.
