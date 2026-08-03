## PLG Funnel Analysis Dashboard
End-to-End Product-Led Growth Analytics — from Synthetic Data to Semantic Model

## Overview

A complete Product-Led Growth (PLG) analytics pipeline, built to demonstrate the full path from raw event data to a production-style, refreshable BI dashboard: synthetic data generation → normalized MySQL warehouse → SQL analysis → a star-schema semantic model → live DAX measures → an interactive Power BI report.

The project simulates a 10,000-user SaaS product and answers three questions any PLG team asks: where users drop off in the funnel, which experiments actually move the needle, and how retention behaves across cohorts over time.

## Business Problem

Product-led growth platforms generate constant event volume but often can't answer simple questions cleanly: where exactly is the funnel leaking users, which of several competing experiments is worth prioritizing, and whether early cohort behavior is stable enough to trust. This project builds the full analytical stack needed to answer those three questions from first principles, rather than from a spreadsheet someone manually maintains.

## Solution

A normalized MySQL warehouse (3NF) with dimension and fact tables built around a user_id grain.

Ten hand-written SQL queries covering funnel conversion, segmentation, time-to-value, cohort retention, A/B test comparison, churn risk, and LTV.

A Python EDA layer (analysis/PLG_Analytics_EDA_v2.py) that runs proper statistical validation — chi-square significance testing — on all three A/B tests, not just raw percentage comparisons.

A Power BI semantic model with a genuine star schema, an explicit _Measures table, and every visual backed by live DAX — no static exports, no manually maintained snapshot data anywhere in the report.

## Architecture

The dashboard connects to MySQL via ODBC and refreshes directly from the warehouse — there is no intermediate export step between the database and the report. See docs/database_erd.png for the full entity-relationship diagram of the warehouse schema.

## Database Schema

**Dimension Tables**

| Table                | Purpose                                                                                                         |
| -------------------- | --------------------------------------------------------------------------------------------------------------- |
| **dim_users**        | Account-level attributes including user segment, device, platform, industry, and signup date.                   |
| **dim_funnel_stage** | Lookup dimension providing funnel stage labels and explicit sort order, decoupled from raw `event_type` values. |

**Fact Tables**

| Table                | Grain                     | Purpose                                                                                  |
| -------------------- | ------------------------- | ---------------------------------------------------------------------------------------- |
| **fact_user_events** | One row per user event    | Stores the complete product journey from signup through payment.                         |
| **fact_ab_tests**    | One row per user per test | Stores A/B test assignments, variants, and conversion outcomes across three experiments. |
| **fact_cohort_data** | One row per user          | Stores milestone dates and time-to-conversion metrics for cohort analysis.               |



---

## Why a dimension for funnel stages: 

event_type in the fact table is a system value (feature_use), not a display label, and carries no inherent ordering. Rather than embed presentation logic directly in the event log or route it through a disconnected helper table, dim_funnel_stage holds the natural key, display label, and sort order as a proper one-to-many related dimension — keeping the fact table a clean, unopinionated record of what happened. Full relationships are visualized in docs/database_erd.png



## Dashboard Walkthrough

**Page 1** — Funnel Conversion KPI cards (Signups, Activated, Feature Users, PQL Qualified, Paid), a funnel visualization, and a stage-by-stage conversion table showing drop-off between each step of the journey.

---

**Page 2** - Experiments & Retention A/B test conversion rates by test, an A/B test summary (sample sizes, absolute and relative lift), and monthly cohort performance tracking retention and engagement over time.

---

The dashboard is intentionally scoped to these two focused, interactive pages rather than a static summary view — every number is explorable and refreshes from the live model.

## Key Metrics

| Funnel Stage     |  Users | Conversion from Previous Stage |
| ---------------- | -----: | -----------------------------: |
| Signup           | 10,000 |                              — |
| Activation       |  7,027 |                         70.27% |
| Feature Adoption |  3,496 |                         49.75% |
| PQL Qualified    |  1,434 |                         41.02% |
| Paid Conversion  |    378 |                         26.36% |


