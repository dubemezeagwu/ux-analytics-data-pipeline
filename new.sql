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

CREATE TABLE user_events (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    user_id VARCHAR(50) NOT NULL,
    session_id VARCHAR(50) NOT NULL,
    company_id VARCHAR(50) NOT NULL,
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

CREATE INDEX idx_event_timestamp ON user_events (event_timestamp);
CREATE INDEX idx_user_id ON user_events (user_id);
CREATE INDEX idx_session_id ON user_events (session_id);
CREATE INDEX idx_event_type ON user_events (event_type);
CREATE INDEX idx_company_id ON user_events (company_id);

