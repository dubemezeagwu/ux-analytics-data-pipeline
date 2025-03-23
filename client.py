import requests
import json
import uuid
import random
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

API_URL = "http://localhost:5000/send_event"

PAGES = [
    "https://example.com/home",
    "https://example.com/products",
    "https://example.com/cart",
    "https://example.com/checkout",
    "https://example.com/blog"
]

ELEMENTS = [
    {"selector": "#button1", "text": "Submit", "type": "button"},
    {"selector": "#link1", "text": "Read More", "type": "link"},
    {"selector": "#input-email", "text": "", "type": "input"},
    {"selector": "#form-checkout", "text": "Checkout", "type": "form"},
    {"selector": "#search-bar", "text": "", "type": "input"},
    {"selector": "#dropdown-menu", "text": "Select Option", "type": "dropdown"},
]

EVENT_TYPES = ["page_view", "click", "scroll", "form_submit", "hover", "keydown"]

USER_IDS = [str(i) for i in range(1, 1000)]  # 1000 users
COMPANY_NAMES = ["TechCorp", "RetailX", "FinanceHub", "EduPlus", "HealthSync"]
SUBSCRIPTION_TIERS = ["free", "basic", "pro", "enterprise"]
REGIONS = ["North America", "Europe", "Asia", "Australia"]

# Creating company IDs and assigning users to companies
COMPANY_IDS = {user_id: str(uuid.uuid4()) for user_id in USER_IDS}
COMPANIES = {
    company_id: {
        "name": random.choice(COMPANY_NAMES),
        "subscription_tier": random.choice(SUBSCRIPTION_TIERS),
        "region": random.choice(REGIONS),
    }
    for company_id in COMPANY_IDS.values()
}

# Assign each user a company based on their user_id
USER_COMPANIES = {user_id: COMPANY_IDS[user_id] for user_id in USER_IDS}

def generate_random_event(user_id, session_id, timestamp):
    event_type = random.choice(EVENT_TYPES)
    page_url = random.choice(PAGES)
    element = random.choice(ELEMENTS)
    
    device_type = random.choice(["Mobile", "Tablet", "Desktop"])
    browser = random.choice(["Chrome", "Firefox", "Safari", "Edge"])
    os = random.choice(["Windows", "Mac OS", "iOS", "Android"])
    country = random.choice(["USA", "India", "Germany", "Brazil", "UK"])
    city = random.choice(["New York", "London", "Berlin", "Mumbai", "Sydney"])
    region = random.choice(REGIONS)
    company_id = USER_COMPANIES[user_id]

    event_data = {
        "event_id": str(uuid.uuid4()),
        "event_timestamp": int(timestamp.timestamp()),
        "user_id": user_id,
        "session_id": session_id,
        "company_id": company_id,
        "event_type": event_type,
        "page_url": page_url,
        "element_selector": element["selector"] if event_type in ["click", "hover", "keydown"] else None,
        "element_text": element["text"] if event_type in ["click", "hover"] else None,
        "element_type": element["type"] if event_type in ["click", "hover"] else None,
        "target_url": "https://example.com/next" if event_type == "click" else None,
        "last_page_url": random.choice(PAGES) if event_type == "page_view" else None,
        "user_agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X)"
        ]),
        "ip_address": f"192.168.1.{random.randint(1, 255)}",
        "device_type": device_type,
        "browser": browser,
        "os": os,
        "country": country,
        "city": city,
        "region": region,
        "x_coordinate": random.randint(0, 1920) if event_type in ["click", "hover"] else None,
        "y_coordinate": random.randint(0, 1080) if event_type in ["click", "hover"] else None,
        "session_duration_seconds": random.randint(60, 1800),
        "metadata": json.dumps({"custom_data": "value"})
    }

    # Add extra data for specific event types
    if event_type == "scroll":
        event_data["scroll_depth"] = random.randint(10, 100)
    elif event_type == "keydown":
        event_data["key_pressed"] = random.choice(["Enter", "Backspace", "ArrowDown", "Space"])
    elif event_type == "form_submit":
        event_data["form_id"] = element["selector"]
        event_data["form_data"] = json.dumps({"email": "test@example.com", "password": "******"})
    
    return event_data

def send_event(event_data):
    response = requests.post(
        API_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(event_data)
    )
    if response.status_code == 200:
        print("Event sent successfully:", response.json())
    else:
        print("Error sending event:", response.text)

def process_user(user_id):
    for _ in range(10):  # Each user visits 10 times a month
        session_id = str(uuid.uuid4())
        session_start = datetime.utcnow() - timedelta(days=random.randint(1, 30))
        for _ in range(random.randint(5, 15)):  # 5 to 15 events per session
            event_time = session_start + timedelta(seconds=random.randint(1, 600))
            event = generate_random_event(user_id, session_id, event_time)
            send_event(event)
            # time.sleep(random.uniform(0.1, 0.5))  # Optional sleep if needed

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=200) as executor:
        # Execute the function for each user in parallel
        executor.map(process_user, USER_IDS)
