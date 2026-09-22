# Mbécté Trading

Application e-commerce Django claire et responsive pour une boutique de beauté et de soin. Les visiteurs commandent sans compte, depuis une fiche produit ou un panier de session. Le propriétaire dispose d’un espace privé pour gérer le catalogue, les commandes et les informations publiques de la boutique.

## Fonctionnalités

- vitrine publique et catalogue responsive ;
- produits avec image principale, galerie ordonnée, slug stable et prix promotionnel ;
- panier stocké en session, commande directe et commande panier sans compte client ;
- instantané du nom et du prix dans chaque ligne de commande ;
- notification SMTP avec journalisation si l’envoi échoue, sans annuler la commande ;
- dashboard protégé : KPI, produits, commandes, statuts, réglages boutique et compte ;
- pages privées non mises en cache, déconnexion POST avec confirmation et CSRF ;
- SEO de base : métadonnées, Open Graph produit, `robots.txt`, `sitemap.xml`, pages 404/500 ;
- configuration SQLite locale ou PostgreSQL par variables d’environnement.

## Prérequis

- Python 3.14 ou une version récente compatible avec Django 6 ;
- Git ;
- PostgreSQL uniquement si vous l’utilisez en production.

## Installation locale

Sous PowerShell :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Sous macOS/Linux, l’activation est `source .venv/bin/activate` et la copie `cp .env.example .env`.

Ouvrez ensuite :

- boutique : `http://127.0.0.1:8000/`
- connexion propriétaire : `http://127.0.0.1:8000/compte/connexion/`
- dashboard : `http://127.0.0.1:8000/dashboard/`

Le fichier `.env` est chargé automatiquement et n’est jamais versionné. Remplacez impérativement `SECRET_KEY`, désactivez `DEBUG` et renseignez les hôtes autorisés avant une mise en production.

## Images et fichiers statiques

Les images produits sont enregistrées dans `media/products/` via `ImageField`. En développement, Django sert automatiquement `MEDIA_URL`. En production, configurez le serveur web ou un stockage média persistant pour servir le dossier `MEDIA_ROOT`.

Collectez les fichiers statiques avant le déploiement :

```powershell
python manage.py collectstatic --noinput
```

Le logo vectoriel se trouve dans `static/images/logo.svg`. Les favicons sont dans le même dossier. Ils peuvent être remplacés par les fichiers définitifs du client en conservant les noms.

## SMTP

Configurez dans `.env` :

```env
EMAIL_HOST=smtp.votre-fournisseur.com
EMAIL_PORT=587
EMAIL_HOST_USER=adresse@example.com
EMAIL_HOST_PASSWORD=mot-de-passe-application
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=adresse@example.com
OWNER_ORDER_EMAIL=proprietaire@example.com
```

Utilisez un mot de passe d’application fourni par le service email. En cas de panne SMTP, la commande reste enregistrée et l’erreur est écrite dans les logs.

Pour tester sans envoyer d’email :

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
OWNER_ORDER_EMAIL=proprietaire@example.com
```

## PostgreSQL

Le pilote `psycopg` est déjà inclus. Modifiez `.env` :

```env
DB_ENGINE=postgresql
DB_NAME=mbecte_trading
DB_USER=mbecte
DB_PASSWORD=un-secret-fort
DB_HOST=localhost
DB_PORT=5432
```

Puis exécutez `python manage.py migrate`. Aucun identifiant de base de données n’est codé en dur.

## Vérifications

```powershell
python manage.py check
python manage.py makemigrations --check
python manage.py test
```

Les tests couvrent les slugs et promotions, le panier, les deux parcours de commande, les totaux, le fallback email, les statuts, l’accès privé, les en-têtes anti-cache et la déconnexion.

## Commandes Git utiles

```powershell
git status
git add .
git commit -m "Description du changement"
git pull --rebase origin main
git push origin main
```

Remote attendu : `git@github.com:YoussouThiombane/shop.git`. Ne jamais versionner `.env`, `.venv`, `db.sqlite3`, les uploads ou les secrets.
