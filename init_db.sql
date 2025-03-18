CREATE TABLE user_events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    user_id VARCHAR(100),
    event_data JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE heatmap_aggregates (
    id SERIAL PRIMARY KEY,
    page_url TEXT,
    heatmap_data JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_sessions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    session_start TIMESTAMP,
    session_end TIMESTAMP
);
