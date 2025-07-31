import requests
import time

for _ in range(50):
    requests.post("http://localhost:8006/commande/", json={
        "client_id": 1,
        "produits": [{"id": 1, "quantite": 2}, {"id": 3, "quantite": 1}]
    })
    time.sleep(0.2)
