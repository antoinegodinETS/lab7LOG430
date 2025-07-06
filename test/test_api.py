import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import pytest
from fastapi.testclient import TestClient
from main import app
from common.database import SessionLocal, init_db  # Import correct de init_db
from magasin.models import Magasin, Produit, StockMagasin
from maison_mere.models import Vente
from logistique.models import DemandeApprovisionnement, StockLogistique

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    session = SessionLocal()
    session.query(DemandeApprovisionnement).delete()
    session.query(Vente).delete()
    session.query(StockMagasin).delete()
    session.query(StockLogistique).delete()
    session.query(Produit).delete()
    session.commit()
    session.close()
    init_db()  # Appel correct à init_db
    yield
    session = SessionLocal()
    session.query(DemandeApprovisionnement).delete()
    session.query(Vente).delete()
    session.query(StockMagasin).delete()
    session.query(StockLogistique).delete()
    session.query(Produit).delete()
    session.commit()
    session.close()


client = TestClient(app)

def insert_magasin_et_produit():
    session = SessionLocal()

    magasin = Magasin(nom="Magasin API", quartier="Est")
    session.add(magasin)
    session.commit()

    produit = Produit(nom="Produit API", prix=12.5, description="Test API produit")
    session.add(produit)
    session.commit()

    stock = StockMagasin(magasin_id=magasin.id, produit_id=produit.id, quantite=30)
    session.add(stock)
    session.commit()

    # 🔑 Récupérer les IDs pendant que la session est encore ouverte
    magasin_id = magasin.id
    produit_id = produit.id

    session.close()

    return magasin_id, produit_id

def test_get_stock_magasin(setup_database):
    magasin_id, _ = insert_magasin_et_produit()

    response = client.get(f"/api/v1/magasins/{magasin_id}/stock")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["quantite"] == 30
    assert "produit_id" in data[0]

def test_vente_magasin(setup_database):
    magasin_id, produit_id = insert_magasin_et_produit()

    # Vente de 5 unités
    response = client.post(f"/api/v1/magasins/{magasin_id}/produits/{produit_id}/vente?quantite=5")
    assert response.status_code == 200
    assert "Vente réussie" in response.text or "✅" in response.text

    # Vérifier stock mis à jour
    session = SessionLocal()
    stock = session.query(StockMagasin).filter_by(magasin_id=magasin_id, produit_id=produit_id).first()
    session.close()
    assert stock.quantite == 25
    
def test_rapport_consolide():
    response = client.get("/api/v1/maison-mere/rapport-ventes")
    assert response.status_code == 200
    assert "ventes_par_magasin" in response.json()


def test_stock_logistique():
    response = client.get("/api/v1/logistique/stock")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_performances_magasin():
    response = client.get("/api/v1/maison-mere/performance")
    assert response.status_code == 200
    assert "chiffre_affaires" in response.json()

def test_update_produit():
    # Créer produit d'abord
    from magasin.models import Produit
    from common.database import SessionLocal
    db = SessionLocal()
    produit = Produit(nom="Ancien", prix=10.0, description="Desc")
    db.add(produit)
    db.commit()
    pid = produit.id
    db.close()

    response = client.put(f"/api/v1/maison-mere/produits/{pid}", json={"nom": "Nouveau"})
    assert response.status_code == 200
    assert response.json()["message"] == "Produit mis à jour avec succès"
    
def test_vente_produit():
    from magasin.models import Magasin, Produit, StockMagasin
    from common.database import SessionLocal
    db = SessionLocal()

    m = Magasin(nom="Mag Test", quartier="A")
    p = Produit(nom="TestProduit", prix=5.0, description="Desc")
    db.add_all([m, p])
    db.commit()

    s = StockMagasin(magasin_id=m.id, produit_id=p.id, quantite=10)
    db.add(s)
    db.commit()

    # 🔐 Récupérer les IDs avant de fermer la session
    magasin_id = m.id
    produit_id = p.id
    db.close()

    response = client.post(f"/api/v1/magasins/{magasin_id}/produits/{produit_id}/vente?quantite=5")
    assert response.status_code == 200
    assert "réussie" in response.text


def test_demande_et_validation_approvisionnement():
    from magasin.models import Magasin, Produit
    from logistique.models import StockLogistique
    from common.database import SessionLocal

    db = SessionLocal()
    m = Magasin(nom="MagA", quartier="Z")
    p = Produit(nom="ProdZ", prix=3.0, description="...")
    db.add_all([m, p])
    db.commit()

    stock = StockLogistique(produit_id=p.id, quantite=100)
    db.add(stock)
    db.commit()

    # ✅ Récupère les id avant de fermer la session
    magasin_id = m.id
    produit_id = p.id
    db.close()

    # Création demande
    resp = client.post("/api/v1/logistique/demande", params={
        "magasin_id": magasin_id,
        "produit_id": produit_id,
        "quantite": 10
    })
    assert resp.status_code == 200

    # Validation
    resp_val = client.post("/api/v1/logistique/approvisionner", params={
        "produit_id": produit_id,
        "quantite": 10,
        "magasin_id": magasin_id
    })
    assert resp_val.status_code == 200
    assert "envoyées" in resp_val.text


