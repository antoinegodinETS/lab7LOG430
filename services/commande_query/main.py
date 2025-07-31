from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, CommandeRead
from consumer import start_consumer 
import threading

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/commandes/")
def get_commandes(db: Session = Depends(get_db)):
    return db.query(CommandeRead).all()

@app.get("/health")
def health():
    return {"status": "commande_query ok"}

@app.on_event("startup") 
def start_kafka_consumer():
    threading.Thread(target=start_consumer, daemon=True).start()
