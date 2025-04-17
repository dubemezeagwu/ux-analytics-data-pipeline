-- echo "cron.database_name = 'events_db'" >> /var/lib/postgresql/data/postgresql.conf
-- echo "shared_preload_libraries = 'pg_cron'" >> /var/lib/postgresql/data/postgresql.conf

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
    company_id UUID NOT NULL,
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

-- Create indexes for optimization
CREATE INDEX idx_event_timestamp ON user_events (event_timestamp);
CREATE INDEX idx_user_id ON user_events (user_id);
CREATE INDEX idx_session_id ON user_events (session_id);
CREATE INDEX idx_event_type ON user_events (event_type);
CREATE INDEX idx_company_id ON user_events (company_id);

-- Insert dummy company data
INSERT INTO company (company_id, name, address, phone, email, region, subscription_tier, subscription_start_date, subscription_end_date)
VALUES 
    ('e17b9e3a-6b62-4f1a-a1dd-1d96f4c2a5f3', 'Tech Corp', '123 Tech Street, NY', '123-456-7890', 'contact@techcorp.com', 'North America', 'pro', '2024-01-01', '2025-01-01'),
    ('c23a4c5d-7b85-4d2f-bc71-2e97f1e1f4b6', 'Retail World', '45 Market St, London', '555-232-7890', 'support@retailworld.com', 'Europe', 'enterprise', '2023-05-15', '2026-05-15'),
    ('d74f9e5c-5b48-412e-bb49-3c6f4d8e3f74', 'Health Inc.', '99 Wellness Ave, LA', '678-123-4567', 'info@healthinc.com', 'North America', 'basic', '2023-08-20', '2024-08-20'),
    ('a95f1b4c-6d78-49e2-bb82-8d7f2e1d3f94', 'Edu Learn', '300 College Road, Toronto', '416-789-1234', 'hello@edulearn.com', 'Canada', 'free', '2022-11-30', NULL),
    ('f65d9c1e-8e62-48a5-bc2a-5e96e7d4f3b7', 'Finance Solutions', '77 Wall Street, NY', '212-345-6789', 'contact@financesol.com', 'USA', 'pro', '2024-02-01', '2025-02-01');

-- Insert dummy user events data
INSERT INTO user_events (
    event_id, event_timestamp, user_id, session_id, company_id, event_type, page_url, element_selector, element_text, 
    element_type, target_url, last_page_url, user_agent, ip_address, device_type, browser, os, country, city, region, 
    x_coordinate, y_coordinate, session_duration_seconds, metadata
) VALUES 
    (gen_random_uuid(), NOW(), 'user123', 'sessionA', 'e17b9e3a-6b62-4f1a-a1dd-1d96f4c2a5f3', 'click', '/home', '#login-btn', 'Login', 'button', '/dashboard', '/home', 
     'Mozilla/5.0', '192.168.1.1', 'Desktop', 'Chrome', 'Windows', 'USA', 'New York', 'North America', 300, 400, 180, '{"referrer": "google.com"}'),

    (gen_random_uuid(), NOW(), 'user456', 'sessionB', 'c23a4c5d-7b85-4d2f-bc71-2e97f1e1f4b6', 'scroll', '/products', '#product-list', NULL, 'div', NULL, '/home',
     'Mozilla/5.0', '192.168.1.2', 'Mobile', 'Safari', 'iOS', 'UK', 'London', 'Europe', 200, 500, 120, '{"session_type": "guest"}'),

    (gen_random_uuid(), NOW(), 'user789', 'sessionC', 'd74f9e5c-5b48-412e-bb49-3c6f4d8e3f74', 'page_view', '/about', NULL, NULL, NULL, NULL, '/contact',
     'Mozilla/5.0', '192.168.1.3', 'Tablet', 'Firefox', 'Android', 'Canada', 'Toronto', 'Canada', 150, 250, 90, '{}'),

    (gen_random_uuid(), NOW(), 'user321', 'sessionD', 'a95f1b4c-6d78-49e2-bb82-8d7f2e1d3f94', 'form_submit', '/signup', '#signup-form', 'Submit', 'form', NULL, '/home',
     'Mozilla/5.0', '192.168.1.4', 'Desktop', 'Edge', 'Windows', 'Germany', 'Berlin', 'Europe', 400, 450, 300, '{"form_type": "registration"}'),

    (gen_random_uuid(), NOW(), 'user654', 'sessionE', 'f65d9c1e-8e62-48a5-bc2a-5e96e7d4f3b7', 'keydown', '/search', '#search-box', 'Search', 'input', NULL, '/home',
     'Mozilla/5.0', '192.168.1.5', 'Mobile', 'Chrome', 'Android', 'USA', 'San Francisco', 'North America', 500, 600, 150, '{"search_term": "finance"}'),

    (gen_random_uuid(), NOW(), 'user987', 'sessionF', 'e17b9e3a-6b62-4f1a-a1dd-1d96f4c2a5f3', 'hover', '/dashboard', '#settings-icon', NULL, 'icon', NULL, '/home',
     'Mozilla/5.0', '192.168.1.6', 'Desktop', 'Safari', 'MacOS', 'France', 'Paris', 'Europe', 250, 350, 200, '{}');

