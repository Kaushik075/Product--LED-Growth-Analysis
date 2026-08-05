-- ============================================================
-- PLG Funnel Analysis - Database Setup
-- Creates the complete database schema for a fresh installation.
-- ============================================================
-- Create Database
CREATE DATABASE IF NOT EXISTS plg_analytics;
USE plg_analytics;

-- DIMENSION TABLES
-- Users (Account-level data)
CREATE TABLE IF NOT EXISTS dim_users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    company_name VARCHAR(255),
    user_segment VARCHAR(50),
    signup_date DATE NOT NULL,
    country VARCHAR(100),
    device_type VARCHAR(50),
    platform VARCHAR(50),
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Funnel Stage Dimension
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

-- FACT TABLES
-- User Events (Step-by-step user journey)
CREATE TABLE IF NOT EXISTS fact_user_events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    event_type VARCHAR(100),
    event_timestamp DATETIME NOT NULL,
    event_value DECIMAL(10, 2),
    metadata JSON,
    FOREIGN KEY (user_id) REFERENCES dim_users(user_id),
    INDEX idx_user_event (user_id, event_timestamp)
);

-- A/B Test Assignments
CREATE TABLE IF NOT EXISTS fact_ab_tests (
    ab_test_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    test_name VARCHAR(100),
    variant VARCHAR(50),
    test_start_date DATE NOT NULL,
    test_end_date DATE,
    converted BOOLEAN DEFAULT FALSE,
    conversion_timestamp DATETIME,
    FOREIGN KEY (user_id) REFERENCES dim_users(user_id),
    INDEX idx_user_test (user_id, test_name)
);

-- Cohort Analysis Table
CREATE TABLE IF NOT EXISTS fact_cohort_data (
    cohort_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    cohort_date DATE,
    signup_date DATE,
    activation_date DATE,
    feature_adoption_date DATE,
    pql_date DATE,
    payment_date DATE,
    days_to_activation INT,
    days_to_pql INT,
    days_to_payment INT,
    FOREIGN KEY (user_id) REFERENCES dim_users(user_id)
);

SHOW TABLES;

USE plg_analytics;
SHOW TABLES;
DESC dim_users;

USE plg_analytics;

SELECT COUNT(*) as total_users FROM dim_users;
SELECT COUNT(*) as total_events FROM fact_user_events;
SELECT COUNT(*) as total_ab_tests FROM fact_ab_tests;
SELECT COUNT(*) as total_cohorts FROM fact_cohort_data;


