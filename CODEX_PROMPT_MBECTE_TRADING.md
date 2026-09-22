# Prompt Codex — Mbécté Trading

Tu es chargé de développer de zéro une application e-commerce Django complète pour **Mbécté Trading** dans un dossier de projet actuellement vide.

## 1. Objectif général
Créer un site vitrine + catalogue + prise de commandes, moderne, fluide, responsive et premium, pour vendre des produits de beauté et de soin du visage.

Le visiteur **ne crée pas de compte**. Seul le propriétaire/admin se connecte à une interface privée pour gérer ses produits, ses commandes, ses informations de contact et son tableau de bord.

Le dépôt Git distant à utiliser à la fin est :

```bash
git@github.com:YoussouThiombane/shop.git
```

Le logo fourni par le client se trouve dans le contexte de la tâche. Utilise-le dans le site et génère également un favicon cohérent à partir de son emblème.

## 2. Contraintes techniques obligatoires

- Framework : **Django**.
- Python : version récente compatible avec Django stable.
- Créer un environnement virtuel local nommé `.venv`.
- Installer tous les packages Python uniquement dans `.venv`.
- Générer `requirements.txt`.
- Utiliser des variables d'environnement via `.env` et fournir un `.env.example` sans secrets.
- Ne jamais committer `.env`, `.venv`, fichiers temporaires, base locale, caches ou secrets.
- Prévoir SQLite pour le développement local si nécessaire, mais rendre la configuration compatible PostgreSQL via variables d'environnement pour la production.
- Frontend : Django templates + HTML5 + CSS custom + Bootstrap 5 + JavaScript natif. Éviter les frameworks JS lourds.
- Les fichiers statiques doivent être organisés proprement.
- Les uploads produits doivent utiliser Django `ImageField` et Pillow.
- Le code doit être lisible, modulaire, maintenable et prêt à être repris par un développeur junior.
- Toutes les pages doivent être responsive mobile/tablette/desktop.

## 3. Direction artistique

Ne fais surtout pas un site sombre simplement parce que le logo est noir et doré.

Le design doit être **clair, sobre, premium, humain et personnalisé**, avec une esthétique beauté/soin haut de gamme, sans effet “template IA”.

Palette suggérée :

- fond principal : ivoire très clair `#FAF8F3`
- blanc : `#FFFFFF`
- texte principal : charbon doux `#222326`
- doré principal inspiré du logo : `#C69A45`
- doré foncé pour hover : `#A7792F`
- beige/taupe léger : `#DED6CA`
- vert sauge discret d'accent : `#7E8A75`

Le noir peut être utilisé uniquement ponctuellement pour les textes ou certains contrastes, jamais comme fond dominant.

Style attendu :

- beaucoup d'espace blanc
- typographie élégante et lisible
- cartes de produits propres avec ombres légères
- coins légèrement arrondis
- animations courtes et discrètes
- boutons bien dimensionnés
- navigation très simple
- états hover/focus visibles
- pas de surcharge visuelle
- accessibilité correcte des contrastes et formulaires

Utiliser le logo réel fourni. Créer un favicon propre à partir de l'emblème/monogramme du logo.

## 4. Architecture Django attendue

Organise le projet au minimum avec ces apps :

- `core` : accueil, paramètres publics, pages générales
- `catalog` : produits et images
- `orders` : panier et commandes
- `dashboard` : espace privé du propriétaire
- `accounts` : authentification admin/propriétaire

Tu peux ajuster cette structure si une organisation plus simple et propre est préférable, mais garde une séparation claire des responsabilités.

## 5. Modèle Produit

Créer un modèle `Product` avec au minimum :

- `name`
- `slug` unique
- `description`
- `price`
- `promotional_price` nullable
- `main_image`
- `is_active`
- `created_at`
- `updated_at`

Règles :

- le slug doit être généré automatiquement à partir du nom
- il doit rester unique même si plusieurs produits ont le même nom
- le propriétaire peut modifier le slug si nécessaire, mais l'unicité doit rester garantie
- si `promotional_price` est renseigné et strictement inférieur au prix normal, afficher le prix normal barré et le prix promo mis en avant
- si la promo est vide ou invalide, afficher uniquement le prix normal

Créer un modèle `ProductImage` lié à `Product` pour les images complémentaires :

- produit
- image
- ordre d'affichage
- texte alternatif facultatif

L'image principale doit toujours apparaître en premier dans la fiche produit.

## 6. Gestion des images produit

Dans l'interface privée :

- formulaire de création/édition produit
- upload d'une image principale
- possibilité d'ajouter plusieurs images complémentaires
- possibilité de supprimer une image complémentaire
- possibilité de choisir leur ordre d'affichage si c'est raisonnablement simple

Dans la page détail produit publique :

- carrousel/swiper tactile
- l'utilisateur doit pouvoir balayer sur mobile
- boutons précédent/suivant sur desktop
- miniatures si cela reste propre
- l'image principale est toujours la première image affichée
- chargement fluide et adapté au mobile

