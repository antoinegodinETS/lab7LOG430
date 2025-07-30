from event_store.consumer import start_consumer
from event_store.publisher import publish_event
from event_store.event import Event
from event_store.database import SessionLocal

import requests

SEUIL_MAX = 500

def handle_stock(event):
    if event["type"] != "StockReserve":
        return

    commande_id = event["payload"]["commande_id"]
    produits = event["payload"]["produits"]

    # Appeler l’API pour calculer le montant
    r = requests.post("http://stock:8000/stock/prix", json={"id": commande_id, "produits": produits})
    montant = r.json()["montant_total"]

    with SessionLocal() as db:
        if montant > SEUIL_MAX:
            publish_event("paiement.events", Event.build("PaiementRefuse", "paiement", {"commande_id": commande_id}), db)
        else:
            publish_event("paiement.events", Event.build("PaiementEffectue", "paiement", {"commande_id": commande_id}), db)

if __name__ == "__main__":
    start_consumer("stock.events", handle_stock)
