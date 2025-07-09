from fastapi import FastAPI, Depends, HTTPException
from schemas import EtatPayload
from sqlalchemy.orm import Session
import models
import schemas
import crud
import database
from prometheus_fastapi_instrumentator import Instrumentator




app = FastAPI()
Instrumentator().instrument(app).expose(app)

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/commande/", response_model=schemas.CommandeOut)
def creer_commande(commande: schemas.CommandeCreate, db: Session = Depends(get_db)):
    return crud.valider_commande(db, commande)

@app.get("/commande/{commande_id}", response_model=schemas.CommandeOut)
def lire_commande(commande_id: int, db: Session = Depends(get_db)):
    commande = crud.get_commande(db, commande_id)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande


@app.post("/commande/{id}/etat")
def update_state(id: int, payload: EtatPayload, db: Session = Depends(get_db)):
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