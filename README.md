# Carnet & Actions

Notre carnet de recettes, nos menus de la semaine et les actions Migros, Lidl, Aldi et Denner.

- L'app : `index.html`, publiée avec GitHub Pages. À ajouter sur l'écran d'accueil de l'iPhone depuis Safari (Partager → Sur l'écran d'accueil).
- Les données : dossier `data/`.
  - `recettes.json` : toutes les recettes, par identifiant. `source: "moi"` = nos recettes, `source: "claude"` = suggestions.
  - `promos.json` : actions de la semaine (mises à jour par Claude chaque lundi et jeudi).
  - `menus.json` : les deux menus de la semaine (préparés par Claude chaque jeudi).
  - `preferences.json` : favoris, goûts et règles.
  - `semaine.json` : dates de la semaine d'actions.

L'app lit ces fichiers et, avec le code d'accès enregistré sur le téléphone, écrit dans `recettes.json` et `preferences.json`.
