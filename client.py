import requests
import json
import uuid
import random
import time

API_URL = "http://localhost:5000/send_event"

# Sample pages and elements
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
]

EVENT_TYPES = ["page_view", "click", "scroll", "form_submit", "hover", "keydown"]

def generate_random_event():
    user_id = str(random.randint(1, 5))
    session_id = str(uuid.uuid4())  # New session per event
    event_type = random.choice(EVENT_TYPES)
    page_url = random.choice(PAGES)
    element = random.choice(ELEMENTS)
    
    # Simulate additional fields
    device_type = random.choice(["Mobile", "Tablet", "Desktop"])
    browser = random.choice(["Chrome", "Firefox", "Safari", "Edge"])
    os = random.choice(["Windows", "Mac OS", "iOS", "Android"])
    country = random.choice(["USA", "India", "Germany", "Brazil", "UK"])
    city = random.choice(["New York", "London", "Berlin", "Mumbai", "Sydney"])
    region = random.choice(["North America", "Europe", "Asia", "Australia"])

    # Generate the event payload based on the schema
    event_data = {
        "event_id": str(uuid.uuid4()),
        "event_timestamp": int(time.time()),  # Event timestamp in seconds
        "user_id": user_id,
        "session_id": session_id,
        "company_id": "new_company1",  # Generate a random company_id
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
        "x_coordinate": random.randint(0, 1920) if event_type in ["click", "hover"] else 0,
        "y_coordinate": random.randint(0, 1080) if event_type in ["click", "hover"] else 0,
        "session_duration_seconds": random.randint(60, 1800),  # Random session duration
        "metadata": json.dumps({"custom_data": "value"})  # Example custom data
    }

    # Additional event-specific data
    if event_type == "scroll":
        event_data["scroll_depth"] = random.randint(10, 100)  # Scroll depth in percentage
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

if __name__ == "__main__":
    for _ in range(50):  # Generate 50 events
        event = generate_random_event()
        send_event(event)
        time.sleep(random.uniform(0.5, 0.6))  # Simulating real user activity delays
