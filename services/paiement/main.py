# services/paiement/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PaiementDemande(BaseModel):
    id: str
    montant: float

SEUIL_MAX = 500  # Montant maximum autorisé

@app.post("/paiement")
def effectuer_paiement(paiement: PaiementDemande):
    if paiement.montant > SEUIL_MAX:
        raise HTTPException(
            status_code=400,
            detail=f"Paiement refusé : montant trop élevé ({paiement.montant} > {SEUIL_MAX})"
        )
    return {"status": "paiement accepté", "commande_id": paiement.id}

@app.get("/health")
def health():
    return {"status": "paiement ok"}