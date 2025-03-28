import requests
import json
import uuid
import random
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

API_URL = "http://localhost:5000/send_event"

PAGES = [
    "https://example.com/home",
    "https://example.com/products",
    "https://example.com/cart",
    "https://example.com/checkout",
    "https://example.com/blog"
]

ELEMENTS = [
    {"selector": "#button1", "text": "Add to Cart", "type": "button"},
    {"selector": "#link1", "text": "View Details", "type": "link"},
    {"selector": "#input-email", "text": "", "type": "input"},
    {"selector": "#form-checkout", "text": "Checkout", "type": "form"},
    {"selector": "#search-bar", "text": "", "type": "input"},
    {"selector": "#dropdown-menu", "text": "Sort by Price", "type": "dropdown"},
]

EVENT_TYPES = ["page_view", "click", "scroll", "form_submit", "hover", "keydown"]

USER_IDS = [str(i) for i in range(1, 10000)]  # 10,000 users
COMPANY_NAMES = ["TechCorp", "RetailX", "FinanceHub", "EduPlus", "HealthSync"]
SUBSCRIPTION_TIERS = ["free", "basic", "pro", "enterprise"]
REGIONS = ["North America", "Europe", "Asia", "Australia"]

ACTUAL_COMPANY_IDS = [
    "e17b9e3a-6b62-4f1a-a1dd-1d96f4c2a5f3",
    "c23a4c5d-7b85-4d2f-bc71-2e97f1e1f4b6",
    "d74f9e5c-5b48-412e-bb49-3c6f4d8e3f74",
    "a95f1b4c-6d78-49e2-bb82-8d7f2e1d3f94",
    "f65d9c1e-8e62-48a5-bc2a-5e96e7d4f3b7",
]

COMPANY_IDS = {user_id: random.choice(ACTUAL_COMPANY_IDS) for user_id in USER_IDS}
COMPANIES = {
    company_id: {
        "name": random.choice(COMPANY_NAMES),
        "subscription_tier": random.choice(SUBSCRIPTION_TIERS),
        "region": random.choice(REGIONS),
    }
    for company_id in COMPANY_IDS.values()
}

USER_COMPANIES = {user_id: COMPANY_IDS[user_id] for user_id in USER_IDS}

START_DATE = datetime(2025, 2, 1)
END_DATE = datetime(2025, 3, 31)
TOTAL_EVENTS = 100000


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


def process_events(event_queue):
    current_date = START_DATE
    events_generated = 0

    while current_date <= END_DATE and events_generated < TOTAL_EVENTS:
        daily_users = random.sample(USER_IDS, k=random.randint(1, 25))  # Pick a random set of active users per day
        print(f"Generating events for {current_date.strftime('%Y-%m-%d')} with {len(daily_users)} users...")

        for user_id in daily_users:
            session_id = str(uuid.uuid4())
            session_start = current_date.replace(hour=8, minute=0, second=0)  # Start session at 8 AM

            for _ in range(random.randint(5, 15)):  # Generate 5-15 events per session
                event_time = session_start + timedelta(seconds=random.randint(60, 3600))  # Within the hour
                event = generate_random_event(user_id, session_id, event_time)
                event_queue.put(event)  # Add event to queue
                events_generated += 1

                if events_generated >= TOTAL_EVENTS:
                    return
        
        current_date += timedelta(days=1)  # Move to the next day


def event_sender_worker(event_queue):
    while True:
        event_data = event_queue.get()
        if event_data is None:
            break
        send_event(event_data)
        event_queue.task_done()


if __name__ == "__main__":
    event_queue = Queue()
    with ThreadPoolExecutor(max_workers=500) as executor:
        executor.submit(process_events, event_queue)
        for _ in range(500):
            executor.submit(event_sender_worker, event_queue)

        event_queue.join()
