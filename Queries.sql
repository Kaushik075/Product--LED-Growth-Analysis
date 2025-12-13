-- QUERY 1: PLG FUNNEL CONVERSION RATES --

SELECT 
    'Signup' as funnel_stage,
    COUNT(DISTINCT user_id) as users_count,
    ROUND(100.0 * COUNT(DISTINCT user_id) / (SELECT COUNT(*) FROM dim_users), 2) as conversion_rate
FROM fact_user_events
WHERE event_type = 'signup'

UNION ALL

SELECT 
    'Activation',
    COUNT(DISTINCT user_id),
    ROUND(100.0 * COUNT(DISTINCT user_id) / (SELECT COUNT(*) FROM dim_users), 2)
FROM fact_user_events
WHERE event_type = 'activation'

UNION ALL

SELECT 
    'Feature Adoption',
    COUNT(DISTINCT user_id),
    ROUND(100.0 * COUNT(DISTINCT user_id) / (SELECT COUNT(*) FROM dim_users), 2)
FROM fact_user_events
WHERE event_type = 'feature_use'

UNION ALL

SELECT 
    'PQL Qualified',
    COUNT(DISTINCT user_id),
    ROUND(100.0 * COUNT(DISTINCT user_id) / (SELECT COUNT(*) FROM dim_users), 2)
FROM fact_user_events
WHERE event_type = 'pql_qualified'

UNION ALL

SELECT 
    'Paid Conversion',
    COUNT(DISTINCT user_id),
    ROUND(100.0 * COUNT(DISTINCT user_id) / (SELECT COUNT(*) FROM dim_users), 2)
FROM fact_user_events
WHERE event_type = 'payment_complete'
ORDER BY conversion_rate DESC;


-- QUERY 2: FUNNEL BY USER SEGMENT --

SELECT 
    u.user_segment,
    COUNT(DISTINCT CASE WHEN e.event_type = 'signup' THEN u.user_id END) as signups,
    COUNT(DISTINCT CASE WHEN e.event_type = 'activation' THEN u.user_id END) as activated,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.event_type = 'activation' THEN u.user_id END) / 
          COUNT(DISTINCT CASE WHEN e.event_type = 'signup' THEN u.user_id END), 2) as activation_rate,
    COUNT(DISTINCT CASE WHEN e.event_type = 'payment_complete' THEN u.user_id END) as customers,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.event_type = 'payment_complete' THEN u.user_id END) / 
          COUNT(DISTINCT CASE WHEN e.event_type = 'signup' THEN u.user_id END), 2) as conversion_rate
FROM dim_users u
LEFT JOIN fact_user_events e ON u.user_id = e.user_id
GROUP BY u.user_segment
ORDER BY conversion_rate DESC;


-- QUERY 3: FUNNEL BY DEVICE TYPE --

SELECT 
    u.device_type,
    COUNT(DISTINCT CASE WHEN e.event_type = 'signup' THEN u.user_id END) as signups,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.event_type = 'activation' THEN u.user_id END) / 
          COUNT(DISTINCT CASE WHEN e.event_type = 'signup' THEN u.user_id END), 2) as activation_rate,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.event_type = 'feature_use' THEN u.user_id END) / 
          COUNT(DISTINCT CASE WHEN e.event_type = 'signup' THEN u.user_id END), 2) as engagement_rate,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN e.event_type = 'payment_complete' THEN u.user_id END) / 
          COUNT(DISTINCT CASE WHEN e.event_type = 'signup' THEN u.user_id END), 2) as conversion_rate
FROM dim_users u
LEFT JOIN fact_user_events e ON u.user_id = e.user_id
GROUP BY u.device_type
ORDER BY conversion_rate DESC;


-- QUERY 4: TIME TO VALUE (TTV) ANALYSIS --

SELECT 
    'Signup to Activation' as journey_stage,
    ROUND(AVG(c.days_to_activation), 1) as avg_days,
    ROUND(AVG(c.days_to_activation), 1) as median_days,
    MIN(c.days_to_activation) as min_days,
    MAX(c.days_to_activation) as max_days,
    COUNT(DISTINCT c.user_id) as users_completed
FROM fact_cohort_data c
WHERE c.activation_date IS NOT NULL

UNION ALL

SELECT 
    'Activation to PQL',
    ROUND(AVG(DATEDIFF(c.pql_date, c.activation_date)), 1),
    ROUND(AVG(DATEDIFF(c.pql_date, c.activation_date)), 1),
    MIN(DATEDIFF(c.pql_date, c.activation_date)),
    MAX(DATEDIFF(c.pql_date, c.activation_date)),
    COUNT(DISTINCT c.user_id)
FROM fact_cohort_data c
WHERE c.pql_date IS NOT NULL AND c.activation_date IS NOT NULL

UNION ALL

SELECT 
    'PQL to Paid',
    ROUND(AVG(DATEDIFF(c.payment_date, c.pql_date)), 1),
    ROUND(AVG(DATEDIFF(c.payment_date, c.pql_date)), 1),
    MIN(DATEDIFF(c.payment_date, c.pql_date)),
    MAX(DATEDIFF(c.payment_date, c.pql_date)),
    COUNT(DISTINCT c.user_id)
FROM fact_cohort_data c
WHERE c.payment_date IS NOT NULL AND c.pql_date IS NOT NULL;


-- QUERY 5: COHORT RETENTION ANALYSIS (WEEKLY) --

