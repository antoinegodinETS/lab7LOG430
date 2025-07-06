# Système Multi-Magasins - Architecture Microservices avec API Gateway et Observabilité

Une application web Python modulaire pour gérer les **stocks**, **ventes**, **approvisionnements** et fonctionnalités **e-commerce**.  
Basée sur **FastAPI**, elle expose des **API RESTful** et propose une **interface web** pour la maison mère et les magasins.  
**PostgreSQL** assure la persistance des données, tandis qu’une **API Gateway** centralise les accès.

---

## 🚀 Démarrage rapide

1. **Installer les dépendances**
2. **Initialiser la base de données**  
   Les scripts `init_data.py` et `populate_ventes.py` sont automatiquement exécutés au lancement.  
   👉 Pas besoin de lancer manuellement l'initialisation.

3. **Lancer les services avec Docker Compose**  
   - Interface accessible : [http://localhost:8088](http://localhost:8088)  
   - API principale : [http://localhost:8003/docs](http://localhost:8003/docs)  
   - API Gateway : [http://localhost:8080](http://localhost:8080)

---

## 🧱 Structure du projet

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

## 📈 Résultats observables

- **Latence** : mesurée via **Prometheus** / **Grafana**
- **Disponibilité** : vérifiée via les logs centralisés
- **Répartition de charge** : visualisée dans Grafana
![Alt text](docs/latence.PNG?raw=true "Latence")
![Alt text](docs/erreur5xx.PNG?raw=true "Erreur5xx")
---

## 📝 Licence

Ce projet est sous licence **MIT**.

---

## 📎 Notes supplémentaires

- **Swagger / OpenAPI** : chaque service FastAPI expose sa documentation via `/docs`
- **Postman** : requêtes mises à jour pour utiliser l’API Gateway KrakenD
