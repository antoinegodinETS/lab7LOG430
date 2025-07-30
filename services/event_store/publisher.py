import uuid
from datetime import datetime
import json
import logging

from sqlalchemy.orm import Session
from . import models

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def publish_event(topic: str, event_data: dict, db: Session):
    try:
        event = models.Evenement(
            id=str(uuid.uuid4()),
            type=event_data.get("type"),
            source=event_data.get("source"),
            timestamp=datetime.utcnow(),
            payload=json.dumps(event_data.get("payload"))
        )
        db.add(event)
        db.commit()
        logger.info(f"[EVENT STORE] Événement enregistré dans {topic} : {event.type}")
    except Exception as e:
        db.rollback()
        logger.error(f"[EVENT STORE] Erreur lors de l’enregistrement de l’événement : {e}")
