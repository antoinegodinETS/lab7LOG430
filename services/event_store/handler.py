import json
from datetime import datetime
from sqlalchemy.orm import Session

import models
import database

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
        print(f"[EVENT_STORE] Event {event['type']} stored successfully.")
    except Exception as e:
        db.rollback()
        print(f"[EVENT_STORE] Failed to store event: {e}")
    finally:
        db.close()
