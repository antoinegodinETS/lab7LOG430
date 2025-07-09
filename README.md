# Système Multi-Magasins - Architecture Microservices avec API Gateway et Observabilité

Une application web Python modulaire pour gérer les **stocks**, **ventes**, **approvisionnements** et fonctionnalités **e-commerce**.  
Basée sur **FastAPI**, elle expose des **API RESTful** et propose une **interface web** pour la maison mère et les magasins.  
**PostgreSQL** assure la persistance des données, tandis qu’une **API Gateway** centralise les accès.

---

## 🚀 Démarrage rapide

### 1. Installer les dépendances :
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
```

### 2. Lancer les services avec Docker Compose
```bash
docker-compose up --build
```

### Interfaces disponibles
- Interface 1 : [http://localhost:8004](http://localhost:8004)
- Interface 2 : [http://localhost:8005](http://localhost:8005)

## 📦 Exemple d’appel de la saga via cURL

Le service **orchestrateur** expose une route `POST /saga/commande/` qui déclenche une saga complète de validation de commande (stock + paiement).

### ✅ Cas de succès — Commande complète et confirmée

```bash
curl -X POST http://localhost:8002/saga/commande/ \
  -H "Content-Type: application/json" \
  -d '{
    "produits": [
      {"produit_id": 1, "quantite": 1},
      {"produit_id": 2, "quantite": 1}
    ]
  }'
```

Cette commande simule l’achat de produits disponibles en stock avec un montant raisonnable.  
Elle passe par toutes les étapes de la saga :

- 🟢 Création (`CREEE`)
- 🟢 Vérification du stock (`STOCK_VERIFIE`)
- 🟢 Réservation du stock (`STOCK_RESERVE`)
- 🟢 Paiement réussi (`PAYEE`)
- 🟢 Confirmation finale (`CONFIRMEE`)

---

### ❌ Cas d’échec — Stock insuffisant

```bash
curl -X POST http://localhost:8002/saga/commande/ \
  -H "Content-Type: application/json" \
  -d '{
    "produits": [
      {"produit_id": 2, "quantite": 999}  # Produit stock trop faible
    ]
  }'

```

Cette commande tente de commander un produit en quantité excessive.  
Résultat :

- 🔴 Échec à l’étape **de vérification du stock**
- 🔁 Saga interrompue
- ❌ Commande mise à jour à `ANNULEE`

---

### ❌ Cas d’échec — Paiement refusé

```bash
curl -X POST http://localhost:8002/saga/commande/ \
  -H "Content-Type: application/json" \
  -d '{
    "produits": [
      {"produit_id": 4, "quantite": 10}  # Suppose que le montant dépasse le solde
    ]
  }'

```

Cette commande passe la vérification et la réservation du stock, mais échoue au moment du paiement (ex. : montant trop élevé).  
Comportement de la saga :

- 🔁 Stock libéré automatiquement
- ❌ Commande mise à jour à `ANNULEE`

## 🧱 Structure du projet

Le projet est organisé en plusieurs services et composants pour assurer une architecture modulaire et scalable :

### 📂 Services principaux
- **Clients** : Gestion des comptes clients (CRUD).
- **Panier** : Gestion des paniers d'achat avec support pour le load balancing.
- **Commande** : Validation et suivi des commandes.
- **Stock** : Vérification et réservation des stocks.
- **Paiement** : Traitement des paiements.

### 📂 Composants supplémentaires
- **Orchestrateur** : Implémente les sagas pour coordonner les services.
- **API Gateway** : Centralise les accès et assure la répartition de charge.
- **Observabilité** : Monitoring avec Prometheus et visualisation avec Grafana.
- **Reverse Proxy** : Nginx pour la répartition de charge et le routage.

### 📂 Répartition des fichiers
- `services/` : Contient les services individuels (clients, panier, commande, etc.).
- `gateway/` : Configuration et code de l'API Gateway.
- `src/` : Code source principal pour l'interface et les scripts.
- `docs/` : Documentation et diagrammes UML.
- `test/` : Tests unitaires et d'intégration.
- `docker-compose.yml` : Configuration Docker pour orchestrer les services.

Cette structure permet une séparation claire des responsabilités et facilite la maintenance et l'évolution


### ✅ Fonctionnalités principales

- 🏬 Gestion de plusieurs **magasins**
- 📦 Suivi des **stocks** (magasin + centre logistique)
- 🔁 **Demandes d’approvisionnement** avec validation
- 💰 **Ventes de produits** (avec vérification de stock)
- 🛒 **Gestion du panier d'achat**
- 📋 Création et gestion des **comptes clients**
- 🛍️ Validation des **commandes** (check-out)
- 📊 Tableau de bord centralisé (**performances**, rapports)
- 🔍 Visualisation via **Prometheus + Grafana**
- ⚖️ Répartition de charge avec **Nginx** et **KrakenD**
- 🧪 Stress test via `k6`

---

## 📊 Observabilité

- **Prometheus** : [http://localhost:9091](http://localhost:9091)
- **Grafana** : [http://localhost:3000](http://localhost:3000)  
  ➤ login : `admin` / `admin`

Dashboards disponibles :
- monitoring des services clients, panier, commande, stock
- monitoring de l'API Gateway

---

## 🌐 API Gateway (KrakenD)

### Endpoints exposés via KrakenD

#### Clients
- `GET /clients` : Retourne la liste des clients
- `POST /clients` : Crée un nouveau client

#### Panier
- `GET /panier/{id}` : Retourne le contenu du panier
- `POST /panier` : Ajoute un produit au panier

#### Commande
- `GET /commande/{id}` : Retourne les détails d'une commande
- `POST /commande` : Valide une commande

### Configuration de KrakenD

L'API Gateway est configurée pour :
- **Routage dynamique** : redirige les requêtes vers les services appropriés.
- **Répartition de charge** : round-robin entre plusieurs instances d’un service.
- **Transformation des réponses** : traitement des objets ou listes JSON.

```json
// Exemple de configuration pour l'endpoint /clients dans krakend.json
{
  "endpoint": "/clients",
  "method": "GET",
  "backend": [
    {
      "host": ["http://clients:8000"],
      "url_pattern": "/clients"
    }
  ]
}
```

## ⚙️ CI/CD

Le projet utilise **GitHub Actions** pour :

- Linting avec **Flake8**
- Exécution des tests
- Build Docker

📁 Fichier : `.github/workflows/python-app.yml`

---

## 🔧 Choix techniques

| Technologie     | Rôle                               |
|------------------|--------------------------------------|
| Python 3.12       | Langage principal                   |
| FastAPI           | API REST + interface HTML          |
| SQLAlchemy        | ORM (PostgreSQL)                   |
| PostgreSQL        | Base de données relationnelle      |
| Docker            | Conteneurisation                   |
| KrakenD           | API Gateway                        |
| Grafana           | Visualisation                      |
| Prometheus        | Monitoring                         |
| Nginx             | Répartition de charge              |
| GitHub Actions    | Intégration continue (CI/CD)       |

---

## 🧪 Test de charge

### 🔁 Répartition de charge via KrakenD

Le fichier `krakend.json` configure une **répartition de charge round-robin** entre plusieurs instances d’un service.

#### 🔬 Exemple de test de charge avec `k6` :

```bash
k6 run k6-lb.js
```

## 📝 Licence

Ce projet est sous licence **MIT**.

---

## 📎 Notes supplémentaires

- **Swagger / OpenAPI** : chaque service FastAPI expose sa documentation via `/docs`
- **Postman** : requêtes mises à jour pour utiliser l’API Gateway KrakenD