## A/B Testing Analysis

| Experiment       | Control | Treatment | Absolute Lift | Relative Lift |
| ---------------- | ------: | --------: | ------------: | ------------: |
| Feature Adoption |  14.67% |    23.56% |     +8.89 pts |       +60.61% |
| Onboarding Flow  |  15.35% |    26.02% |    +10.67 pts |       +69.51% |
| Pricing Strategy |  15.40% |    23.57% |     +8.17 pts |       +53.01% |


All three tests ran on balanced samples (~4,000 users per variant) and were validated for statistical significance using chi-square testing (p < 0.05) in analysis/PLG_Analytics_EDA_v2.py, not just raw percentage comparison.

## Cohort Analysis

Weekly signup cohorts tracked across the full observation window (aggregated to monthly in the dashboard view):

| Metric                               |  Value |
| ------------------------------------ | -----: |
| Cohort Size                          | 10,000 |
| Week 1 Retention (Activation)        | 70.27% |
| Week 2 Engagement (Feature Adoption) | 34.96% |
| Paid Conversion                      |  3.78% |

---

Every visual in the report is powered by an explicit measure in a dedicated _Measures table — there are no implicit aggregations and no business logic embedded in calculated columns. Measures use direct boolean filter arguments in CALCULATE rather than wrapping FILTER() around entire tables, and stage-over-stage conversion is computed via a self-referencing lookup against dim_funnel_stage[SortOrder] rather than hardcoded stage-to-stage logic. All relationships are single-direction unless a specific case requires otherwise, keeping filter propagation predictable across the model.

**Project evolution**: the dashboard was originally built against manually maintained Excel snapshot tables layered on top of the connected database. During a later engineering pass, the model was fully migrated to compute every visual live from the warehouse via DAX, and the snapshot tables were removed entirely — a deliberate step to ensure the dashboard reflects the actual state of the data rather than a point-in-time export.

## Project Structure

## 📂 Project Structure

```text
PLG_Analytics_Project/
├── Dashboard/
│   └── PLG_Funnel_Analysis_Dashboard.pbix
│
├── DATABASE/
│   ├── Database_Setup.sql
│   ├── Queries.sql
│   ├── migration_01_add_dim_funnel_stage.sql
│   └── reset_database.sql
│
├── DATA/
│   └── plg_data_generator.py
│
├── analysis/
│   └── PLG_Analytics_EDA_v2.py
│
├── docs/
│   ├── screenshots/
│   │   ├── funnel_conversion.png
│   │   ├── experiments_retention.png
│   │   └── mysql_erd.png
│   │
│   └── PLG_Analytics_Report.pdf
│
├── README.md
├── .gitignore
└── LICENSE
```


## Screenshots

See docs/ for the full-resolution dashboard pages (funnel_conversion.png, experiments_retention.png) and the warehouse entity-relationship diagram (database_erd.png).

## Learning Outcomes
Designing a normalized, query-efficient MySQL warehouse from scratch, including dimension modeling decisions (degenerate dimensions, natural vs. surrogate keys).
Writing production-style DAX: explicit measures, correct filter context, self-referencing lookups for sequential comparisons, and avoiding anti-patterns like disconnected helper tables where a proper relationship is the better fit.

Recognizing and correcting a real architectural gap mid-project — migrating a dashboard from static, manually maintained data to a fully live, DAX-driven semantic model — rather than treating "it displays correctly" as equivalent to "it's built correctly."

Applying proper statistical validation (chi-square significance testing) to A/B test results instead of relying on raw percentage comparisons.

## Future Enhancements
Extend the schema to link A/B test participation to downstream payment events, enabling a defensible revenue-impact calculation rather than the current standalone reporting of conversion lift and revenue as separate signals.
Add incremental refresh for the fact tables as event volume scales beyond a single full-refresh pattern.
Formalize the SQL migration scripts under a lightweight versioning convention as the schema continues to evolve.

## License
MIT — see **LICENSE** for details.
