# PRD: CTC Sudoku Solver

## 1) Resume executif
Un outil web interactif pour resoudre des sudokus CTC avec un large support de contraintes, une UI riche, et plusieurs niveaux d'aide. Le produit doit etre tres simple a installer et agreable a utiliser, avec un mode local-only.

## 2) Contexte et probleme
- Les sudokus CTC ont de nombreuses contraintes; les outils existants sont difficiles a configurer et manquent d'aide progressive.
- L'utilisateur veut une UI interactive qui permet des iterations rapides sur les contraintes et une assistance a la resolution.

## 3) Objectifs
- Setup local ultra simple.
- Resolution agreable avec assistance multi-niveaux.
- Support complet des contraintes MVP (toutes celles listees dans le brief et celles deja implementees ailleurs dans le projet).
- Mode local-only (front + backend local).

## 4) Utilisateurs cibles
- Primaire: createur/resolveur CTC (utilisateur principal).
- Secondaire (optionnel): autres fans CTC via partage/import.

## 5) Portee MVP
### In scope
- UI de grille interactive: edition, annotations, candidats, erreurs.
- Configuration visuelle des contraintes (ajout, edition, suppression).
- Aide multi-niveaux:
  - "Accompagnement": s'applique a chaque changement et guide en continu.
  - "Step by step": resolution pas a pas.
  - "Full solution": resolution complete.
  - (Note: niveaux implementes comme classes heritant de Solver.)
- Import/export JSON suivant `board.example.json`.
- Interactions indispensables: overlays, drag/drop, hotkeys, auto-candidats, etc.
- Setup tres simple (idealement un seul command/script).

### Out of scope (MVP)
- Comptes, cloud hosting, bibliotheque communautaire.
- Generation de puzzle.
- Validation schema JSON.

## 6) Exigences fonctionnelles
### UI / UX
- Grille editable avec candidats et annotations.
- Interface simple et rapide a prendre en main.
- Ajout de contraintes par interaction directe (overlay/drag/drop).
- Raccourcis clavier pour accelerer la saisie.

### Constraints
- Support complet des contraintes prioritaires CTC mentionnees dans le brief, plus celles deja implementees ailleurs dans le codebase.

### Aide / Solver
- API d'aide avec 3 niveaux (accompagnement, step-by-step, full solution).
- Chaque niveau est une classe qui herite de `Solver`.
- Les niveaux doivent etre interchangeables dans l'UI.

### Import/Export
- Lecture/ecriture au format JSON defini par `board.example.json`.
- Pas de validation schema pour le MVP.

## 7) Exigences non fonctionnelles
- UI reactive (reponse < 200 ms sur actions courantes).
- Navigation fluide sur navigateur desktop (Chrome/Firefox/Edge).
- Lancement local simple (ex: script unique).
- Installation locale simple (README + script/commande).

## 8) Donnees et formats
- Source de verite: JSON `board.example.json`.
- Aucune base de donnees pour le MVP.

## 9) Architecture et API
### Etat actuel
- Aucun endpoint existant.

### Besoins
- API "commandes" (actions de resolution).
- API "etat" (snapshot de grille/contraintes/solver).

### Proposition d'API (local-only)
Base URL: `http://127.0.0.1:8000`

#### API "etat"
- `GET /api/state`
  - Retourne l'etat complet: grille, candidats, annotations, contraintes, mode d'aide, historique minimal.
  - Reponse:
    - `grid`: valeurs 9x9 (0 pour vide)
    - `candidates`: liste par cellule
    - `notes`: annotations utilisateur
    - `constraints`: liste des contraintes avec leurs parametres
    - `helpMode`: `guide` | `step` | `full`
    - `dirty`: bool (modifie depuis dernier solve)

- `GET /api/constraints`
  - Retourne la liste des types de contraintes supportees + schema UI minimal.

- `GET /api/board`
  - Export JSON conforme au schema `board` (section "Schema JSON").

#### API "commandes"
- `POST /api/board/import`
  - Body: JSON conforme au schema `board` (section "Schema JSON").
  - Remplace l'etat courant.

- `POST /api/grid/set`
  - Body: `{ row, col, value }`
  - Met a jour une cellule.

- `POST /api/candidates/set`
  - Body: `{ row, col, candidates: [int] }`

- `POST /api/notes/set`
  - Body: `{ row, col, notes: string }`

- `POST /api/constraints/add`
  - Body: `{ type, payload }`

- `POST /api/constraints/update`
  - Body: `{ id, payload }`

- `POST /api/constraints/remove`
  - Body: `{ id }`

