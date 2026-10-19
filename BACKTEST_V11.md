# FootPredict V11 — tests historiques

La V11 est développée sur une branche distincte de `main`. Aucun de ces tests ne garantit des gains.

## Données et sécurité

Depuis `api/`, fournir `API_FOOTBALL_KEY` comme variable d'environnement ou dans le fichier local `.env`. Ne jamais publier cette clé ni committer ce fichier. L'accès aux historiques dépend de l'abonnement API-Football.

## Récupérer les rencontres terminées

Exemple pour les saisons 2024 de la Premier League (39) et de la Liga (140) :

```bash
cd api
python -m app.services.collect_history --league 39 --season 2024 --league 140 --season 2024 --output history.json
```

Pour davantage de données, ajouter d'autres paires `--league ID --season YEAR`. Vérifier les quotas API avant les appels. Le collecteur déduplique les matchs et ne retient que le statut FT.

## Évaluer les prédictions

```bash
python -m app.services.backtest --input history.json --limit 1000 --output backtest-report.json
```

Le rapport donne le nombre de matchs réellement évalués, le taux d'exactitude 1X2, le Brier multiclasses et la log-loss. Un historique minimum de cinq matchs antérieurs par équipe est requis. Il faut **plus de 1 000 matchs bruts** pour espérer 1 000 matchs évaluables.

## Limites de validité

- Les matchs de même heure ne servent pas d'historique les uns aux autres.
- Le test ne reconstitue pas les blessures, les compositions ou les cotes connues avant chaque rencontre.
- Les modèles et seuils doivent être évalués sur des périodes non utilisées pour les régler.
- Les données simulées des tests unitaires ne doivent jamais être annoncées comme des résultats réels.
- Ce rapport mesure la qualité des probabilités, non la rentabilité des paris.
