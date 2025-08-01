import requests
import time

COMMANDE_URL = "http://localhost:8006/commande/"

def test_saga_succes(n=5):
    print(f"\n--- Test Saga - {n} Cas de succès ---")
    for i in range(n):
        data = {
            "client_id": 1,
            "produits": [
                {"id": 1, "quantite": 1},
                {"id": 2, "quantite": 1}
            ]
        }
        r = requests.post(COMMANDE_URL, json=data)
        r.raise_for_status()
        print(f"✅ {i+1}/{n} Commande succès :", r.json())
        time.sleep(1)  # peut réduire à 0.5 si Kafka est rapide

def test_saga_echec(n=5):
    print(f"\n--- Test Saga - {n} Cas d’échec ---")
    for i in range(n):
        data = {
            "client_id": 2,
            "produits": [
                {"id": 1, "quantite": 2},
                {"id": 2, "quantite": 2}  # total = 700
            ]
        }
        r = requests.post(COMMANDE_URL, json=data)
        r.raise_for_status()
        print(f"❌ {i+1}/{n} Commande échec :", r.json())
        time.sleep(1)

if __name__ == "__main__":
    test_saga_succes(n=10)
    test_saga_echec(n=10)
    print("\n✅ Tests de saga complétés.")
