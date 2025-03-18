-- psql -h localhost -d events_db -U admin


CREATE TABLE user_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    user_id VARCHAR(50) NOT NULL,
    session_id VARCHAR(50) NOT NULL,
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
    x_coordinate INT,
    y_coordinate INT
);

-- Create indexes separately
CREATE INDEX idx_event_timestamp ON user_events (event_timestamp);
CREATE INDEX idx_user_id ON user_events (user_id);
CREATE INDEX idx_session_id ON user_events (session_id);
CREATE INDEX idx_event_type ON user_events (event_type);


1. Total Number of Events by Event Type
This metric shows the distribution of different event types (e.g., page views, clicks, scrolls, etc.).

SELECT event_type, COUNT(*) AS total_events
FROM user_events
GROUP BY event_type
ORDER BY total_events DESC;
2. Average Time Spent Per Page
To calculate the average time a user spends on each page, you can consider the difference between consecutive page_view events for the same session. This assumes a page_view event is logged when the user enters and exits a page.

WITH page_times AS (
    SELECT 
        user_id, 
        session_id, 
        page_url, 
        event_timestamp,
        LEAD(event_timestamp) OVER (PARTITION BY user_id, session_id ORDER BY event_timestamp) AS next_event_timestamp
    FROM user_events
    WHERE event_type = 'page_view'
)
SELECT 
    page_url,
    AVG(EXTRACT(EPOCH FROM (next_event_timestamp - event_timestamp))) AS avg_time_spent_seconds
FROM page_times
WHERE next_event_timestamp IS NOT NULL
GROUP BY page_url
ORDER BY avg_time_spent_seconds DESC;
3. Clicks per Page
You can query the total number of clicks per page to measure user engagement.

SELECT page_url, COUNT(*) AS total_clicks
FROM user_events
WHERE event_type = 'click'
GROUP BY page_url
ORDER BY total_clicks DESC;
4. Scroll Depth by Page
If scroll events include the y_coordinate data, you can estimate scroll depth to understand how far users are scrolling on pages.

SELECT page_url, AVG(y_coordinate) AS avg_scroll_depth
FROM user_events
WHERE event_type = 'scroll' AND y_coordinate IS NOT NULL
GROUP BY page_url
ORDER BY avg_scroll_depth DESC;
5. Form Submissions per Page
This query counts how many form submissions occurred on each page.

SELECT page_url, COUNT(*) AS total_form_submissions
FROM user_events
WHERE event_type = 'form_submit'
GROUP BY page_url
ORDER BY total_form_submissions DESC;
6. Hover Events per Page
This query shows how many times users hovered over elements on each page.

SELECT page_url, COUNT(*) AS total_hovers
FROM user_events
WHERE event_type = 'hover'
GROUP BY page_url
ORDER BY total_hovers DESC;
7. Keydown Events per Page
You can track the number of keyboard interactions on each page.

SELECT page_url, COUNT(*) AS total_keydowns
FROM user_events
WHERE event_type = 'keydown'
GROUP BY page_url
ORDER BY total_keydowns DESC;
8. Unique Users per Page
You can calculate the number of unique users interacting with each page.

SELECT page_url, COUNT(DISTINCT user_id) AS unique_users
FROM user_events
GROUP BY page_url
ORDER BY unique_users DESC;
9. Page Views per User
This query counts how many pages each user visited, which can help assess user activity.

SELECT user_id, COUNT(DISTINCT page_url) AS pages_visited
FROM user_events
WHERE event_type = 'page_view'
GROUP BY user_id
ORDER BY pages_visited DESC;
10. Session Duration
This query calculates the total duration of user sessions by considering the time between the first and last event in a session.

WITH session_times AS (
    SELECT 
        user_id, 
        session_id, 
        MIN(event_timestamp) AS session_start,
        MAX(event_timestamp) AS session_end
    FROM user_events
    GROUP BY user_id, session_id
)
SELECT 
    user_id, 
    session_id,
    EXTRACT(EPOCH FROM (session_end - session_start)) AS session_duration_seconds
FROM session_times
ORDER BY session_duration_seconds DESC;
11. User Engagement by Event Type
This metric can measure how engaged users are by the number of interactions (clicks, hovers, form submissions, etc.) per session.

SELECT 
    user_id, 
    session_id,
    COUNT(*) AS total_events
FROM user_events
WHERE event_type IN ('click', 'hover', 'form_submit', 'keydown')
GROUP BY user_id, session_id
ORDER BY total_events DESC;

These queries provide insights into different aspects of user behavior and help evaluate the overall user experience on the platform.