Tu peux utiliser le Carousel Bootstrap 5 sans package JS externe.

## 7. Page d'accueil publique

La page d'accueil doit contenir :

1. header clair avec logo Mbécté Trading
2. hero section courte et premium présentant la marque
3. quelques informations rassurantes sur l'entreprise et son positionnement beauté/soin
4. affichage du numéro WhatsApp du propriétaire **uniquement comme information** : `70 207 39 07`
5. ce numéro ne doit PAS être un lien `wa.me`, ni un bouton redirigeant vers WhatsApp
6. section produits immédiatement après les informations principales

Chaque carte produit doit afficher :

- image principale
- nom
- prix normal
- prix promo s'il existe
- bouton `Ajouter au panier`
- bouton `Voir le détail`

Le bouton `Ajouter au panier` ouvre un modal demandant uniquement la quantité avant ajout au panier.

## 8. Page détail produit

Créer une URL publique de type :

```text
/produits/<slug>/
```

La page doit afficher :

- carrousel images avec image principale en premier
- nom
- description
- prix normal / promo
- choix de quantité
- bouton `Ajouter au panier`
- bouton `Commander maintenant`

`Commander maintenant` doit ouvrir un modal demandant :

- nom complet
- numéro de téléphone
- adresse
- quantité

Le formulaire doit créer directement une commande pour ce produit sans obliger le visiteur à passer par le panier.

## 9. Panier

Le panier doit fonctionner sans compte client, via session Django.

Fonctions :

- ajouter un produit avec une quantité
- modifier la quantité depuis le panier
- supprimer un produit
- afficher sous-total de chaque ligne
- afficher total général
- conserver le panier pendant la session
- icône/badge du nombre d'articles dans le header

Lors de la validation d'une commande depuis le panier, demander uniquement :

- nom complet
- numéro de téléphone
- adresse

Ne redemande pas les quantités puisque celles-ci sont déjà définies dans le panier.

Après création de commande :

- vider le panier
- afficher une page/message de confirmation propre
- générer un numéro/référence de commande lisible

## 10. Commandes

Créer des modèles `Order` et `OrderItem`.

`Order` doit contenir au minimum :

- référence unique
- nom complet du client
- téléphone
- adresse
- statut
- total
- date de création
- date de mise à jour

Statuts minimum :

- `preparation`
- `delivered`

Tu peux ajouter `new` ou `cancelled` si utile, mais ne complique pas inutilement.

`OrderItem` doit contenir :

- commande
- produit
- nom du produit au moment de la commande
- prix unitaire au moment de la commande
- quantité
- sous-total

Les anciennes commandes doivent rester cohérentes même si le prix du produit change ensuite.

## 11. Notification email de nouvelle commande

À chaque nouvelle commande, envoyer automatiquement un email au propriétaire indiquant qu'une nouvelle commande vient d'être reçue.

L'email doit inclure :

- référence de commande
- nom client
- téléphone
- adresse
- articles commandés
- quantités
- total
- date/heure

Utiliser SMTP avec mot de passe d'application.

Toutes les informations SMTP doivent venir des variables d'environnement :

```env
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=
OWNER_ORDER_EMAIL=
```

Ne jamais écrire un mot de passe d'application directement dans le code.

L'échec temporaire d'envoi d'email ne doit pas annuler une commande déjà enregistrée. Journaliser proprement l'erreur.

## 12. Espace propriétaire / dashboard

Créer une authentification privée uniquement pour le propriétaire.

Prévoir :

- page de connexion moderne
- déconnexion protégée
- aucun bouton d'inscription publique

Dashboard avec KPIs :

- nombre total de produits actifs
- nombre total de commandes
- nombre de commandes en préparation
- nombre de commandes livrées
- chiffre d'affaires total des commandes livrées
- chiffre d'affaires des 30 derniers jours si simple à calculer
- nombre de commandes du jour

Ajouter des graphiques simples avec Chart.js via CDN uniquement si cela apporte une vraie valeur, sinon rester sur des KPI cards et tableaux propres.

Pages privées :

- liste produits
- créer produit
- modifier produit
- supprimer/désactiver produit avec confirmation
- liste commandes
- détail commande
- changer statut commande en préparation/livrée
- réglages du compte/propriétaire

## 13. Réglages propriétaire

Créer un modèle ou une configuration `SiteSettings` permettant de modifier depuis le dashboard :

- nom de la boutique
- texte de présentation
- numéro WhatsApp affiché publiquement
- email de contact si nécessaire
- adresse ou informations complémentaires si nécessaire

Initialiser le numéro avec :

```text
70 207 39 07
```

Le propriétaire doit pouvoir modifier ces informations sans toucher au code.

## 14. URL publique et bouton Copier

Dans la liste des produits du dashboard :

