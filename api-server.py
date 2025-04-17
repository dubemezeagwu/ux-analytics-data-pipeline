import json
import time
import uuid
import threading
import kafka
import asyncpg
from flask import Flask, request, jsonify
import asyncio

app = Flask(__name__)

# Kafka producer
producer = kafka.KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = "user_events"

# In-memory set to store company IDs
company_set = set()

# PostgreSQL connection details
DB_CONFIG = {
    "user": "admin",
    "password": "admin",
    "database": "events_db",
    "host": "localhost",
    "port": 5432
}

# Function to refresh company_set every 5 minutes
async def refresh_company_set():
    global company_set
    while True:
        try:
            conn = await asyncpg.connect(**DB_CONFIG)
            rows = await conn.fetch("SELECT company_id FROM company")
            await conn.close()
            
            company_set = {str(row["company_id"]) for row in rows}
            print(f"Updated company_set with {len(company_set)} companies.")
        except Exception as e:
            print(f"Error updating company_set: {e}")
        
        time.sleep(300)  # Refresh every 5 minutes

# Start background thread to update company_set
threading.Thread(target=lambda: asyncio.run(refresh_company_set()), daemon=True).start()

@app.route("/send_event", methods=["POST"])
def send_event():
    data = request.json
    required_fields = {"user_id", "session_id", "event_type", "page_url"}
    allowed_event_types = {"page_view", "click", "scroll", "form_submit", "hover", "keydown"}
    
    # Validate required fields
    if not data or not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400
    
    if data["event_type"] not in allowed_event_types:
        return jsonify({"error": "Invalid event type"}), 400
    
    # Validate company_id
    company_id = data.get("company_id")
    if company_id and company_id not in company_set:
        return jsonify({"error": "Company not found ", "company_id": company_id}), 403  # Drop event if company is not in DB
    
    event = {
        "event_id": str(uuid.uuid4()),
        "event_timestamp": data["event_timestamp"],
        "user_id": data["user_id"],
        "session_id": data["session_id"],
        "company_id": company_id,
        "event_type": data["event_type"],
        "page_url": data["page_url"],
        "element_selector": data.get("element_selector"),
        "element_text": data.get("element_text"),
        "element_type": data.get("element_type"),
        "target_url": data.get("target_url"),
        "last_page_url": data.get("last_page_url"),
        "user_agent": request.headers.get("User-Agent"),
        "ip_address": request.remote_addr,
        "device_type": data.get("device_type", "desktop"),
        "browser": data.get("browser"),
        "os": data.get("os"),
        "country": data.get("country"),
        "city": data.get("city"),
        "region": data.get("region"),
        "x_coordinate": data.get("x_coordinate"),
        "y_coordinate": data.get("y_coordinate"),
        "session_duration_seconds": data.get("session_duration_seconds", 0),
        "metadata": data.get("metadata", {})
    }
    
    producer.send(topic, event)
    print(f"Produced: {event}")
    return jsonify({"message": "Event sent successfully"}), 200

if __name__ == "__main__":
    print(f"Listening for events on /send_event and sending to topic: {topic}")
    app.run(host="0.0.0.0", port=5000, debug=True)
