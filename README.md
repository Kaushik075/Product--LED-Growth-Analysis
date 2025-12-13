
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




🔍 Business Problem
---
Product-led growth platforms struggle with understanding user progression through the funnel and identifying where interventions create the most impact. This project addresses three critical questions:

Where do users drop off? Analysis reveals 50% activation-to-feature adoption drop-off, indicating a severe engagement issue that costs the company ~$200K annually in potential revenue.

Which interventions work best? Three A/B tests were designed to address different funnel stages: onboarding flow (+31% lift), pricing strategy (+47% lift), and feature adoption (+87% lift), all achieving statistical significance.

Is deployment safe? Weekly cohort analysis confirms metrics are stable (variance < 1%), validating that observed improvements are genuine and not noise.

# images

📊 DASHBOARD Overview 

# Funnel Conversion Analysis
Shows 10K users → 7K activated (70%) → 3.5K feature adoption (50% DROP-OFF) → 378 paid (3.8% conversion)

Key Finding: Feature adoption is the bottleneck. Half of activated users never discover key features.

# Experiments & Retention
Your A/B tests show massive wins:

Tooltip Guide: +87% lift ✅ Deploy (solves feature adoption gap)

Freemium Model: +47% lift ✅ Deploy (highest revenue impact)

Quick Start: +31% lift ✅ Deploy (improves onboarding)

Validation: 99.8% cohort stability means these improvements will stick.

# Strategic Insights
The "exec summary" page with:

Funnel health assessment (calculations shown)

A/B test lift calculations (all p<0.001)

Revenue impact analysis: +$165K-$570K/year depending on deployment

Top 3 priority actions with ROI scores



Insights Identified
---

50% Feature Adoption Bottleneck Worth $200K+:
Half of activated users never use features, representing your largest revenue leakage opportunity.

+87% Lift Solution Validated (p < 0.001):
Tooltip guide test proves high-impact fix with 99.9% confidence, generating +$165.6K annually from simple UI change.

$570K Combined Revenue Opportunity (87% Growth):
Three interventions (tooltip, freemium, retargeting) transform revenue from $680K to $1.25M over 7 weeks.

<1% Cohort Variance Confirms Safe Deployment: 
User behavior is stable across 8 weeks, validating A/B results are genuine and safe to deploy at scale.

Mobile 26% Better Than Desktop, Direct 27% Better Than Paid: 
Segment gaps reveal optimization opportunities in device UX and paid targeting without major product changes.


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

Results 
--
## Funnel Performance Analysis

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


MAJOR RECOMMENDATIONS
-
Deploy Tooltip Guide First (2 Weeks, +$165.6K ROI):
Launch feature adoption tooltip immediately as quickest win with highest lift (+87%) and lowest effort (UI change only) to establish momentum.

Implement Freemium Pricing Second (4 Weeks, +$318.6K ROI):
Roll out freemium model in parallel to capture price-sensitive segment and expand customer base while tooltip impact is validated in production.

Launch Retargeting Campaign for Inactive Users (1 Week, +$45K ROI): 
Target 3,661 activated users who skip features with email/push using tooltip insights to capture low-hanging fruit while major initiatives deploy.

Monitor Feature Adoption Rate Weekly (Target: 49.7% → 65%):
Track progress toward 65% feature adoption goal post-deployment with real-time dashboards to ensure improvements match A/B test results in production.

Phased 20% Rollout Before Full Deployment (Risk Mitigation): 
Test all interventions on 20% user segment first to validate production results before 100% deployment, protecting against unexpected environment-specific issues.
