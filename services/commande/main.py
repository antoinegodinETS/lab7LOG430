from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator
from uuid import uuid4
from datetime import datetime
import json
from kafka import KafkaProducer

import models
import schemas
import crud
import database

# 👇 Import du modèle Evenement défini dans event_store/models.py
from services.event_store.models import Evenement
from services.event_store.publisher import publish_event


app = FastAPI()
Instrumentator().instrument(app).expose(app)

models.Base.metadata.create_all(bind=database.engine)

def get_producer():
    return KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/commande/", response_model=schemas.CommandeOut)
def creer_commande(commande: schemas.CommandeCreate, db: Session = Depends(get_db)):
    created = crud.valider_commande(db, commande)

    event = {
        "id": str(uuid4()),
        "type": "CommandeCreee",
        "source": "commande",
        "timestamp": datetime.utcnow().isoformat(),
        "payload": {
            "commande_id": created.id,
            "produits": [p.dict() for p in commande.produits]
        }
    }

    # Publier l'événement dans Kafka
    producer = get_producer()
    producer.send("commande.events", event)
    producer.flush()

    return created



@app.get("/commande/{commande_id}", response_model=schemas.CommandeOut)
def lire_commande(commande_id: int, db: Session = Depends(get_db)):
    commande = crud.get_commande(db, commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande

@app.post("/commande/{id}/etat")
def update_state(id: int, payload: schemas.EtatPayload, db: Session = Depends(get_db)):
    cmd = crud.get_commande(db, id)
    if not cmd:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    cmd.statut = payload.etat
    db.commit()
    db.refresh(cmd)
    return {"id": id, "etat": cmd.statut}

@app.get("/health")
def health():
    return {"status": "commande ok"}
