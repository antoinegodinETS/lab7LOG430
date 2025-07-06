# 🔄 Comparaison de Performance : Avec et Sans Load Balancing

## 🧪 Méthodologie

Nous avons utilisé l’outil [k6](https://k6.io) pour simuler 20 utilisateurs virtuels (VUs) pendant 10 secondes. Le test a été effectué deux fois :

- 🟢 Une fois via **l’API Gateway avec NGINX** (load balancing activé entre deux instances `interface1` et `interface2`)
- 🔴 Une autre fois **directement vers `interface1`** sans load balancing

---

## 📊 Résultats

| 🔧 Scénario                     | ⚖️ Avec Load Balancer (NGINX) | 🚫 Sans Load Balancer (interface1) |
|-------------------------------|-------------------------------|------------------------------------|
| **Requêtes complètes**        | 5 854                         | 4 587                              |
| **Requêtes réussies**         | ✅ 100 %                       | ✅ 100 %                            |
| **Durée moyenne (req)**       | 33.89 ms                      | 43.43 ms                           |
| **Durée médiane (req)**       | 32.74 ms                      | 42.58 ms                           |
| **95ᵉ percentile**            | 61.77 ms                      | 49.44 ms                           |
| **RPS (req/sec)**             | 583.8                         | 456.8                              |
| **Données reçues**            | 1.1 MB                        | 706 kB                             |
| **Données envoyées**          | 457 kB                        | 358 kB                             |

---

## ✅ Analyse

- Le **load balancing via NGINX** permet de traiter **environ 27 % de requêtes supplémentaires** dans le même intervalle.
- La **latence moyenne est réduite de ~10 ms**, ce qui améliore la réactivité globale.
- Le système démontre une meilleure **scalabilité horizontale** grâce à la répartition de charge entre deux services identiques.

---

## 📌 Conclusion

Le scénario avec load balancing offre des performances significativement meilleures. Cette architecture est à privilégier en production pour mieux absorber les pics de charge et garantir une meilleure expérience utilisateur.

