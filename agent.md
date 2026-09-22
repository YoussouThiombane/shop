# AGENT.md — Mbécté Trading

## Mission
Construire et maintenir l'application Django Mbécté Trading sans dériver du périmètre fonctionnel. Prioriser un produit simple, fiable, premium, responsive et maintenable.

## Règles de décision
- Ne pas réécrire une partie fonctionnelle sans raison concrète.
- Avant de modifier l'architecture, vérifier si une solution locale suffit.
- Préférer le code Django standard aux dépendances supplémentaires.
- Ne pas ajouter de framework JavaScript lourd.
- Frontend : templates Django + Bootstrap 5 + CSS custom + JavaScript natif.
- Réutiliser les composants existants avant d'en créer de nouveaux.
- Éviter la sur-ingénierie.
- Ne pas inventer de fonctionnalités métier non demandées.
- En cas d'ambiguïté mineure, choisir l'option la plus simple, sûre et maintenable.

## Environnement Python
- Toujours travailler dans `.venv`.
- Si `.venv` n'existe pas : `python -m venv .venv`.
- Ne jamais installer de package globalement.
- Toute nouvelle dépendance doit être justifiée et ajoutée à `requirements.txt`.
- Les secrets restent dans `.env`, jamais dans Git.

## Architecture fonctionnelle
Le projet couvre uniquement :
- vitrine publique
- catalogue produits
- images multiples par produit
- panier par session
- commande sans compte client
- commande directe depuis une fiche produit
- dashboard propriétaire
- gestion produits
- gestion commandes
- paramètres boutique
- notifications email de nouvelles commandes
- authentification propriétaire

## Produit
Chaque produit possède :
- nom
- slug unique
- description
- prix
- prix promotionnel facultatif
- image principale
- images complémentaires
- statut actif/inactif

Règles :
- image principale toujours affichée en premier
- prix normal barré uniquement si une promo valide existe
- slug stable et unique
- URL publique : `/produits/<slug>/`
- dashboard : bouton copier l'URL publique

## Commandes
Le client ne crée jamais de compte.

Commande directe :
- nom complet
- téléphone
- adresse
- quantité

Commande panier :
- les quantités sont déjà dans le panier
- demander seulement nom complet, téléphone et adresse

Statuts minimum :
- preparation
- delivered

Les lignes de commande stockent le nom et le prix au moment de la commande pour préserver l'historique.

## Emails
- Nouvelle commande => email propriétaire.
- Utiliser SMTP via variables d'environnement.
- Mot de passe d'application uniquement dans `.env`.
- Une panne SMTP ne doit jamais supprimer ou annuler une commande déjà créée.

## UI / Branding
Ne pas créer un thème noir dominant.

Palette de référence :
- `#FAF8F3` ivoire
- `#FFFFFF` blanc
- `#222326` charbon
- `#C69A45` doré
- `#A7792F` doré hover
- `#DED6CA` beige/taupe
- `#7E8A75` sauge discret

Le site doit être :
- clair
- sobre
- premium
- humain
- fluide
- responsive
- accessible

Éviter les effets visuels typiques de templates IA : gradients excessifs, glassmorphism partout, halos lumineux, animations inutiles, textes marketing génériques.

## WhatsApp
Numéro initial : `70 207 39 07`.

Il est affiché à titre d'information uniquement :
- pas de lien `wa.me`
- pas de redirection WhatsApp automatique
- pas de bouton WhatsApp cliquable

## Authentification et cache
- Toutes les pages privées sont protégées.
- Logout uniquement en POST.
- Afficher un modal de confirmation avant logout.
- Après logout, le bouton Retour du navigateur ne doit pas restaurer une page privée utilisable.
- Pages privées : `no-store`, `no-cache`, `must-revalidate`, `max-age=0`, `Pragma: no-cache`, `Expires: 0`.
- CSRF actif.

## Base de données
- SQLite acceptable pour développement local.
- Configuration compatible PostgreSQL via variables d'environnement.
- Ne pas coder en dur les identifiants de base.

## Qualité
Avant tout commit final :
- `python manage.py check`
- migrations cohérentes
- tests passants
- absence de secrets dans Git
- `.gitignore` vérifié
- parcours commande directe testé
- parcours panier testé
- logout + retour navigateur testé
- responsive vérifié

## Git
Remote attendu :
`git@github.com:YoussouThiombane/shop.git`

Ne jamais faire de `git push --force` sans instruction explicite.

## Principe d'économie de quota IA
Avant de lancer une exploration large ou une refonte :
1. lire uniquement les fichiers liés à la tâche
2. identifier la cause précise
3. faire le changement minimal
4. tester
5. s'arrêter si l'objectif est atteint

Ne pas relire tout le projet si 2 ou 3 fichiers suffisent. Ne pas générer plusieurs variantes d'une même solution sans besoin réel.
