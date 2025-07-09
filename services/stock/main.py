from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

STOCK = {
    "produit_1": {"quantite": 10, "prix": 100},
    "produit_2": {"quantite": 5, "prix": 250}
}


class Produit(BaseModel):
    id: str
    qte: int

class Commande(BaseModel):
    id: Optional[str] = None
    produits: list[Produit]

@app.post("/stock/verifier")
def verifier_stock(cmd: Commande):
    for p in cmd.produits:
        if STOCK.get(p.id) is None or STOCK[p.id]["quantite"] < p.qte:
            raise HTTPException(status_code=400, detail=f"Stock insuffisant pour {p.id}")
    return {"status": "ok"}


@app.post("/stock/reserver")
def reserver_stock(cmd: Commande):
    for p in cmd.produits:
        if STOCK.get(p.id) is None or STOCK[p.id]["quantite"] < p.qte:
            raise HTTPException(status_code=400, detail=f"Stock insuffisant pour {p.id}")
        STOCK[p.id]["quantite"] -= p.qte
    return {"status": "reserve", "stock": STOCK}


@app.post("/stock/liberer")
def liberer_stock(cmd: Commande):
    for p in cmd.produits:
        if p.id in STOCK:
            STOCK[p.id]["quantite"] += p.qte
    return {"status": "libere", "stock": STOCK}

@app.post("/stock/prix")
def calculer_prix_total(cmd: Commande):
    total = 0
    for p in cmd.produits:
        if p.id not in STOCK:
            raise HTTPException(status_code=400, detail=f"Produit inconnu: {p.id}")
        total += p.qte * STOCK[p.id]["prix"]
    return {"montant_total": total}


@app.get("/health")
def health():
    return {"status": "stock ok"}

