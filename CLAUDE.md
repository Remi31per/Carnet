# Carnet de repas — notes pour Claude

Nom affiché dans l'app : « Carnet de repas » (anciennement « Carnet & Actions » ; le dépôt et l'adresse restent « Carnet »).

App de recettes et de menus pour un couple en Suisse romande, utilisée sur iPhone (ajoutée à l'écran d'accueil).
Adresse : https://remi31per.github.io/Carnet/ — hébergée par GitHub Pages depuis la branche `main`, dossier racine.
Toujours répondre en français.

## Règle de travail : noter chaque changement
Quand l'utilisateur change une règle ou une attente, ou demande une modification durable, la noter **dans la même demande** :
- règles de repas, goûts, favoris, exclusions → `data/preferences.json` (et mettre à jour le résumé en bas de ce fichier) ;
- fonctionnement de l'app, format des données, façon de travailler, tâche programmée → ce fichier `CLAUDE.md`.
Puis committer et pousser sur `main`. Sinon le changement reste dans la conversation et est oublié la fois suivante.

## Fichiers
- `index.html` : toute l'app (HTML, CSS, JS dans un seul fichier). Pas de build. Un bouton flèche « Revenir en haut » (`#totop`, en bas à droite) apparaît dès qu'on a défilé de 500 px ; le garder.
  Apparence : une seule police douce, **Nunito**, partout. **Thème automatique par défaut : mode nuit de 19 h à 7 h, mode jour le reste du temps** ; options Automatique / Nuit / Jour dans Favoris → Affichage (clé `themeMode` dans le téléphone). Mode nuit en tons assez clairs (fond `#1F2924`, cartes `#2A3530`, texte ivoire) ; ne pas revenir aux couleurs sombres d'avant.
  **Style « variante 2 : tuiles en relief, palette feuillage »** (choisi par l'utilisateur le 01.11.2026 parmi 5 maquettes ; planche d'inspiration dans le projet Claude « App menus ») :
  - Palette : **vert forêt `#134B42` (principal)**, sauge `#80917D` (tuile des midis), moutarde `#EEA83B` (onglet actif, badge « Nouvelle idée », point du menu choisi), terracotta `#CA763B` (prix, « en action », compteurs), tilleul `#AEBA8A` (légumes, textes clairs), ivoire `#F1E8D6`. Fond du mode jour `#EAE3D3`, cartes `#F4EFE3`. Variables `--forest --sage --must --terra --lime --ivory`.
  - **Relief doux** partout (ombre claire en haut à gauche, ombre sombre en bas à droite : `--shadow`, `--glow`, `--press` pour les éléments creusés), pas de bordures.
  - **En-tête** (identique sur tous les onglets) : tuile vert forêt **à bas en biais (forme d'origine) avec les quatre coins arrondis** (deux pseudo-éléments `::before`/`::after`, celui du bas incliné), titre « Carnet de repas » en ivoire, date limite des actions, et à droite **l'illustration du chef au wok** (symbole SVG `#f-wok`, dessin maison) ; **bouton Actualiser rond, entier, à cheval sur le bord bas** (il dépasse à moitié du bandeau).
  - **Onglets Recettes, Actions, Favoris, Ajouter** : tout le contenu dans une grande tuile de couleur propre à l'onglet (`.tabtile`), les cartes claires ressortent dessus : Recettes tilleul `.t-rec`, Actions terracotta `.t-act`, Favoris moutarde `.t-fav`, Ajouter vert sapin `.t-add` (versions plus sombres en mode nuit). Le Menu garde ses deux tuiles (sauge et ivoire).
  - Filtres des recettes : « Toutes », « Rapides · 15 min », « Nôtres · midis », « Nôtres · soirs », « Nôtres · weekend », « Idées de Claude », en **3 lignes de 2**. Badge « Notre plat » / « Idée de Claude » (pas « Ma recette » ni « Les miennes »).
  - **Menu** : grand sélecteur Menu 1 / Menu 2 creusé (le menu choisi ressort, avec son thème), puis une **tuile sauge des midis** (une grande carte par fournée : jours, moment de cuisine, plat, badge, temps prép. + cuisson, portions, actions, légumes favoris, conseil) et une **tuile ivoire des 5 soirs** (lun–ven, badge, temps, actions, conseil). Pas de bloc récapitulatif des actions sur le Menu. **Pastille illustrée par plat** (`dishArt` → `DA`) : petite image composée (contenant : assiette, bol, planche, poêle, plat à gratin, grill + **aliment principal du plat** : filet de poulet, pilons, boulettes, steak, saumon, poisson, pâtes, lasagne, pizza, tarte, omelette, etc. + accompagnements et garniture). Composition fixée par recette dans `SPEC` (clé = id) ; pour une nouvelle recette, l'ajouter à `SPEC` (sinon `guess()` la déduit du titre). **Chaque pastille doit être unique et cohérente avec le plat.**
  - **Bloc d'humour en bas du Menu** (`#funBox`, `FUNS` en JS) : une illustration rigolote d'aliment + une phrase, **tirée au hasard à chaque actualisation générale** (`pickFun()` dans `loadAll`). Inspiration : lot 5 de la planche (aliments personnifiés en aplats, humour léger). Dessins maison uniquement : jamais de personnages connus (dessins animés, marques) ni de vraies personnes. On peut ajouter d'autres illustrations dans `FUNS` (symboles `#f-…`).
  - **Mode nuit** : fond `#24302A`, cartes `#313D37` ; les blocs ont des **contours éclairés** (liseré clair en haut, fin contour ivoire, léger dégradé lumineux depuis le haut) pour bien voir les blocs et leurs séparations. Ne pas l'assombrir.
  - Pas de bandeau « Mode lecture » en haut de page (seuls les messages d'erreur s'affichent dans `#status`).
  - Pastilles à choix (filtres, magasins, favoris) : **effet 3D** en mode jour (bombées, liseré clair en haut, ombre portée en dessous, légèrement enfoncées au toucher), pas de halo blanc.
  - **Toucher l'onglet où l'on est déjà ramène tout en haut** de la page.
  - **Cœur + (`.favadd`, `adoptRecipe`)** sur chaque idée de Claude (cartes Recettes, plats « Nouvelle idée » du Menu, fiche du plat) : la recette passe en `source: "moi"` (+ `adoptedFrom: "claude"`, `adoptedAt`), garde son id, et ne sera donc plus retirée chaque semaine. **Un nouveau toucher sur le cœur (devenu rouge et plein) annule**, tant qu'on est dans la même semaine d'idées (adoption depuis le dernier jeudi) : la recette redevient `source: "claude"` et `adoptedFrom`/`adoptedAt` sont retirés.
  - **Décorations de fête du bandeau** (`festiveFor`, `applyFestive`) : 21 octobre « Joyeux anniversaire Cindy ! » et 25 août « Joyeux anniversaire Rémi ! » (fanions, confettis, ballons) ; 24 et 25 décembre (guirlande de sapin, boules, neige, étoile) ; 31 décembre et 1er janvier (feux d'artifice, étoiles, « Bonne année AAAA ! »). Aperçu possible avec `?fete=cindy|remi|veille|noel|reveillon|nouvelan` dans l'adresse.
  - Barre d'onglets vert forêt flottante en bas, onglet actif en bloc moutarde. Icônes au trait (sprite `#i-…`, helper `ic(nom)`). Garder ce style pour tout nouvel élément.
  **Fenêtre du bas** (bottom sheet, `openSheet(html)` / `closeSheet()`) : se ferme avec la croix, en touchant le fond, ou en glissant vers le bas. Utilisée pour : la recette d'un plat touché dans le Menu (`showRecipe` : ingrédients à avoir sous forme de liste à cocher, puis la préparation s'il y en a ; nos recettes sans étapes = juste la liste), les actions d'un plat via la pastille « N en action » (`showHits` : toutes les actions à la suite dans une seule fenêtre, avec magasin, produit, prix, rabais, ingrédient concerné, date), et une action seule via la pastille du magasin à côté d'un ingrédient (`showPromo`).
  Recettes : les cartes sont **repliées** (titre, badge, type, temps de préparation, « en action ») et **se déplient d'un toucher** (`S.openCards`).
  Recettes : **deux recherches** dans un même bloc séparé par un trait fin : « Par nom de plat » (titre et mots-clés) et « Par aliment que j'ai » (ingrédients ; plusieurs aliments séparés par une virgule, « et » ou « + », tous requis ; les ingrédients trouvés sont surlignés).
  **À chaque modification de `index.html`, changer `APP_VERSION`** (ex. `2026-11-02a`) : l'app compare sa version à celle publiée (au démarrage, au retour dans l'app et sur « Actualiser ») et se recharge seule si elle diffère, sinon l'iPhone garde l'ancienne page en cache.
