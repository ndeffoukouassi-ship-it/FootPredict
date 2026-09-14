# FootPredict

Application d'analyse de matchs de football orientée pronostics.

## Fonctionnalités

- Matchs du jour regroupés par ligue
- Analyse de forme (domicile / extérieur)
- Blessures et absences
- Pronostics 1X2
- Les deux équipes marquent (BTTS)
- Over / Under 2.5
- Pronostics 1ère mi-temps
- Score de confiance
- Recommandations automatiques
- Cache Redis

## Stack technique

| Couche       | Technologie                          |
|--------------|--------------------------------------|
| Frontend     | Next.js 15 + TypeScript + Tailwind   |
| Backend      | FastAPI (Python)                     |
| Cache        | Redis                                |
| Données      | API-Football                         |
| UI           | shadcn/ui + Lucide                   |

## Démarrage rapide

### Prérequis
- Docker & Docker Compose
- Clé API Football gratuite : https://www.api-football.com

### Installation

1. Place ta clé API dans `api/.env`
2. Lance tout avec une seule commande :

```bash
docker compose up --build
```

### URLs

- **Frontend** : http://localhost:3000
- **API Docs** : http://localhost:8000/docs
- **Health**   : http://localhost:8000/health

## Structure

```
foot-predict/
├── api/                  # Backend FastAPI
├── web/                  # Frontend Next.js
└── docker-compose.yml
```

## Roadmap

- [ ] Modèle ML (LightGBM / XGBoost)
- [ ] Value bets (comparaison avec les cotes)
- [ ] Authentification + suivi de bankroll
- [ ] Notifications
- [ ] Application mobile (PWA)

## Licence

MIT
