import os
import httpx
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
import time
from prometheus_client import Counter, Histogram
import logging
import json


instrumentator = Instrumentator()
app = FastAPI()
instrumentator.instrument(app).expose(app)

# Enregistre des métriques personnalisées
saga_success_counter = Counter("saga_success_total", "Nombre de sagas réussies")
saga_failure_counter = Counter("saga_failure_total", "Nombre de sagas échouées")
saga_duration_histogram = Histogram("saga_duration_seconds", "Durée des sagas")
etat_counter = Counter("saga_etat_total", "Étapes atteintes par les sagas", ["etat"])

logger = logging.getLogger("uvicorn")

def log_event(event: str, extra: dict = {}):
    logger.info(json.dumps({"event": event, **extra}))

SERVICES = {
    "stock": "http://stock:8000",
    "paiement": "http://paiement:8000",
    "commande": "http://commande:8000"
}

@app.get("/health")
def health():
    return {"status": "orchestrateur ok"}


@app.post("/saga/commande/")
async def lancer_saga(cmd: dict):
    start_time = time.time()
    produits = cmd["produits"]

    async with httpx.AsyncClient() as client:
        try:
            # 1. Calcul du montant total
            r = await client.post(
                f"{SERVICES['stock']}/stock/prix",
                json={"produits": produits}
            )
            if r.status_code != 200:
                saga_failure_counter.inc()
                return {"status": "échec", "message": "Erreur de calcul du prix."}
            montant = r.json()["montant_total"]

            # 2. Création de la commande
            r = await client.post(
                f"{SERVICES['commande']}/commande/",
                json={"client_id": 1}
            )
            if r.status_code != 200:
                saga_failure_counter.inc()
                raise HTTPException(status_code=400, detail="Erreur lors de la création de la commande")

            order_id = str(r.json()["id"])
            await client.post(f"{SERVICES['commande']}/commande/{order_id}/etat", json={"etat": "CREEE"})
            etat_counter.labels("CREEE").inc()
            log_event("Commande créée", {"order_id": order_id})

            # 3. Vérification du stock
            r = await client.post(
                f"{SERVICES['stock']}/stock/verifier",
                json={"id": order_id, "produits": produits}
            )
            if r.status_code != 200:
                await client.post(f"{SERVICES['commande']}/commande/{order_id}/etat", json={"etat": "ANNULEE"})
                saga_failure_counter.inc()
                return {"status": "échec", "message": "Stock insuffisant."}

            await client.post(f"{SERVICES['commande']}/commande/{order_id}/etat", json={"etat": "STOCK_VERIFIE"})
            etat_counter.labels("STOCK_VERIFIE").inc()
            log_event("Stock vérifié", {"order_id": order_id})

            # 4. Réservation du stock
            r = await client.post(
                f"{SERVICES['stock']}/stock/reserver",
                json={"id": order_id, "produits": produits}
            )
            if r.status_code != 200:
                await client.post(f"{SERVICES['commande']}/commande/{order_id}/etat", json={"etat": "ANNULEE"})
                saga_failure_counter.inc()
                return {"status": "échec", "message": "Erreur de réservation du stock."}

            await client.post(f"{SERVICES['commande']}/commande/{order_id}/etat", json={"etat": "STOCK_RESERVE"})
            etat_counter.labels("STOCK_RESERVE").inc()
            log_event("Stock réservé", {"order_id": order_id})

            # 5. Paiement
            r = await client.post(
                f"{SERVICES['paiement']}/paiement",
                json={"id": order_id, "montant": montant}
            )
            if r.status_code != 200:
                await client.post(f"{SERVICES['stock']}/stock/liberer", json={"id": order_id, "produits": produits})
                await client.post(f"{SERVICES['commande']}/commande/{order_id}/etat", json={"etat": "ANNULEE"})
                saga_failure_counter.inc()
                return {"status": "échec", "message": "Paiement échoué."}

            await client.post(f"{SERVICES['commande']}/commande/{order_id}/etat", json={"etat": "PAYEE"})
            etat_counter.labels("PAYEE").inc()
            log_event("Paiement effectué", {"order_id": order_id})

            # 6. Confirmation de la commande
            r = await client.post(
                f"{SERVICES['commande']}/commande/{order_id}/etat",
                json={"etat": "CONFIRMEE"}
            )
            if r.status_code != 200:
                await client.post(f"{SERVICES['stock']}/stock/liberer", json={"id": order_id, "produits": produits})
                await client.post(f"{SERVICES['commande']}/commande/{order_id}/etat", json={"etat": "ANNULEE"})
                saga_failure_counter.inc()
                return {"status": "échec", "message": "Impossible de confirmer la commande."}

            etat_counter.labels("CONFIRMEE").inc()
            saga_success_counter.inc()
            log_event("Commande confirmée", {"order_id": order_id})

            return {"status": "ok", "commande_id": order_id}

        finally:
            saga_duration_histogram.observe(time.time() - start_time)
