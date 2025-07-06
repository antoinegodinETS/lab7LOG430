# ADR – Choix de PostgreSQL comme moteur de base de données

## Statut  
Décision prise – 9 juin 2025

## Contexte  
Le projet a évolué pour gérer **plusieurs magasins**, un **centre logistique** et une **maison mère**, avec des besoins en **synchronisation des données**, **transactions concurrentes** et **consultation centralisée**.  
Le système n’est plus mono-instance mais repose sur une architecture modulaire avec des interactions entre services.  

Le moteur de base de données doit permettre :
- Une gestion robuste des transactions concurrentes
- Des connexions réseau (accès client/serveur)
- Un bon support de requêtes complexes et jointures
- Une capacité de montée en charge raisonnable

## Décision  
Nous avons choisi **PostgreSQL** comme base de données principale pour le système.

### Raisons principales :
- **Robustesse transactionnelle** : PostgreSQL garantit l’ACID, essentiel pour les opérations critiques comme les ventes, les mouvements de stock et les validations.
- **Support client/serveur** : Chaque entité (magasin, logistique, maison mère) peut se connecter à un serveur PostgreSQL central ou conteneurisé, ce qui facilite la **centralisation** des données.
- **Compatibilité ORM** : Excellent support avec SQLAlchemy, ce qui permet de conserver la même couche d’abstraction que dans Lab 1.
- **Évolutivité** : PostgreSQL est adapté pour monter en charge, même dans un contexte futur de déploiement cloud ou web/mobile.
- **Requêtes avancées** : Permet d’agréger facilement les données pour les rapports consolidés, les tableaux de bord (UC1, UC3), et les alertes.

## Conséquences  
- Le projet doit maintenant inclure un service PostgreSQL (via `docker-compose`) ou pointer vers un serveur PostgreSQL.
- Les scripts de création de base et les modèles SQLAlchemy doivent être compatibles PostgreSQL.
- L’intégration en CI/CD doit prévoir une BDD PostgreSQL pour les tests.
- Le déploiement en environnement de prod/test nécessite une configuration réseau plus rigoureuse (ports, credentials, etc.).

## Alternatives envisagées mais rejetées  
- **SQLite** : Trop limité pour la gestion concurrente et les connexions multi-sources. Inadéquat pour la centralisation des magasins/logistique.
- **MongoDB** : Moins adapté pour des opérations SQL relationnelles et des contraintes fortes d’intégrité.
- **MySQL** : Comparable à PostgreSQL, mais PostgreSQL est mieux outillé pour des opérations complexes (ex : `CTE`, JSONB, transactions imbriquées).
- **Base cloud externe** : Rejetée pour des raisons de simplicité, de coût et de dépendance à Internet dans un contexte local de VM.
