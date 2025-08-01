from event_store.consumer import start_consumer
from event_store.publisher import publish_event
from event_store.event import Event
from event_store.database import SessionLocal

import requests
from prometheus_client import Counter
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

import uvicorn

# --- Application FastAPI pour exposer /metrics et /health ---
app = FastAPI()

Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    return {"status": "paiement ok"}

# --- Saga Metrics ---
saga_started = Counter("saga_started_total", "Nombre de sagas démarrées")
saga_success = Counter("saga_success_total", "Nombre de sagas réussies")
saga_failed = Counter("saga_failed_total", "Nombre de sagas échouées")

# --- Paramètres métier ---
SEUIL_MAX = 500

# --- Handler Kafka ---
def handle_stock(event):
    if event["type"] != "StockReserve":
        return

    saga_started.inc()

    commande_id = event["payload"]["commande_id"]
    produits = event["payload"]["produits"]

    try:
        # Appeler l’API du service stock pour connaître le prix total
        r = requests.post("http://stock:8000/stock/prix", json={"id": commande_id, "produits": produits})
        r.raise_for_status()
        montant = r.json()["montant_total"]

        with SessionLocal() as db:
            if montant > SEUIL_MAX:
                saga_failed.inc()
                publish_event("paiement.events", Event.build("PaiementRefuse", "paiement", {"commande_id": commande_id}), db)
            else:
                saga_success.inc()
                publish_event("paiement.events", Event.build("PaiementEffectue", "paiement", {"commande_id": commande_id}), db)

    except Exception as e:
        saga_failed.inc()
        print(f"Erreur dans paiement: {e}")

# --- Lancer l'application API + Kafka ---
if __name__ == "__main__":
    import threading

    # Lancer le consumer Kafka en arrière-plan
    t = threading.Thread(target=start_consumer, args=("stock.events", handle_stock))
    t.daemon = True
    t.start()

    # Lancer FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)
