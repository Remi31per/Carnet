# Carnet & Actions — notes pour Claude

App de recettes et de menus pour un couple en Suisse romande, utilisée sur iPhone (ajoutée à l'écran d'accueil).
Adresse : https://remi31per.github.io/Carnet/ — hébergée par GitHub Pages depuis la branche `main`, dossier racine.
Toujours répondre en français.

## Règle de travail : noter chaque changement
Quand l'utilisateur change une règle ou une attente, ou demande une modification durable, la noter **dans la même demande** :
- règles de repas, goûts, favoris, exclusions → `data/preferences.json` (et mettre à jour le résumé en bas de ce fichier) ;
- fonctionnement de l'app, format des données, façon de travailler, tâche programmée → ce fichier `CLAUDE.md`.
Puis committer et pousser sur `main`. Sinon le changement reste dans la conversation et est oublié la fois suivante.

## Fichiers
- `index.html` : toute l'app (HTML, CSS, JS dans un seul fichier). Pas de build.
- `manifest.webmanifest`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` : installation sur l'écran d'accueil. Après un changement d'icône, incrémenter `?v=` dans `index.html` et le manifest.
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
Tâche programmée Claude « Actions Carnet », lundi et jeudi à 9 h 46 (Europe/Zurich) :
- lundi et jeudi : met à jour `promos.json` et `semaine.json` depuis rappn.ch (Migros, Lidl, Aldi, Denner ; canton de Vaud) ;
- jeudi : prépare deux menus (Menu 1 et Menu 2) pour la semaine suivante dans `menus.json` et ajoute les nouvelles recettes « claude ».

## Règles du foyer (résumé ; `preferences.json` fait foi)
- 2 personnes. Midis en tupperware : 3 fournées de 4 portions (Lun–Mar, Mer–Jeu, Ven), réchauffage au micro-ondes, toujours des légumes.
- Midi : pas d'os, pas de purée, pas de tofu, surtout poulet (filet) et viande hachée, porc possible. Pâtes courtes plutôt que spaghetti.
- Butternut : au plus un plat par menu. Soirs : 15 min de préparation au plus. En général, peu de préparation active.
- Viande suisse uniquement dans les actions, sauf produits industriels panés.
- Cuisines : méditerranéenne, italienne, asiatique, suisse. Inspirations listées dans `preferences.json` ; pas d'influenceurs sauf Le Riz Jaune.
