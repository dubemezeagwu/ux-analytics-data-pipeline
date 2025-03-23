
-- Event Type Distribution (Pie Chart)
SELECT 
    event_type, 
    COUNT(*) AS event_count
FROM user_events
GROUP BY event_type
ORDER BY event_count DESC;

-- Active Users (Unique Users Per Day) (Line Chart)
SELECT 
    date_trunc('day', event_timestamp) AS event_date,
    COUNT(DISTINCT user_id) AS unique_users
FROM user_events
GROUP BY event_date
ORDER BY event_date;

-- User Engagement by Device Type (Bar Chart)
SELECT 
    device_type, 
    COUNT(*) AS event_count
FROM user_events
GROUP BY device_type
ORDER BY event_count DESC;

-- Total Events Over Time (Time Series Chart)
SELECT
  date_trunc('day', event_timestamp) AS event_date,
  COUNT(*) AS total_events
FROM
  user_events
GROUP BY
  event_date
ORDER BY
  event_date;

-- Conversion Rate (Form Submissions vs Total Events)
SELECT 
    (COUNT(CASE WHEN event_type = 'form_submit' THEN 1 END) * 100.0 / COUNT(*)) AS conversion_rate
FROM user_events;

-- Top Pages by Events (Bar Chart)
SELECT 
    page_url, 
    COUNT(*) AS event_count
FROM user_events
GROUP BY page_url
ORDER BY event_count DESC
LIMIT 10;

-- User Engagement by Country (Map Visualization)
SELECT 
    country, 
    COUNT(*) AS event_count
FROM user_events
GROUP BY country
ORDER BY event_count DESC;

-- Top Browsers Used (Pie Chart)
SELECT 
    browser, 
    COUNT(*) AS browser_usage
FROM user_events
GROUP BY browser
ORDER BY browser_usage DESC;

-- Active Users in the Last 7 Days
SELECT 
    date_trunc('day', event_timestamp) AS event_date,
    COUNT(DISTINCT user_id) AS active_users
FROM user_events
WHERE event_timestamp >= NOW() - INTERVAL '7 days'
GROUP BY event_date
ORDER BY event_date;


DO $$ 
DECLARE 
    r RECORD;
BEGIN 
    FOR r IN (SELECT matviewname FROM pg_matviews) 
    LOOP 
        EXECUTE 'REFRESH MATERIALIZED VIEW ' || r.matviewname;
    END LOOP; 
END $$;
