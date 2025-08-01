# ADR 1 — Choix d’Apache Kafka comme système de messagerie pour la communication inter-services

## Contexte

Dans une architecture microservices, chaque service (commande, stock, paiement) est autonome et découplé. Or, une coordination est requise pour garantir la cohérence des transactions distribuées. Une solution classique est d’utiliser une architecture orientée événements avec un système de messagerie pour transmettre les événements entre services.

Le projet nécessite :

- Un transport fiable et persistant des événements (commande créée, stock réservé, paiement effectué, etc.)
- La relecture des événements passés dans un Event Store
- Un bus d’événements rapide et compatible Python

## Décision

Nous avons choisi **Apache Kafka** comme infrastructure de messagerie centrale. Kafka agit à la fois comme système de transport (Pub/Sub) et journal d’événements durable (Event Store), ce qui nous permet d’unifier les flux de messages et le stockage historique.

## Justification

- Kafka permet un découplage total entre les producteurs (ex : service commande) et les consommateurs (stock, paiement)
- Kafka est conçu pour scaler horizontalement, ce qui répond aux besoins futurs de montée en charge
- Grâce à son modèle de topics partitionnés et à la rétention configurable, Kafka permet de rejouer les événements pour reconstruire l’état ou corriger des erreurs
- La bibliothèque `kafka-python` nous a permis d’intégrer Kafka de manière simple et efficace dans chaque microservice

## Conséquences

- L’architecture devient événementielle, avec des services plus autonomes
- Le traitement des messages est asynchrone, ce qui améliore la tolérance aux pannes
- Kafka devient un composant critique qu’il faut surveiller et superviser attentivement
- Une logique de consommation et d’acknowledgement doit être bien gérée pour éviter les doublons ou pertes de messages
