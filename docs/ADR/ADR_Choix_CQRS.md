# ADR 2 — Adoption du pattern CQRS avec synchronisation événementielle

## Contexte

Le service commande gère des opérations complexes : validation métier, émission d’événements, suivi de l’état d’une commande. Il est important de séparer les opérations d’écriture (création de commande, mise à jour d’état) des opérations de lecture (consultation des commandes) pour :

- améliorer les performances de lecture
- éviter les conflits de verrouillage
- isoler les projections utilisées dans l’IHM ou les analyses

## Décision

Nous avons adopté le pattern **CQRS** (Command Query Responsibility Segregation). Cela consiste à :

- utiliser une base orientée écriture dans le service commande principal
- créer un service séparé (`commande_query`) dédié aux lectures, alimenté par les événements Kafka

## Justification

- Kafka agit comme **Event Broker** entre les deux services
- Le service `commande_query` consomme les événements `CommandeCreee`, `CommandeMiseAJour`, etc., et les insère dans une base optimisée pour la lecture
- Cette séparation rend l’architecture plus modulaire et évolutive

## Conséquences

- L’écriture et la lecture utilisent des modèles de données différents, adaptés à chaque usage
- Le service de lecture peut être mis à jour ou régénéré simplement en rejouant les événements Kafka
- La cohérence est éventuelle entre les deux vues, ce qui est acceptable pour notre scénario
- Il faut superviser les consommateurs Kafka pour garantir la synchronisation
