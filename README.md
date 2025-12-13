
## Product LED Growth Funnel Analysis- SaaS User Journey & Experimentation 


 Executive Summary
 ---
This project demonstrates a complete, production-grade analytics pipeline that transforms raw user data into actionable business intelligence. Starting from a normalized MySQL database with 10,000 users and 51,000+ events, the analysis identifies a critical feature adoption bottleneck and quantifies a $570K/year revenue opportunity through A/B testing and statistical validation.

 Key Deliverables
 ---

📊 EDA Report: PLG_Analytics_Report.pdf - Comprehensive exploratory data analysis with statistical findings

📋 SQL Queries: PLG_MySQL_Queries.pdf - 10 production-ready queries covering funnel, cohort, and revenue analysis

📈 Power BI Dashboard: 3-page interactive dashboard with automated insights and recommendations

🐍 Python Analysis: End-to-end data pipeline with chi-square testing and scenario modeling


 Quick Insights Identified
---
Feature Adoption Gap: 50% of activated users don't use features (critical bottleneck identified)

Tooltip Guide Test: +87% lift validated through A/B testing (p < 0.001)

Revenue Impact: Deploying recommendations could generate +$165K to +$570K annually

Implementation Timeline: 7 weeks to full deployment across all 3 experiments



🔍 Business Problem
---
Product-led growth platforms struggle with understanding user progression through the funnel and identifying where interventions create the most impact. This project addresses three critical questions:

Where do users drop off? Analysis reveals 50% activation-to-feature adoption drop-off, indicating a severe engagement issue that costs the company ~$200K annually in potential revenue.

Which interventions work best? Three A/B tests were designed to address different funnel stages: onboarding flow (+31% lift), pricing strategy (+47% lift), and feature adoption (+87% lift), all achieving statistical significance.

Is deployment safe? Weekly cohort analysis confirms metrics are stable (variance < 1%), validating that observed improvements are genuine and not noise.

Methodology
---

# Phase 1: Data Generation & Infrastructure

The project begins with a 3NF normalized MySQL database designed to handle millions of records with proper relationships and constraints. Using Python and the Faker library, 10,000 realistic user profiles were generated across Organic, Paid, Referral, and Direct segments with device and platform distribution. Events were created to simulate realistic user journeys (51,231 total events) with probabilistic conversion rates at each funnel stage (signup→activation: 70%, activation→feature: 50%, feature→PQL: 40%, PQL→paid: 25%).

# Phase 2: Exploratory Data Analysis

Pandas-based EDA examined user demographics, funnel progression, and temporal patterns. Each user segment was analyzed separately to identify performance differences (Direct segment showed 4.3% conversion vs 3.4% for Paid). Time-to-value metrics were calculated (1.1 days signup→activation, 11 days activation→PQL, 15 days PQL→paid), revealing that the activation bottleneck happens early when engagement barriers are highest.

# Phase 3: A/B Testing & Statistical Validation

Three concurrent tests were conducted on balanced samples (n=4,000 per variant). Chi-square tests confirmed statistical significance for all treatments (p < 0.001, 99.9% confidence level). The Feature Adoption test achieved the highest lift (+87%) using an in-app tooltip, demonstrating that simple, contextual guidance directly addresses the engagement gap identified in Phase 2.

# Phase 4: Power BI Visualization & Insights

A professional 3-page dashboard was built in Power BI to present findings: funnel visualization with drop-off indicators, A/B test comparison charts, and weekly cohort retention tracking. An insights bookmark synthesizes all analysis into 8 actionable boxes covering health assessment, statistical significance, revenue scenarios, and priority recommendations, making the findings accessible to both technical and non-technical stakeholders.

# Phase 5: Business Impact Modeling & Documentation

Three revenue scenarios were modeled based on test results: deploying the tooltip guide (low effort, +$165.6K/year), implementing freemium pricing (+$318.6K/year), or both (+$570K/year). Documentation ensures every number is traceable to its underlying calculation, supporting stakeholder confidence in deployment decisions.

Results & Key Findings
--
Funnel Performance Analysis
The complete funnel shows healthy top-of-funnel (70% activation, industry average) but severe mid-funnel friction. Feature adoption sits at just 35% of signups (vs. expected 50%+), representing the primary bottleneck. This 50% activation-to-feature drop-off translates directly to revenue loss: if adoption improved to 60%, an additional $165K would be generated annually based on current cohort data.

<img width="739" height="305" alt="Image" src="https://github.com/user-attachments/assets/615c8e32-6e89-4fe2-ba61-f21cf741f3c8" />


A/B Test Results with Statistical Validation
--

All three treatments showed statistically significant improvements. The Feature Adoption test using an in-app tooltip guide emerged as the clear winner: 28% conversion vs. 15% control, a +87% relative lift. This is particularly powerful because tooltip implementation requires minimal engineering effort (UI change only) and delivers the highest business impact.

<img width="734" height="327" alt="Image" src="https://github.com/user-attachments/assets/e0bc6a42-afe3-4ca8-8d11-b4133804781d" />


Cohort Stability & Risk Assessment
-
Weekly cohorts from August through November show consistent metrics (±0.09% activation variance, ±0.15% feature adoption variance), confirming that conversion patterns are stable and not driven by seasonal or temporal anomalies. This low variance validates deployment safety: improvements observed in A/B tests reflect genuine behavioral changes, not noise.

Device & Segment Performance Insights
-
Mobile users outperform desktop (4.14% vs 3.28% conversion), while Direct acquisition channels show 27% higher conversion than Paid channels (4.32% vs 3.42%). These insights suggest prioritizing mobile experience optimization and investigating why Paid channels underperform relative to organic acquisition.
