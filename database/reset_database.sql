-- ============================================================
-- Database Reset
-- Clears all tables before regenerating synthetic data.
-- ============================================================

USE plg_analytics;

SET FOREIGN_KEY_CHECKS = 0;


TRUNCATE TABLE fact_cohort_data;
TRUNCATE TABLE fact_ab_tests;
TRUNCATE TABLE fact_user_events;
TRUNCATE TABLE dim_users;

SET FOREIGN_KEY_CHECKS = 1;

SELECT 'dim_users' AS table_name, COUNT(*) AS row_count FROM dim_users
UNION ALL
SELECT 'fact_user_events', COUNT(*) FROM fact_user_events
UNION ALL
SELECT 'fact_ab_tests', COUNT(*) FROM fact_ab_tests
UNION ALL
SELECT 'fact_cohort_data', COUNT(*) FROM fact_cohort_data;
