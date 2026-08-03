<div align="center">

# 📊 PLG Funnel Analytics
### End-to-End Product-Led Growth Analysis Platform

**A full-stack analytics engineering project modeling the signup → activation → paid-conversion journey of a simulated 10,000-user SaaS product — built on a real MySQL warehouse, validated with statistical A/B testing, and visualized in a live-connected Power BI dashboard.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Power BI](https://img.shields.io/badge/Power%20BI-DAX%20%2F%20Live%20Connection-F2C811?style=flat-square&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Pandas](https://img.shields.io/badge/pandas-2.0-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![SciPy](https://img.shields.io/badge/SciPy-Statistical%20Testing-8CAAE6?style=flat-square&logo=scipy&logoColor=white)](https://scipy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

</div>

---

## 📖 Table of Contents

1. [Project Overview](#-project-overview)
2. [Business Problem](#-business-problem)
3. [Solution Overview](#-solution-overview)
4. [Architecture](#-architecture)
5. [Technology Stack](#-technology-stack)
6. [Data Model](#-data-model)
7. [Database Statistics](#-database-statistics)
8. [Funnel Analysis](#-funnel-analysis)
9. [Dashboard Overview](#-dashboard-overview)
10. [A/B Testing Analysis](#-ab-testing-analysis)
11. [Cohort Analysis](#-cohort-analysis)
12. [Revenue Analysis](#-revenue-analysis)
13. [Folder Structure](#-folder-structure)
14. [Installation](#-installation)
15. [Screenshots](#-screenshots)
16. [Key Learnings](#-key-learnings)
17. [Future Improvements](#-future-improvements)
18. [License](#-license)
19. [Contact](#-contact)

---

## 🎯 Project Overview

This project simulates and analyzes the complete **Product-Led Growth (PLG) funnel** of a SaaS product — from initial signup through activation, feature adoption, product-qualified-lead (PQL) status, and paid conversion — for a synthetic base of **10,000 users**.

It is built as a genuine data engineering pipeline, not a static analysis notebook: a normalized MySQL warehouse feeds a Power BI dashboard through a **live DAX connection**, meaning every visual recalculates directly against the database rather than reading from a frozen export. On top of the warehouse, a Python analysis layer runs statistical validation — including chi-square significance testing — on three simulated A/B experiments.

The goal was to practice and demonstrate the full lifecycle a Data/Analytics Engineer actually owns: schema design, reproducible data generation, SQL analysis, statistical rigor, and BI delivery — end to end, with no step skipped or faked.

---

## 💼 Business Problem

SaaS companies operating a product-led growth motion live or die by one question: **where in the user journey are we losing people, and which levers actually move the needle?**

A raw signups number tells you nothing about:
- How many users ever reach meaningful activation
- Where the sharpest drop-offs occur between funnel stages
- Whether a specific onboarding or pricing change actually improves conversion, or whether an observed lift is just noise
- What a converted customer is actually worth, in aggregate

This project frames and answers exactly that set of questions using a structured funnel model, cohort tracking, and hypothesis-tested experimentation — the same analytical toolkit a PLG-focused analytics team would use in production.

---

## 🛠 Solution Overview

The project is organized as four connected layers:

| Layer | Purpose |
|---|---|
| **Data Generation** (`data/plg_data_generator.py`) | Produces a reproducible, seeded synthetic dataset simulating realistic funnel behavior, A/B test assignments, and cohort outcomes |
| **Warehouse** (`database/`) | A normalized MySQL star schema storing users, funnel events, A/B test results, and cohort-level journey timing |
| **Analysis** (`analysis/PLG_Analytics_EDA.py`) | Runs funnel, cohort, and experiment analysis in Python, including a real chi-square significance test on each A/B experiment |
| **Visualization** (`dashboard/PLG_Funnel_Analysis_Dashboard.pbix`) | A two-page Power BI report connected live to the MySQL warehouse via DAX — no static exports, no manual refresh step |

---

## 🏗 Architecture

```
┌─────────────────────┐      ┌──────────────────────┐      ┌───────────────────────┐
│  plg_data_generator  │ ───▶ │   MySQL Warehouse     │ ───▶ │   Power BI Dashboard   │
│   (Python / Faker)   │      │   (plg_analytics)     │      │  (Live DAX connection) │
└─────────────────────┘      └──────────┬───────────┘      └───────────────────────┘
                                          │
                                          ▼
                              ┌──────────────────────┐
                              │  PLG_Analytics_EDA    │
                              │ (pandas / SciPy stats)│
                              └──────────────────────┘
```

The dashboard connects to MySQL directly — there is no intermediate CSV or Excel export between the database and the report. This was a deliberate architectural choice: every KPI on the dashboard reflects the current state of the warehouse, not a snapshot frozen at generation time.

---

## 🧰 Technology Stack

| Category | Tools |
|---|---|
| **Database** | MySQL 8.0 (window functions, CTEs) |
| **Data Generation** | Python, Faker (seeded for reproducibility) |
| **Analysis** | Python, pandas, NumPy, SciPy (`chi2_contingency`) |
| **Visualization** | Power BI Desktop, DAX, live MySQL connection |
| **Version Control** | Git / GitHub |

---

## 🗂 Data Model

The warehouse is modeled as a **star schema** — a central set of fact tables recording events and outcomes, surrounding a shared user dimension.

### Tables

| Table | Type | Grain | Purpose |
|---|---|---|---|
| `dim_users` | Dimension | 1 row per user | Account-level attributes: segment, country, industry, device/platform, signup date |
| `dim_funnel_stage` | Dimension | 1 row per funnel stage | Maps each raw `event_type` to a display label and sort order for the funnel visual |
| `fact_user_events` | Fact | 1 row per event | The raw event log — every signup, activation, feature-adoption, PQL, and payment event per user |
| `fact_ab_tests` | Fact | 1 row per user per test | A/B test variant assignment and conversion outcome for each of the three experiments |
| `fact_cohort_data` | Fact | 1 row per user | Pre-computed journey timing per user — days to activation, days to PQL, days to payment |

### Why `dim_funnel_stage` exists

`event_type` in `fact_user_events` is a system value (e.g. `feature_adoption`), not a presentation-ready label, and it carries no inherent ordering. Rather than hardcode display logic into the fact table or a report-side transform, `dim_funnel_stage` holds the natural key, a clean `stage_label`, and an explicit `sort_order` — keeping the fact table an unopinionated record of what happened, while giving the dashboard a proper dimension to join against for labeling and ordering.

### Relationships

```
dim_users (1) ──── (many) fact_user_events
dim_users (1) ──── (many) fact_ab_tests
dim_users (1) ──── (1)    fact_cohort_data
dim_funnel_stage (1) ──── (many) fact_user_events   [via event_type]
```

Full visual reference: [`docs/images/database_erd.png`](docs/images/database_erd.png)

---

## 📈 Database Statistics

| Metric | Value |
|---|---|
| Total Users | 10,000 |
| Total Events Logged | 1 row per funnel touchpoint per user |
| A/B Test Participants | ~12,000 assignments across 3 experiments |
| Cohort Records | 10,000 (1 per user) |
| Funnel Stages Tracked | 5 |

---

## 🔻 Funnel Analysis

| Stage | Users | 
|---|---:|
| Signup | 10,000 |
| Activated | 7,027 |
| Feature Adoption | 3,496 |
| PQL Qualified | 1,434 |
| Paid Customers | 378 |
| **Overall Conversion** | **3.78%** |

The steepest drop-off occurs between **Activation → Feature Adoption** and again between **PQL → Paid Conversion** — the two stages where a PLG motion typically lives or dies: getting an activated user to genuinely adopt core functionality, and converting demonstrated intent (PQL) into an actual payment.

---

## 📊 Dashboard Overview

The Power BI report is built as two focused pages rather than one crowded view, each connected live to the MySQL warehouse.

### Funnel Conversion Dashboard
KPI cards for each funnel stage, a funnel visual showing stage-by-stage drop-off, and a supporting table with exact conversion percentages per stage.

`[ IMAGE PLACEHOLDER: docs/images/funnel_conversion.png ]`

### Experiments & Retention Dashboard
A/B test conversion-rate comparisons across all three experiments, a monthly cohort performance table, and week-1 retention tracking.

`[ IMAGE PLACEHOLDER: docs/images/experiments_retention.png ]`

---

## 🧪 A/B Testing Analysis

Three simulated experiments were run against distinct funnel levers — onboarding flow, pricing strategy, and feature adoption prompts — each assigned to a balanced control/treatment split of roughly 4,000 users per arm.

Rather than trust raw percentage-point differences, each result was validated using a **chi-square test of independence** (`scipy.stats.chi2_contingency`) in `analysis/PLG_Analytics_EDA.py`, confirming that the observed lift is statistically significant (p < 0.05) and not attributable to random variation.

| Test | Control | Treatment | Relative Lift | Sample Sizes (Control / Treatment) |
|---|---:|---:|---:|---:|
| Feature Adoption | 14.67% | 23.56% | +60.61% | 3,994 / 4,006 |
| Onboarding Flow | 15.35% | 26.02% | +69.51% | 3,915 / 4,085 |
| Pricing Strategy | 15.40% | 23.57% | +53.01% | 3,999 / 4,001 |

The **Onboarding Flow** experiment produced both the highest treatment conversion rate and the largest relative lift, making it the strongest candidate for a full rollout — with the caveat that this is a simulated dataset, and the statistical significance reflects internal validity of the test design, not a real-world business guarantee.

---

## 📅 Cohort Analysis

Every user is assigned a `cohort_date` at signup, and `fact_cohort_data` pre-computes their individual journey timing — `days_to_activation`, `days_to_pql`, `days_to_payment` — relative to that anchor date.

This allows retention and conversion to be tracked **by cohort** rather than in aggregate: grouping users by their signup month/week and measuring what percentage of each cohort reached activation, PQL, or payment within a fixed window (e.g. Week 1 retention). This is the standard approach for distinguishing "the funnel is improving over time" from "an early cohort happened to convert well" — comparing like-aged cohorts against each other rather than pooling all users regardless of tenure.

---

## 💰 Revenue Analysis

| Metric | Value |
|---|---:|
| Total Paying Customers | 378 |
| Total Revenue | $63,232.45 |
| ARPU (Average Revenue Per User) | $167.28 |

These are the only revenue figures reported. No revenue lift, incremental opportunity, or projected upside from the A/B tests is estimated or claimed here — the dataset is synthetic, and extrapolating a dollar impact from it would misrepresent what this project validates (statistical methodology and pipeline correctness, not real business economics).

---

## 📁 Folder Structure

```text
Product--LED-Growth-Analysis/
├── dashboard/
│   └── PLG_Funnel_Analysis_Dashboard.pbix
│
├── database/
│   ├── database_setup.sql
│   ├── Queries.sql
│   ├── migration_01_add_dim_funnel_stage.sql
│   └── reset_database.sql
│
├── data/
│   └── plg_data_generator.py
│
├── analysis/
│   └── PLG_Analytics_EDA.py
│
├── docs/
│   └── images/
│       ├── funnel_conversion.png
│       ├── experiments_retention.png
│       └── database_erd.png
│
├── PLG_Analytics_Report.pdf
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

---

## ⚙️ Installation

**Prerequisites:** MySQL Server running locally, Python 3.9+, Power BI Desktop (to open the `.pbix`).

```bash
# 1. Clone the repository
git clone https://github.com/Kaushik075/Product--LED-Growth-Analysis.git
cd Product--LED-Growth-Analysis

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Create the database and schema
mysql -u root -p < database/database_setup.sql

# 4. (Optional) Run the migration only if upgrading a pre-existing database
#    that predates dim_funnel_stage — not needed after a fresh install above
mysql -u root -p < database/migration_01_add_dim_funnel_stage.sql

# 5. Set your MySQL password as an environment variable (never hardcode it)
export PLG_MYSQL_PASSWORD="your_mysql_password"      # macOS/Linux
set PLG_MYSQL_PASSWORD=your_mysql_password            # Windows cmd

# 6. Re-generating data? Reset first to avoid duplicate rows
mysql -u root -p < database/reset_database.sql

# 7. Generate the synthetic dataset (10,000 users + events + A/B tests + cohorts)
python data/plg_data_generator.py

# 8. Run the statistical analysis (funnel, cohort, chi-square A/B validation)
python analysis/PLG_Analytics_EDA.py

# 9. Open the dashboard
#    dashboard/PLG_Funnel_Analysis_Dashboard.pbix in Power BI Desktop
#    (it connects live to the plg_analytics MySQL database)
```

---

## 🖼 Screenshots

### Funnel Conversion
`[ <img width="1079" height="679" alt="Image" src="https://github.com/user-attachments/assets/56541153-cf07-4bbf-89bc-b6395ead3116" /> ]`

### Experiments & Retention
`[<img width="1087" height="685" alt="Image" src="https://github.com/user-attachments/assets/29518125-4ddc-4859-b6d7-00fffa2f6a19" />]`

### Entity Relationship Diagram
`[ <img width="970" height="620" alt="Image" src="https://github.com/user-attachments/assets/97dd3eb5-b624-4ef7-807b-55f636a81476" /> ]`

---

## 🎓 Key Learnings

- **Live BI connections beat static exports.** Wiring the dashboard directly to MySQL via DAX — instead of a periodic Excel/CSV export — meant the report could never silently drift out of sync with the underlying data, at the cost of needing the database available whenever the report refreshes.
- **A percentage difference is not a significant result.** Building the chi-square validation step forced a real distinction between "the treatment number is higher" and "the treatment number is higher for a reason other than chance."
- **Schema decisions have consequences beyond the create-table statement.** Decoupling `event_type` from `stage_label`/`sort_order` in `dim_funnel_stage` made the funnel visual's ordering and labeling a data problem, not a report-side hack — a small design choice with an outsized effect on maintainability.
- **Reproducibility is a first-class requirement, not an afterthought.** Seeding the Faker/random generators and documenting an explicit setup order (schema → env var → generate → analyze) was necessary to make this project something another person could actually stand up from a clean clone, not just something that worked once on one machine.

---

## 🚀 Future Improvements

- Add automated data-quality checks (row-count and null-rate assertions) that run after each data-generation cycle
- Extend cohort analysis to track multi-month retention curves, not just Week 1
- Add a lightweight CI step that lints the SQL and validates the Python scripts compile on every push
- Parameterize the data generator (user count, funnel conversion rates) via a config file instead of in-code constants

---

## 📄 License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

## 📬 Contact

**Kaushik Yeddanapudi**
Data Engineering | Analytics Engineering
📍 Hyderabad, India

Feel free to open an issue on this repository for questions or feedback.

