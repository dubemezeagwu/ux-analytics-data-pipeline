import kafka
import json
import psycopg2
import uuid
from datetime import datetime

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="events_db",
    user="admin",
    password="admin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Initialize Kafka Consumer
consumer = kafka.KafkaConsumer(
    'user_events',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id="event_group"
)

print("Consumer started... Listening for messages")

for message in consumer:
    event = message.value
    print(f"Consumed: {event}")

    # Ensure required fields exist
    required_fields = [
        "event_id", "event_timestamp", "user_id", "session_id", "event_type",
        "page_url", "element_selector", "element_text", "element_type",
        "target_url", "last_page_url", "user_agent", "ip_address",
        "x_coordinate", "y_coordinate", "company_id", "device_type",
        "browser", "os", "country", "city", "region", "session_duration_seconds", "metadata"
    ]
    
    # if not all(field in event for field in required_fields):
    #     print("Skipping event due to missing fields:", event)
    #     continue

    # Convert timestamp to PostgreSQL-friendly format
    event_timestamp = datetime.utcfromtimestamp(event["event_timestamp"])

    try:
        cursor.execute(
            """
            INSERT INTO user_events (
                event_id, event_timestamp, user_id, session_id, company_id, event_type,
                page_url, element_selector, element_text, element_type,
                target_url, last_page_url, user_agent, ip_address,
                device_type, browser, os, country, city, region, 
                x_coordinate, y_coordinate, session_duration_seconds, metadata
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                str(event["event_id"]),   # Convert UUID to string
                event_timestamp,
                str(event["user_id"]),
                str(event["session_id"]),
                str(event["company_id"]),  # Ensure company_id is UUID as string
                event["event_type"],
                event["page_url"],
                event["element_selector"],
                event["element_text"],
                event["element_type"],
                event["target_url"],
                event["last_page_url"],
                event["user_agent"],
                event["ip_address"],
                event["device_type"],
                event["browser"],
                event["os"],
                event["country"],
                event["city"],
                event["region"],
                int(event["x_coordinate"]),
                int(event["y_coordinate"]),
                int(event["session_duration_seconds"]),
                json.dumps(event["metadata"])  # Storing the metadata as JSON
            )
        )
        conn.commit()
        print("✅ Event inserted into database successfully.")
    
    except Exception as e:
        conn.rollback()
        print("❌ Database insert error:", str(e))

# Close the database connection when the script terminates
cursor.close()
conn.close()
