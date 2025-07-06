from fastapi import FastAPI, Depends
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
    return crud.get_commande(db, commande_id)
