from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import json

import models
import database
from consumer import start_consumer
from handler import handle_event

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/events/")
def lister_evenements(db: Session = Depends(get_db)):
    evenements = db.query(models.Evenement).order_by(models.Evenement.timestamp).all()
    return [
        {
            "id": e.id,
            "type": e.type,
            "source": e.source,
            "timestamp": e.timestamp,
            "payload": json.loads(e.payload)
        }
        for e in evenements
    ]

@app.get("/health")
def health():
    return {"status": "event_store ok"}

if __name__ == "__main__":
    start_consumer("commande.events", handle_event)