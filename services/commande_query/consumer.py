import json
import time
from kafka import KafkaConsumer
from database import SessionLocal
from models import CommandeRead
from prometheus_client import Counter, Histogram, start_http_server
from datetime import datetime

# Démarre Prometheus sur un port dédié
start_http_server(8014)

# Déclaration des métriques
events_consumed = Counter("events_consumed_total", "Nombre d'événements consommés", ["type"])
latency = Histogram("event_processing_latency_seconds", "Latence émission → consommation")

def start_consumer():
    consumer = KafkaConsumer(
        'commande.events',
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='commande_query_group'
    )

    for message in consumer:
        event = message.value

        # Incrément du compteur Prometheus
        events_consumed.labels(type=event["type"]).inc()

        # Calcul de la latence si timestamp est disponible
        try:
            start_ts_str = event.get("timestamp") or event.get("payload", {}).get("timestamp")
            if start_ts_str:
                start_ts = datetime.fromisoformat(start_ts_str).timestamp()
                latency.observe(time.time() - start_ts)
        except Exception as e:
            print(f"[WARN] Erreur lors du calcul de latence : {e}")

        # Traitement de l'événement CommandeCreee
        if event["type"] == "CommandeCreee":
            payload = event["payload"]
            commande = CommandeRead(
                id=payload["commande_id"],
                client_id=1,  # à adapter si le client_id est inclus dans le payload
                statut="validee",
                produits=payload["produits"]
            )

            db = SessionLocal()
            db.merge(commande)
            db.commit()
            db.close()
