from event_store.consumer import start_consumer
from event_store.publisher import publish_event
from event_store.event import Event
from event_store.database import SessionLocal

import requests

def handle_commande_creee(event):
    if event["type"] != "CommandeCreee":
        return

    commande_id = event["payload"]["commande_id"]
    produits = event["payload"]["produits"]

    try:
        r = requests.post("http://stock:8000/stock/verifier", json={"id": commande_id, "produits": produits})
        r.raise_for_status()

        r = requests.post("http://stock:8000/stock/reserver", json={"id": commande_id, "produits": produits})
        r.raise_for_status()

        with SessionLocal() as db:
            publish_event("stock.events", Event.build("StockReserve", "stock", {"commande_id": commande_id, "produits": produits}), db)

    except Exception:
        with SessionLocal() as db:
            publish_event("stock.events", Event.build("StockInsuffisant", "stock", {"commande_id": commande_id}), db)

if __name__ == "__main__":
    start_consumer("commande.events", handle_commande_creee)
