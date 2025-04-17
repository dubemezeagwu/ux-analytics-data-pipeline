-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Create company table
CREATE TABLE company (
    company_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255) UNIQUE,
    region VARCHAR(100),
    subscription_tier VARCHAR(50) CHECK (subscription_tier IN ('free', 'basic', 'pro', 'enterprise')),
    subscription_start_date TIMESTAMP DEFAULT NOW(),
    subscription_end_date TIMESTAMP
);



-- Create user_events table
CREATE TABLE user_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    user_id VARCHAR(50) NOT NULL,
    session_id VARCHAR(50) NOT NULL,
    company_id UUID NOT NULL REFERENCES company(company_id),
    event_type VARCHAR(50) NOT NULL CHECK (
        event_type IN ('page_view', 'click', 'scroll', 'form_submit', 'hover', 'keydown')
    ),
    page_url TEXT NOT NULL,
    element_selector TEXT,  
    element_text TEXT,
    element_type VARCHAR(50),
    target_url TEXT,
    last_page_url TEXT,
    user_agent TEXT,
    ip_address VARCHAR(45),
    device_type VARCHAR(50),  -- Mobile, Tablet, Desktop
    browser VARCHAR(50),
    os VARCHAR(50),
    country VARCHAR(100),
    city VARCHAR(100),
    region VARCHAR(100),
    x_coordinate INT,
    y_coordinate INT,
    session_duration_seconds INT,  -- Time spent in the session
    metadata JSONB  -- Custom event properties
);

-- Indexes for better performance
CREATE INDEX idx_event_timestamp ON user_events (event_timestamp);
CREATE INDEX idx_user_id ON user_events (user_id);
CREATE INDEX idx_session_id ON user_events (session_id);
CREATE INDEX idx_event_type ON user_events (event_type);
CREATE INDEX idx_company_id ON user_events (company_id);

-- Unlogged table for high-speed inserts
CREATE UNLOGGED TABLE user_events_unlogged (LIKE user_events INCLUDING ALL);

-- Materialized view: User activity aggregation
CREATE MATERIALIZED VIEW mv_user_activity AS
SELECT 
    company_id,
    user_id,
    COUNT(*) AS total_events,
    COUNT(DISTINCT session_id) AS unique_sessions,
    COUNT(CASE WHEN event_type = 'click' THEN 1 END) AS total_clicks,
    COUNT(CASE WHEN event_type = 'page_view' THEN 1 END) AS total_page_views,
    MAX(event_timestamp) AS last_activity_timestamp
FROM user_events
WHERE event_timestamp >= NOW() - INTERVAL '1 hour'
GROUP BY company_id, user_id;

-- Materialized view: Daily event summary
CREATE MATERIALIZED VIEW mv_daily_event_summary AS
SELECT 
    DATE(event_timestamp) AS event_date,
    company_id,
    event_type,
    COUNT(*) AS event_count
FROM user_events
WHERE event_timestamp >= NOW() - INTERVAL '1 day'
GROUP BY event_date, company_id, event_type;

-- Background job: Refresh views every 10 minutes
SELECT cron.schedule('*/10 * * * *', $$ 
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_user_activity;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_event_summary;
$$);

-- Function to bulk move unlogged data to main table
CREATE OR REPLACE FUNCTION move_unlogged_data() RETURNS void AS $$
BEGIN
    INSERT INTO user_events SELECT * FROM user_events_unlogged;
    TRUNCATE TABLE user_events_unlogged;
END;
$$ LANGUAGE plpgsql;

-- Schedule the unlogged data move every 10 minutes
SELECT cron.schedule('*/10 * * * *', 'SELECT move_unlogged_data();');
