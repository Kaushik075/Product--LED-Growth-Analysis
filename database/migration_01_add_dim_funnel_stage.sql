USE plg_analytics;

-- ============================================================
-- ============================================================
-- Migration 01
-- Adds dim_funnel_stage for existing databases.
-- Skip this if using database_setup.sql on a new database.
-- ============================================================
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_funnel_stage (
    stage_id INT PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL UNIQUE,
    stage_label VARCHAR(100) NOT NULL,
    sort_order INT NOT NULL
);

INSERT IGNORE INTO dim_funnel_stage (
    stage_id,
    event_type,
    stage_label,
    sort_order
)
VALUES
(1, 'signup', 'Signup', 1),
(2, 'activation', 'Activation', 2),
(3, 'feature_use', 'Feature Adoption', 3),
(4, 'pql_qualified', 'PQL Qualified', 4),
(5, 'payment_complete', 'Paid Conversion', 5);

SELECT *
FROM dim_funnel_stage
ORDER BY sort_order;