- chaque produit affiche son URL publique complète
- ajouter un bouton `Copier le lien`
- utiliser `navigator.clipboard.writeText(...)`
- afficher un petit feedback visuel du type `Lien copié`

Le lien doit pointer directement vers la fiche publique du produit via son slug.

## 15. Sécurité et comportement du cache

Point important : après déconnexion, si l'utilisateur utilise le bouton Retour du navigateur, il ne doit jamais revoir une page privée exploitable depuis le cache.

À mettre en place :

- protection `login_required`
- redirection propre si session expirée
- headers anti-cache sur les vues privées : `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`, `Pragma: no-cache`, `Expires: 0`
- middleware ou décorateur réutilisable pour les pages privées
- logout en POST uniquement
- rotation/invalidation correcte de session
- CSRF actif partout

Avant toute déconnexion, afficher une popup/modal de confirmation :

- `Voulez-vous vraiment vous déconnecter ?`
- boutons `Annuler` et `Se déconnecter`

Après déconnexion, rediriger vers la page de connexion.

## 16. UX et validation

- messages Django pour succès/erreurs
- validation serveur de tous les formulaires
- validation front légère en complément
- numéro téléphone nettoyé/validé raisonnablement
- quantité minimum = 1
- pas de quantité négative ou zéro
- erreurs utilisateur compréhensibles
- boutons désactivés pendant soumission si nécessaire pour éviter les doubles commandes
- pagination des produits et commandes côté dashboard si les listes deviennent longues
- états vides propres
- page 404 personnalisée
- page 500 personnalisée si possible

## 17. SEO basique

- titres de pages corrects
- meta description
- URLs propres
- slug produit
- balises alt sur les images
- Open Graph minimal sur les fiches produit si simple
- `robots.txt` et `sitemap.xml` si cela reste simple

## 18. Favicon et branding

Créer :

- favicon `.ico` ou `.png`
- apple touch icon si simple
- logo utilisé proprement dans le header et la page de connexion

Le favicon doit être dérivé visuellement de l'emblème du logo fourni, pas d'une icône générique.

## 19. Fichiers de projet obligatoires

Créer au minimum :

```text
README.md
AGENTS.md
agent.md
.env.example
.gitignore
requirements.txt
manage.py
```

`AGENTS.md` et `agent.md` doivent contenir la même ligne directrice pour les agents IA du projet afin d'éviter les refontes inutiles et la consommation excessive de quota.

## 20. README

Le README doit expliquer clairement :

- prérequis
- création/activation de `.venv`
- installation des dépendances
- configuration `.env`
- migrations
- création du superutilisateur/propriétaire
- lancement du serveur
- gestion des fichiers media
- configuration SMTP avec mot de passe d'application
- passage éventuel à PostgreSQL
- commandes Git utiles

## 21. Tests obligatoires

Créer des tests Django pour les points critiques :

- slug unique
- prix promotionnel
- ajout panier
- création commande directe
- création commande depuis panier
- total commande
- changement de statut
- vues privées non accessibles sans connexion
- logout invalide la session
- pages privées renvoient les bons headers anti-cache

Lancer les tests avant de terminer.

## 22. Qualité finale

Avant de terminer :

1. lancer `python manage.py check`
2. lancer les migrations
3. lancer les tests
4. vérifier les pages principales manuellement
5. vérifier mobile et desktop
6. vérifier qu'aucun secret n'est présent dans Git
7. vérifier `.gitignore`
8. vérifier que le logo et le favicon fonctionnent
9. vérifier le parcours complet commande directe
10. vérifier le parcours complet panier
11. vérifier email de notification avec fallback propre en cas d'erreur SMTP
12. vérifier le comportement navigateur après logout + bouton Retour

## 23. Git et dépôt distant

Une fois l'application terminée et vérifiée :

```bash
git init
```

Si aucun remote n'existe :

```bash
git remote add origin git@github.com:YoussouThiombane/shop.git
```

Puis :

```bash
git add .
git commit -m "Build Mbecte Trading ecommerce platform"
git branch -M main
git push -u origin main
```

Si le dépôt distant contient déjà un historique, récupère-le proprement avant de pousser et évite tout `--force` sauf instruction explicite.

Si l'authentification SSH GitHub échoue, ne contourne pas la sécurité : affiche l'erreur exacte et indique les commandes à exécuter après configuration de la clé SSH.

## 24. Règle de travail

Ne me demande pas de valider chaque détail. Prends des décisions raisonnables en respectant strictement ce cahier des charges.

Ne rajoute pas de fonctionnalités non demandées qui compliquent inutilement l'application.

Priorités absolues :

1. parcours commande simple et fiable
2. dashboard propriétaire pratique
3. images produit fluides
4. design clair, premium et humain
5. sécurité authentification/cache
6. code propre et maintenable
7. dépôt Git propre

À la fin, fournis un résumé court :

- architecture créée
- fonctionnalités réalisées
- identifiants/étapes restant à configurer uniquement si nécessaire
- résultat des tests
- statut du push Git
