# ADR – Choix de la plateforme de développement

## Statut
Décision prise – 21 mai 2025

## Contexte
Le laboratoire consiste à développer un système de caisse (POS) local, avec une application console et une base de données locale.  
Le projet doit être rapide à mettre en place, simple à comprendre, facile à tester et portable entre différents systèmes d’exploitation.

Les options envisagées :
- Python
- Java
- Node.js / JavaScript
- Go
- Rust

## Décision
Le langage et la plateforme retenus sont **Python 3** (avec SQLAlchemy pour la persistance).

### Raisons principales :
- **Simplicité et productivité** : Python permet de développer rapidement des prototypes fonctionnels avec un minimum de code.
- **Lisibilité** : Le code Python est facile à lire et à maintenir, ce qui facilite la relecture et la correction dans un contexte d’équipe ou d’enseignement.
- **Support des outils** : Bibliothèques de qualité pour la persistance (SQLAlchemy), les tests (pytest/unittest), la gestion de dépendances (pip, poetry) et l’intégration continue.
- **Portabilité** : Python est disponible sur tous les systèmes d’exploitation courants. Facile à packager et à dockeriser.
- **Communauté et documentation** : Très grande communauté, beaucoup de documentation et d’exemples, ce qui facilite la résolution de problèmes.
- **Gestion de la base de données** : L’intégration avec SQLite est native et très simple à mettre en place.
- **Approprié pour une application console** : Pas besoin d’interface graphique complexe.

Les autres plateformes n’ont pas été retenues car :
- **Java** : Plus verbeux, nécessite plus de configuration, plus lourd pour un petit projet console.
- **Node.js** : Moins naturel pour des applications console simples.
- **Go / Rust** : Excellents pour la performance, mais courbe d’apprentissage plus élevée et surdimensionnés pour ce contexte.

## Conséquences
- Le projet sera écrit en Python 3, avec SQLAlchemy comme ORM et SQLite comme base de données locale.
- Facile à exécuter, à tester et à dockeriser.
- La structure du projet sera simple à comprendre et à faire évoluer.

## Alternatives envisagées mais rejetées
- **Java** : Trop lourd et verbeux pour un projet simple en console.
- **Node.js** : Moins adapté à une interface utilisateur en ligne de commande.
- **Go / Rust** : Trop bas niveau pour le contexte du laboratoire, complexité inutile.

## Mise à jour – 9 juin 2025

Bien que le choix initial ait été fait dans le cadre d’une application console locale (Lab 1), le projet a évolué vers une architecture modulaire utilisant FastAPI avec PostgreSQL (Lab 2).  
Le choix de **Python 3** reste toutefois pertinent, car :

- Il s’intègre très bien avec **FastAPI**, SQLAlchemy et la conteneurisation.
- Il permet de maintenir une **cohérence de langage** sur tous les modules (maison mère, magasin, logistique).
- Il simplifie le déploiement grâce aux outils comme `uvicorn`, `pytest`, et `docker-compose`.

Les conséquences techniques ont été ajustées :
- Utilisation de **PostgreSQL** au lieu de SQLite.
- Présence d’une **interface web minimale** plutôt qu’un simple CLI.