- `manifest.webmanifest`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` : installation sur l'écran d'accueil. Après un changement d'icône, incrémenter `?v=` dans `index.html` et le manifest.
- **Recettes ajoutées depuis l'app** : elles sont souvent incomplètes. Claude les complète au fur et à mesure (quantités, ingrédients de base évidents, étapes, cuisson, temps, mots-clés, réchauffage pour un midi), **sans jamais changer ce qu'ils ont saisi**, puis ajoute `completedBy: "claude"` et `updatedAt`. La tâche « Actions Carnet » le fait à chaque exécution ; le faire aussi dans une conversation quand on voit une recette « moi » incomplète sans `completedBy`.
- `data/recettes.json` : objet `{id: recette}`. `source: "moi"` = leurs recettes (ne jamais supprimer sans demande explicite), `source: "claude"` = suggestions (id `c-…`).
  Recette : `{title, source, type: "midi"|"soir"|"weekend", weekend?, servings, prep (min hors cuisson), cuisson (min), time?, tags, reheat? (micro-ondes, plats de midi), ingredients: [{q, n}], steps, notes, inspiration? {nom, url}, saison? {de, a, label}, createdAt, updatedAt?}`
- `data/promos.json` : actions de la semaine `{id: {store, name, format, condition?, price | priceLabel, regular?, pct?, until, cat, origin?, keywords, exclude?}}`.
- `data/menus.json` : `{week, label, intro, options: [{nom: "Menu 1", theme, midi: [{days, when, recipeId, portions, tip?}], soir: [{day, recipeId, tip?, leftover?}], note}, {nom: "Menu 2", …}]}`.
- `data/preferences.json` : favoris (`legumes`, `fruits`, `viandes`), `cuisines`, `regles`, `exclusions`, `viande_suisse`, `poulet`, `variete`, `sources`. Modifiable depuis l'app (onglet Favoris) ; ne le changer que sur demande.
- `data/semaine.json` : `{from, to, updated, week}`.

## Comment l'app lit et écrit
- Sans code d'accès : lecture des fichiers publiés (`data/*.json`).
- Avec un code d'accès GitHub (fine-grained token, dépôt Carnet, Contents en lecture et écriture) enregistré dans le téléphone : lecture et écriture via l'API GitHub (`contents/data/...`). L'app écrit dans `recettes.json` et `preferences.json`.
- Avant de committer des changements de données : `git pull --rebase origin main`, car l'app peut avoir modifié ces fichiers depuis les téléphones.

## Mise à jour automatique
**Robot GitHub « Télécharger les actions des magasins »** (`.github/workflows/actions-magasins.yml`, lundi et jeudi à 7 h 15, lançable à la main dans l'onglet Actions de GitHub) : télécharge les pages d'actions de rappn.ch (Migros, Lidl, Aldi, Denner, canton de Vaud) dans `data/raw/rappn-<magasin>-VD.html`, puis `scripts/extraire_actions.py` les résume dans **`data/raw/actions-brutes.json`** (offres avec nom, marque, prix, ancien prix + texte de la page). Raison : depuis novembre 2026, les tâches Claude ne peuvent plus lire rappn.ch directement (adresse refusée par l'outil de lecture web). Le site ne publie la liste détaillée en ligne que pour Vaud (Fribourg seulement dans son app) ; Lidl, Aldi et Denner ont les mêmes actions partout.

**Depuis le 11.11.2026, les mises à jour se font dans la conversation Claude du projet « App menus »** (celle qui a accès au dépôt), réveillée par un rappel programmé (`send_later`) chaque lundi et jeudi à 8 h 31 ; chaque passage programme le suivant. La tâche programmée « Actions Carnet » est **désactivée** : lancée dans une session neuve, elle n'arrivait pas à accéder au dépôt (arrêt au bout de 2 minutes sans rien publier, 2–10.11.2026). Si un passage manque, demander « mets à jour les actions et les menus » dans le projet.

Ce que fait chaque passage (lundi et jeudi, après le robot), selon le texte de la tâche « Actions Carnet » :
- lundi et jeudi : met à jour `promos.json` et `semaine.json` **à partir de `data/raw/actions-brutes.json`** (vérifier la date `telecharge_le`) pour **nos magasins de Domdidier, Avenches, Payerne et Morat** ;
- à chaque exécution : complète les recettes « moi » ajoutées incomplètes (voir plus haut) ;
- jeudi : **retire toutes les idées de Claude de la semaine d'avant** (recettes `source: "claude"` ; celles adoptées avec le cœur + sont devenues « moi » et restent), **ajoute 15 nouvelles idées** (environ 7 midis, 5 soirs, 3 weekend, champ `week`), puis prépare deux menus (Menu 1 et Menu 2) pour la semaine suivante dans `menus.json`, les nouvelles idées des menus étant prises parmi ces 15.
- Si les actions manquent, la tâche fait quand même les menus du jeudi et le signale.

## Règles du foyer (résumé ; `preferences.json` fait foi)
- 2 personnes. **Soirs et plats du weekend : toujours pour 2 personnes.** Midis en tupperware : 3 fournées de 4 portions (Lun–Mar, Mer–Jeu, Ven), réchauffage au micro-ondes, toujours des légumes.
- Midi : pas d'os, pas de purée, pas de tofu, surtout poulet (filet) et viande hachée, porc possible. Pâtes courtes plutôt que spaghetti.
- Butternut : au plus un plat par menu. Soirs : 15 min de préparation au plus. En général, peu de préparation active.
- Viande suisse uniquement dans les actions, sauf produits industriels panés. Magasins : Domdidier, Avenches, Payerne et Morat.
- Cuisines : méditerranéenne, italienne, asiatique, suisse. Inspirations listées dans `preferences.json` ; pas d'influenceurs sauf Le Riz Jaune.
