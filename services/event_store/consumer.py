from kafka import KafkaConsumer
import json
from sqlalchemy.orm import Session
import models
import database
from datetime import datetime

models.Base.metadata.create_all(bind=database.engine)

def start_consumer(topic: str, handler):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers="kafka:9092",
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset="earliest",
        group_id="event_store_group"
    )
    print(f"[CONSUMER] Listening to {topic}")
    for message in consumer:
        print(f"[CONSUMER] Received event on {topic}")
        handler(message.value)

def handle_event(event: dict):
    db: Session = database.SessionLocal()
    try:
        db_event = models.Evenement(
            id=event["id"],
            type=event["type"],
            source=event["source"],
            timestamp=datetime.fromisoformat(event["timestamp"]),
            payload=json.dumps(event["payload"])
        )
        db.add(db_event)
        db.commit()
        print(f"[EVENT_STORE] Event {event['type']} stored.")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed to store event: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    start_consumer("commande.events", handle_event)
    start_consumer("stock.events", handle_event)
    start_consumer("paiement.events", handle_event)
