# Frontend Flask - Cloud Files

Interface Flask/Tailwind qui consomme une API de partage de fichiers.

## Fonctionnalites

- Authentification (login/signup/logout)
- Upload de fichier (public/prive)
- Tableau de bord utilisateur (liste, changement de statut, suppression)
- Page publique des fichiers partages

## Demarrage local

1. Creer un environnement virtuel:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Installer les dependances:
```bash
pip install -r requirements.txt
```

3. Variables d'environnement:
```bash
export FLASK_SECRET_KEY="une-cle-secrete-forte"
export CLOUD_API_URL="https://cloud-backend-80wx.onrender.com"
```

4. Lancer l'application:
```bash
python3 app.py
```

## Deploiement Vercel

Le projet est pret pour Vercel avec `vercel.json`.

1. Importer le repo dans Vercel.
2. Ajouter les variables d'environnement dans le projet Vercel:
   - `FLASK_SECRET_KEY` (obligatoire en production)
   - `CLOUD_API_URL` (URL de ton backend)
   - `API_TIMEOUT_SECONDS` (optionnel, ex: `15`)
3. Lancer le deploy.

## Structure utile

- `app.py`: application Flask principale
- `api.py`: client HTTP vers le backend
- `templates/`: vues Jinja2
- `static/`: assets frontend
- `vercel.json`: configuration de deploiement Vercel