- `POST /api/solve/guide`
  - Applique l'aide "accompagnement" sur l'etat courant.
  - Reponse: delta minimal + message d'aide.

- `POST /api/solve/step`
  - Applique une deduction unique et renvoie l'explication.

- `POST /api/solve/full`
  - Calcule la solution complete et renvoie la grille resolue + explications optionnelles.

- `POST /api/reset`
  - Reinitialise la grille et les contraintes.

#### Evenements (optionnel si WebSocket)
- `WS /ws/events`
  - Push des deltas d'etat, utile pour l'accompagnement continu.

### Notes d'implementation
- Toutes les commandes renvoient aussi un `stateDelta` pour eviter un refresh complet.
- Les endpoints restent simples pour une UI tres reactive.

### Format `stateDelta`
Objectif: decrire uniquement les changements depuis le dernier etat.
Exemple:
```json
{
  "grid": [{ "row": 3, "col": 4, "value": 7 }],
  "candidates": [{ "row": 3, "col": 4, "set": [1,3,7], "clear": [2,4] }],
  "notes": [{ "row": 2, "col": 5, "text": "unique" }],
  "constraints": {
    "added": [{ "id": "c-12", "type": "Thermo", "payload": { "cells": [[1,1],[1,2]] } }],
    "updated": [{ "id": "c-03", "payload": { "cells": [[2,2],[2,3]] } }],
    "removed": ["c-08"]
  },
  "help": { "message": "Only 7 fits in r4c5", "rule": "single" }
}
```

### Schema JSON (proche du format cible)
Format de board recommande:
```json
{
  "size": 9,
  "cells": {
    "a1": [1,2,3,4,5,6,7,8,9],
    "a2": [1,2,3]
  },
  "constraints": [
    { "type": "bishop", "cells": ["a1","b2"] },
    { "type": "clone", "cells": ["a1","d4","f8"] },
    { "type": "parity", "cell": "a1", "rest": "1" },
    { "type": "greater_than", "higher_value_cell": "a2", "lower_value_cell": "a1" },
    { "type": "killer", "cells": ["a1","b2"], "sum": 15 },
    { "type": "knight" },
    { "type": "king" },
    { "type": "kropki", "cell1": "a1", "cell2": "a2", "color": "black" },
    { "type": "x_v", "cell1": "a1", "cell2": "a2", "sum": "10" }
  ]
}
```
- `cells` mappe les coordonnees (ex: `a1`) vers les candidats possibles.
- `constraints` est une liste d'objets typés avec des champs variables.
- Les champs specifiques (ex: `sum`, `color`, `higher_value_cell`) sont propres au type.
- `constraints` remplace `constraint`.

### Critères d'acceptation (endpoints)
- `GET /api/state`: retourne un etat complet coherent (grille + candidats + contraintes) en < 200 ms.
- `GET /api/constraints`: liste tous les types supportes + champs requis pour `payload`.
- `GET /api/board`: export strictement compatible avec `board.example.json`.
- `POST /api/board/import`: remplace l'etat courant; retourne `stateDelta` vide ou etat complet.
- `POST /api/grid/set`: met a jour la cellule; candidats auto-ajustes si active.
- `POST /api/candidates/set`: remplace les candidats de la cellule cible.
- `POST /api/notes/set`: met a jour l'annotation de cellule.
- `POST /api/constraints/add`: ajoute une contrainte avec `id` unique.
- `POST /api/constraints/update`: modifie uniquement le `payload` cible.
- `POST /api/constraints/remove`: supprime la contrainte et nettoie l'UI.
- `POST /api/solve/guide`: renvoie un `help.message` + delta d'etat.
- `POST /api/solve/step`: applique exactement une deduction.
- `POST /api/solve/full`: renvoie la grille resolue + explication optionnelle.
- `POST /api/reset`: reinitialise grille, candidats, notes, contraintes.
- `WS /ws/events` (si active): emet chaque `stateDelta` des commandes.

## 10) Risques
- Scope creep du nombre de contraintes.
- Complexite UI + performance du solveur.
- Couplage UI/solver et latence du backend local.

## 11) Metriques de succes
- Setup < 10 min.
- First hint < 60 s.
- 100% des contraintes MVP supportees.
- Un puzzle CTC complexe resolu entierement via l'UI.

## 12) Milestones (proposes)
1) Schema JSON + import/export OK.
2) UI grille interactive + contraintes basiques.
3) API commandes/etat + solver branche.
4) Niveaux d'aide + resolution assistée.
5) Packaging + lancement local simplifie.

## 13) Questions ouvertes
- Definition precise des endpoints "commandes" et "etat".
- Definition precise du mode "accompagnement" (granularite, messages, declencheurs).
