USE plg_analytics;

-- ============================================================
-- MIGRATION 01
-- Add Funnel Stage Dimension
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_funnel_stage (
    stage_id INT AUTO_INCREMENT PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL UNIQUE,
    stage_label VARCHAR(100) NOT NULL,
    sort_order INT NOT NULL
);

INSERT IGNORE INTO dim_funnel_stage (
    event_type,
    stage_label,
    sort_order
)
VALUES
('signup', 'Signup', 1),
('activation', 'Activation', 2),
('feature_adoption', 'Feature Adoption', 3),
('pql_qualified', 'PQL Qualified', 4),
('payment_complete', 'Paid Conversion', 5);

SELECT *
FROM dim_funnel_stage
ORDER BY sort_order;