SELECT 
    c.cohort_date as cohort_week,
    COUNT(DISTINCT c.user_id) as cohort_size,
    COUNT(DISTINCT CASE WHEN c.activation_date IS NOT NULL THEN c.user_id END) as week1_active,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN c.activation_date IS NOT NULL THEN c.user_id END) / 
          COUNT(DISTINCT c.user_id), 2) as week1_retention_rate,
    COUNT(DISTINCT CASE WHEN c.feature_adoption_date IS NOT NULL THEN c.user_id END) as week2_engaged,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN c.feature_adoption_date IS NOT NULL THEN c.user_id END) / 
          COUNT(DISTINCT c.user_id), 2) as week2_engagement_rate,
    COUNT(DISTINCT CASE WHEN c.payment_date IS NOT NULL THEN c.user_id END) as paid_customers,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN c.payment_date IS NOT NULL THEN c.user_id END) / 
          COUNT(DISTINCT c.user_id), 2) as paid_conversion_rate
FROM fact_cohort_data c
GROUP BY c.cohort_date
ORDER BY c.cohort_date DESC;


-- QUERY 6: A/B TEST ANALYSIS - OVERALL RESULTS --

SELECT 
    test_name,
    variant,
    COUNT(DISTINCT user_id) as users_assigned,
    SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) as conversions,
    ROUND(100.0 * SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) / COUNT(DISTINCT user_id), 2) as conversion_rate
FROM fact_ab_tests
GROUP BY test_name, variant
ORDER BY test_name, conversion_rate DESC;


-- QUERY 7: A/B TEST - STATISTICAL SIGNIFICANCE --

WITH test_stats AS (
    SELECT 
        test_name,
        variant,
        COUNT(DISTINCT user_id) as sample_size,
        SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) as successes,
        ROUND(100.0 * SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) / COUNT(DISTINCT user_id), 2) as success_rate
    FROM fact_ab_tests
    GROUP BY test_name, variant
)
SELECT 
    test_name,
    MAX(CASE WHEN variant LIKE 'control%' THEN success_rate END) as control_rate,
    MAX(CASE WHEN variant NOT LIKE 'control%' THEN success_rate END) as treatment_rate,
    ROUND(MAX(CASE WHEN variant NOT LIKE 'control%' THEN success_rate END) - 
          MAX(CASE WHEN variant LIKE 'control%' THEN success_rate END), 2) as lift_percentage,
    CASE 
        WHEN ABS(MAX(CASE WHEN variant NOT LIKE 'control%' THEN success_rate END) - 
                 MAX(CASE WHEN variant LIKE 'control%' THEN success_rate END)) > 5 THEN '✅ Significant'
        ELSE '⚠️ Inconclusive'
    END as significance
FROM test_stats
GROUP BY test_name;


-- QUERY 8: PQL IDENTIFICATION - CHARACTERISTICS --

SELECT 
    u.user_segment,
    u.device_type,
    u.platform,
    COUNT(DISTINCT u.user_id) as total_users,
    COUNT(DISTINCT CASE WHEN c.pql_date IS NOT NULL THEN u.user_id END) as pql_count,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN c.pql_date IS NOT NULL THEN u.user_id END) / 
          COUNT(DISTINCT u.user_id), 2) as pql_rate,
    ROUND(AVG(c.days_to_pql), 1) as avg_days_to_pql
FROM dim_users u
LEFT JOIN fact_cohort_data c ON u.user_id = c.user_id
GROUP BY u.user_segment, u.device_type, u.platform
HAVING COUNT(DISTINCT u.user_id) > 20
ORDER BY pql_rate DESC;


-- QUERY 9: CHURN ANALYSIS - AT-RISK SEGMENTS --

SELECT 
    u.user_segment,
    COUNT(DISTINCT u.user_id) as total_users,
    COUNT(DISTINCT CASE WHEN e.event_type = 'activation' THEN u.user_id END) as activated,
    COUNT(DISTINCT CASE WHEN c.feature_adoption_date IS NULL AND 
                             DATEDIFF(CURDATE(), u.signup_date) > 14 THEN u.user_id END) as inactive_14days,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN c.feature_adoption_date IS NULL AND 
                                          DATEDIFF(CURDATE(), u.signup_date) > 14 THEN u.user_id END) / 
          COUNT(DISTINCT u.user_id), 2) as churn_risk_rate
FROM dim_users u
LEFT JOIN fact_user_events e ON u.user_id = e.user_id
LEFT JOIN fact_cohort_data c ON u.user_id = c.user_id
GROUP BY u.user_segment
ORDER BY churn_risk_rate DESC;


-- QUERY 10: REVENUE ANALYSIS - LTV BY COHORT --

SELECT 
    c.cohort_date,
    COUNT(DISTINCT c.user_id) as cohort_size,
    ROUND(SUM(CASE WHEN e.event_type = 'payment_complete' THEN e.event_value ELSE 0 END), 2) as total_revenue,
    COUNT(DISTINCT CASE WHEN e.event_type = 'payment_complete' THEN c.user_id END) as paying_customers,
    ROUND(SUM(CASE WHEN e.event_type = 'payment_complete' THEN e.event_value ELSE 0 END) / 
          COUNT(DISTINCT c.user_id), 2) as revenue_per_user,
    ROUND(SUM(CASE WHEN e.event_type = 'payment_complete' THEN e.event_value ELSE 0 END) / 
          NULLIF(COUNT(DISTINCT CASE WHEN e.event_type = 'payment_complete' THEN c.user_id END), 0), 2) as arpu
FROM fact_cohort_data c
LEFT JOIN fact_user_events e ON c.user_id = e.user_id
GROUP BY c.cohort_date
ORDER BY c.cohort_date DESC;