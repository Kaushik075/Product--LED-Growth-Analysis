-- PLG ANALYTICS - DATABASE RESET SCRIPT
-- Run this BEFORE every rerun of plg_data_generator.py
-- Clears all data and resets auto-increment counters, safely, in dependency order.

USE plg_analytics;

SET FOREIGN_KEY_CHECKS = 0;

-- Truncate child tables first (all reference dim_users via user_id),
-- then the parent. Order doesn't strictly matter with FK checks off,
-- but keeping it explicit avoids surprises if checks are ever re-enabled early.
TRUNCATE TABLE fact_cohort_data;
TRUNCATE TABLE fact_ab_tests;
TRUNCATE TABLE fact_user_events;
TRUNCATE TABLE dim_users;

SET FOREIGN_KEY_CHECKS = 1;

-- Verify everything is actually empty before you rerun the generator
SELECT 'dim_users' AS table_name, COUNT(*) AS row_count FROM dim_users
UNION ALL
SELECT 'fact_user_events', COUNT(*) FROM fact_user_events
UNION ALL
SELECT 'fact_ab_tests', COUNT(*) FROM fact_ab_tests
UNION ALL
SELECT 'fact_cohort_data', COUNT(*) FROM fact_cohort_data;
