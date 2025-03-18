import kafka
import json
import time
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

producer = kafka.KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = "user_events"

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
    
    # Construct event object with new schema
    event = {
        "event_id": str(uuid.uuid4()),  # Generate new event ID
        "event_timestamp": int(time.time()),  # Current Unix timestamp
        "user_id": data["user_id"],
        "session_id": data["session_id"],
        "company_id": data.get("company_id", None),  # Optional field
        "event_type": data["event_type"],
        "page_url": data["page_url"],
        "element_selector": data.get("element_selector"),
        "element_text": data.get("element_text"),
        "element_type": data.get("element_type"),
        "target_url": data.get("target_url"),
        "last_page_url": data.get("last_page_url"),
        "user_agent": request.headers.get("User-Agent"),
        "ip_address": request.remote_addr,
        "device_type": data.get("device_type", "desktop"),  # Default to "desktop" if not provided
        "browser": data.get("browser"),
        "os": data.get("os"),
        "country": data.get("country"),
        "city": data.get("city"),
        "region": data.get("region"),
        "x_coordinate": data.get("x_coordinate"),
        "y_coordinate": data.get("y_coordinate"),
        "session_duration_seconds": data.get("session_duration_seconds", 0),  # Default to 0 if not provided
        "metadata": data.get("metadata", {})  # Store as an empty dict if not provided
    }
    
    # Send event to Kafka
    producer.send(topic, event)
    print(f"Produced: {event}")
    return jsonify({"message": "Event sent successfully"}), 200

if __name__ == "__main__":
    print(f"Listening for events on /send_event and sending to topic: {topic}")
    app.run(host="0.0.0.0", port=5000, debug=True)
