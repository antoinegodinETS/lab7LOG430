from event_store.consumer import start_consumer
import requests
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("commande.consumer")

def handle_paiement(event):
    try:
        event_type = event.get("type")
        payload = event.get("payload", {})
        commande_id = payload.get("commande_id")

        if not commande_id:
            logger.warning("Événement sans commande_id : %s", event)
            return

        if event_type == "PaiementEffectue":
            etat = "PAYEE"
        elif event_type == "PaiementRefuse":
            etat = "ANNULEE"
        else:
            logger.info("Événement ignoré : %s", event_type)
            return

        response = requests.post(
            f"http://commande:8000/commande/{commande_id}/etat",
            json={"etat": etat}
        )

        if response.status_code == 200:
            logger.info(json.dumps({
                "event": event_type,
                "commande_id": commande_id,
                "action": f"État mis à jour → {etat}"
            }))
        else:
            logger.error(json.dumps({
                "event": event_type,
                "commande_id": commande_id,
                "error": f"Erreur API commande : {response.status_code}",
                "details": response.text
            }))

    except Exception as e:
        logger.exception(f"Erreur dans handle_paiement : {str(e)}")

if __name__ == "__main__":
    start_consumer("paiement.events", handle_paiement)
