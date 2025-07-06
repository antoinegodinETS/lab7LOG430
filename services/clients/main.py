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

@app.post("/clients", response_model=schemas.ClientOut)
def create(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    print(f"Requête reçue pour créer un client : {client}")
    created_client = crud.create_client(db, client)
    print(f"Client créé avec succès : {created_client}")
    return created_client

@app.get("/clients", response_model=list[schemas.ClientOut])
def read_all(db: Session = Depends(get_db)):
    clients = crud.get_clients(db)
    print(">> Clients récupérés:", clients)
    return clients  # Retourne directement la liste des clients

