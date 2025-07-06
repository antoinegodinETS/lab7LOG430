# Rapport Arc42 – Architecture Microservices pour Système de Gestion

## 1. Introduction

Ce projet vise à concevoir une architecture microservices simple mais efficace pour un système de gestion réparti en plusieurs services : clients, panier, commandes. L’objectif est de démontrer l’évolutivité, la maintenabilité, la scalabilité et l’observabilité de l’architecture à l’aide d’outils modernes comme FastAPI, Docker, Prometheus, Grafana et K6.

## 2. Contexte et Motivations

Le système est destiné à simuler un cas réel de gestion de commande dans un environnement distribué. Il doit permettre :

- La gestion de clients
- La gestion de paniers d’achat
- La validation de commandes
- L’observation des performances
- Une structure évolutive pour le futur

## 3. Vue d’ensemble de l’architecture

### Schéma général :

- **API Gateway** : point d’entrée unique vers les services
- **Services indépendants** : clients, panier, commande
- **Bases de données séparées** pour chaque service
- **Reverse Proxy NGINX** pour le load balancing
- **Prometheus & Grafana** pour l’observabilité
- **K6** pour les tests de charge

### Technologies :

- FastAPI
- PostgreSQL
- Docker / Docker Compose
- Prometheus, Grafana
- K6
- NGINX

## 4. Vue de développement

Organisation des dossiers :

```
.
├── gateway/
├── services/
│ ├── clients/
│ ├── panier/
│ └── commande/
├── prometheus.yml
├── docker-compose.yml
└── grafana/
```

Chaque service suit une structure MVC avec séparation `main.py`, `models.py`, `crud.py`, `schemas.py`, `database.py`.

## 5. Vue de déploiement

Le déploiement est géré avec Docker Compose. Chaque service est conteneurisé avec sa propre base PostgreSQL. L’API Gateway redirige les requêtes vers les bons microservices. Prometheus et Grafana tournent sur des ports exposés pour l'observation.

## 6. Décisions architecturales (ADR)

### ADR 1 : Choix de l’architecture microservices

**Décision** : Utilisation de microservices indépendants plutôt qu’une architecture monolithique.
**Motivation** : Faciliter la scalabilité, l’isolement des erreurs, la maintenance.

### ADR 2 : Mise en place d’un API Gateway personnalisé

**Décision** : Utilisation d’un API Gateway codé en FastAPI avec httpx.
**Motivation** : Permet plus de contrôle, ajoute la logique de load balancing round-robin.

## 7. Qualités architecturales

| Critère        | Justification                                             |
| -------------- | --------------------------------------------------------- |
| Scalabilité    | Services indépendants + load balancing                    |
| Maintenabilité | Code modulaire, bases séparées                            |
| Observabilité  | Prometheus + Grafana                                      |
| Testabilité    | Tests via Postman et K6                                   |
| Disponibilité  | NGINX pour équilibrer les charges sur plusieurs instances |

## 8. Sécurité et accès

La Gateway applique des règles de **CORS** pour autoriser les appels depuis les frontends :

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 9. Documentation et tests

### Swagger / OpenAPI

Chaque microservice expose sa propre documentation via Swagger :

- [http://localhost:8001/docs](http://localhost:8001/docs) — **Service Clients**
- [http://localhost:8002/docs](http://localhost:8002/docs) — **Service Panier**
- [http://localhost:8006/docs](http://localhost:8006/docs) — **Service Commande**

La **Gateway** expose également une documentation automatique :

- [http://localhost:8080/docs](http://localhost:8080/docs)

### Tests

- Les requêtes Postman ont été mises à jour pour refléter l'utilisation de la Gateway.
- Des tests de charge ont été effectués à l’aide de l’outil **K6**.

#### Scénarios de tests avec K6 :

- **Sans load balancing** : appels directs vers `interface1`
- **Avec load balancing** : appels via **NGINX** (équilibreur de charge)

---

## 10. Observabilité

### Outils utilisés :

- **Prometheus** : collecte des métriques d’application
- **Grafana** : visualisation des performances (latence, erreurs 5xx, etc.)

### Comparaison des performances

| Critère             | Sans Load Balancing (`interface1`) | Avec Load Balancing (NGINX) |
| ------------------- | ---------------------------------- | --------------------------- |
| **Latence moyenne** | 43.43 ms                           | **33.89 ms**                |
| **Erreurs 5xx**     | 0                                  | 0                           |
| **Disponibilité**   | Moyenne                            | **Améliorée**               |

### Captures d’écran incluses :

- `latence.PNG`
- `erreur5xx.PNG`

---

## 11. Conclusion

L’architecture microservices mise en place répond efficacement aux besoins fonctionnels et non fonctionnels tout en conservant une solution simple et modulaire.
Grâce à la Gateway, au load balancing et à l'observabilité, nous avons pu améliorer la **résilience**, la **scalabilité** et la **traçabilité** du système.
