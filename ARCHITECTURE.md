# Architecture du Sudoku CTC Solver Assistant

Ce document décrit l'architecture complète du site web assistant de résolution de Sudoku CTC.

## Vue d'ensemble

Le projet est composé de deux parties principales :

1. **Backend Python** : API Flask qui expose le solveur Python
2. **Frontend Web** : Interface HTML/CSS/JavaScript interactive

```
┌────────────────────────────────────────────────────────┐
│                     Frontend (Browser)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Setup Mode  │  │ Solver Mode  │  │  Grid View   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────────────────────────────────────────┘
                            │
                         HTTP/JSON
                            │
┌────────────────────────────────────────────────────────┐
│                    Backend (Flask API)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Board Mgmt  │  │   Solvers    │  │ Constraints  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────────────────────────────────────────┘
                            │
                      Python Solver
                            │
┌────────────────────────────────────────────────────────┐
│                   Core Solver Engine                   │
│       Board → Solver → Strategies → Constraints        │
└────────────────────────────────────────────────────────┘
```

## Architecture Backend (Flask API)

### Fichier : `src/api.py`

Le backend expose une API REST qui permet de :

#### Endpoints principaux

1. **`POST /api/board/new`**
   - Crée une nouvelle grille de Sudoku
   - Corps de requête : configuration JSON de la grille
   - Retourne : `board_id` et état initial de la grille

2. **`GET /api/board/<board_id>`**
   - Récupère l'état actuel d'une grille
   - Retourne : état complet de la grille

3. **`PUT /api/board/<board_id>/cell`**
   - Met à jour une cellule (valeur ou candidats)
   - Corps : `{pos, value?, candidates?}`
   - Utilisé pour l'édition manuelle en mode solver

4. **`POST /api/board/<board_id>/solve/step`**
   - Exécute une étape de résolution
   - Corps : `{solver_type: "simple" | "composite" | "backtracking"}`
   - Retourne : changements effectués, logs détaillés, état de résolution

5. **`GET /api/board/<board_id>/logs`**
   - Récupère l'historique complet des logs

6. **`GET /api/constraints`**
   - Liste toutes les contraintes disponibles
   - Utilisé pour peupler l'interface de création

### Gestion d'état

```python
boards: dict[str, Board] = {}          # Stockage en mémoire des grilles actives
board_logs: dict[str, list[dict]] = {} # Historique des actions
```

⚠️ **Note** : En production, utiliser Redis ou une base de données pour la persistence.

### Système de logs

Chaque action de résolution génère un log structuré :

```python
{
    "solver": "NomDeLaStrategie",
    "changed": True/False,
    "changes": [
        {
            "type": "value_set" | "candidates_eliminated",
            "pos": "a1",
            "value": 5,  # si value_set
            "eliminated": [2, 3],  # si candidates_eliminated
            "remaining": [1, 4, 5]
        }
    ]
}
```

Ce système permet de :

- Tracer exactement ce qui a changé à chaque étape
- Afficher des explications visuelles dans le frontend
- Débugger les stratégies de résolution

## Architecture Frontend

### Structure des fichiers

```
site/
├── index.html          # Structure HTML principale
├── css/
│   └── style.css       # Styles complets avec animations
└── js/
    └── app.js          # Logique applicative complète
```

### Modes d'utilisation

#### 1. Setup Mode (Mode Configuration)

**Objectif** : Créer et configurer une grille avec ses contraintes

**Fonctionnalités** :

- Sélection de contraintes dans une liste
- Sélection visuelle de cellules sur la grille
- Ajout de contraintes à la grille
- Import/Export JSON
- Effacement de la grille

**Workflow** :

```
1. Sélectionner un type de contrainte (Knight, Killer, etc.)
2. Cliquer sur les cellules concernées (elles deviennent jaunes)
3. Cliquer "Add Constraint to Board"
4. Les contraintes actives apparaissent dans la liste à droite
5. Exporter la configuration en JSON pour la réutiliser
```

#### 2. Solver Mode (Mode Résolution)

**Objectif** : Résoudre la grille pas à pas avec logs détaillés

**Fonctionnalités** :

- Sélection du type de solveur (Simple / Composite / Backtracking)
- Exécution step-by-step
- Exécution automatique complète
- Édition manuelle des cellules entre les steps
- Logs détaillés avec visualisation des changements
- Reset à l'état initial
- Statut de la grille (valid/solved)

**Workflow** :

```
1. Passer en Solver Mode (sauvegarde automatique de l'état initial)
2. Choisir le type de solveur
3. Cliquer "Execute Step" pour avancer d'un pas
4. Observer :
   - Les cellules qui changent (vert = valeur placée, rouge = candidats éliminés)
   - Les logs détaillés dans le panneau de droite
   - Le statut Valid/Solved/Steps
5. Entre deux steps, cliquer sur une cellule pour éditer manuellement
6. Continuer jusqu'à résolution ou blocage
```

### État de l'application (JavaScript)

```javascript
state = {
    mode: 'setup' | 'solver',
    boardId: string,              // ID unique de la grille côté backend
    board: Object,                // État complet de la grille
    initialBoard: Object,         // Snapshot au moment du passage en solver mode
    selectedCells: string[],      // Cellules sélectionnées en setup mode
    selectedConstraint: Object,   // Type de contrainte sélectionné
    constraints: Object[],        // Liste des types de contraintes disponibles
    stepCount: number            // Nombre de steps exécutés
}
```

### Communication Frontend-Backend

Toutes les communications utilisent `fetch()` avec JSON :

```javascript
// Exemple : exécuter un step
const response = await fetch(`${API_BASE}/board/${boardId}/solve/step`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ solver_type: 'composite' })
});
const data = await response.json();
// data contient : {changed, solved, board, log}
```

## Visualisation des changements

### Système de highlighting

Quand un step est exécuté, les cellules modifiées sont temporairement mises en évidence :

- **Vert (classe `changed`)** : Une valeur a été placée
- **Rouge (classe `eliminated`)** : Des candidats ont été éliminés

Animation CSS :

```css
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
```

Le highlighting disparaît après 1 seconde.

### Affichage des cellules

**Cellule remplie** :

```html
<div class="cell">
    <div class="cell-value">5</div>
</div>
```

**Cellule avec candidats** :

```html
<div class="cell">
    <div class="cell-candidates">
        <div class="candidate">1</div>
        <div class="candidate">2</div>
        <div class="candidate"></div>
        <!-- 3x3 grid -->
    </div>
</div>
```

### Logs visuels

Chaque step génère une entrée de log avec :

- **En-tête** : "Step N: NomDeLaStrategie"
- **Liste des changements** :
  - ✓ A1: Set value 5 (vert)
  - ✗ B2: Eliminated 2, 3, 4 (rouge)

Les logs sont affichés en ordre inverse chronologique (plus récent en haut).

## Gestion des contraintes

### Format JSON des contraintes

Les contraintes sont stockées dans le JSON de la grille :

```json
{
    "size": 9,
    "cells": {"a1": [1,2,3], "a2": [5], ...},
    "constraint": [
        {
            "type": "knight",
            "cells": []  // Global constraint
        },
        {
            "type": "killer",
            "cells": ["a1", "a2", "b1"],
            "sum": 15
        },
        {
            "type": "palindrome",
            "cells": ["a1", "b2", "c3", "d4"]
        }
    ]
}
```

### Types de contraintes supportées

Voir `src/solver/constraints/factory.py` pour la liste complète :

- **bishop** : Les cellules en diagonale (mouvement fou d'échecs)
- **clone** : Zones identiques
- **clone_zone** : Zones clonées avec rotation/symétrie
- **dutch** : Whispers hollandais (différence ≥ 4)
- **german** : Whispers allemands (différence ≥ 5)
- **greater_than** : Relation d'ordre entre cellules
- **killer** : Somme de cellules
- **king** : Mouvement du roi d'échecs
- **knight** : Mouvement du cavalier d'échecs
- **kropki** : Points noirs/blancs (consécutif/double)
- **palindrome** : Ligne palindromique
- **parity** : Parité (pair/impair)
- **universal** : Toutes les contraintes de position
- **x_v** : Somme X (10) ou V (5)

## Solveurs disponibles

### 1. Simple Solver

- Exécute uniquement `EliminationStrategy`
- Élimine les candidats évidents basés sur les régions
- Rapide mais limité

### 2. Composite Solver (Recommandé)

- Exécute toutes les stratégies dans l'ordre :
  1. Elimination
  2. Hidden Singles
  3. Naked/Hidden Pairs/Triples/Quads
  4. Constraint-specific elimination
  5. X-Wing / W-Wing
  6. Chain Violation Guard
- Boucle jusqu'à ce qu'aucune stratégie ne fasse plus de progrès
- Puis bascule sur Backtracking si nécessaire

### 3. Backtracking Solver

- Force brute avec backtracking
- Garantit de trouver une solution si elle existe
- Peut être lent sur les grilles complexes
- Ne génère pas de logs détaillés des déductions logiques

## Flux de données complet

### Création d'une grille

```
Frontend                    Backend                     Core
   │                           │                          │
   │───New Board (JSON)───────>│                          │
   │                           │───Board.from_dict()─────>│
   │                           │<──Board instance─────────│
   │                           │───serialize_board()─────>│
   │<──{board_id, board}───────│                          │
```

### Exécution d'un step

```
Frontend                    Backend                     Core
   │                           │                          │
   │──Solve Step──────────────>│                          │
   │  {solver_type}            │───Create Solver─────────>│
   │                           │───solver.apply(board)───>│
   │                           │                          │──Strategy loop
   │                           │                          │──Modify board
   │                           │<─changed: bool───────────│
   │                           │                          │
   │                           │──calculate_changes()────>│
   │<──{changed, board, log}───│                          │
   │                           │                          │
   │──Render grid + logs───────│                          │
   │──Highlight changes────────│                          │
```

## Formats de données

### Position des cellules

Format : `lettre minuscule + chiffre`

- Exemples : `a1`, `b5`, `i9`
- `a1` = rangée 0, colonne 0
- `i9` = rangée 8, colonne 8

### État d'une cellule (API)

```json
{
    "row": 0,
    "col": 0,
    "pos": "a1",
    "value": null | 1-9,
    "candidates": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "is_filled": false
}
```

### État complet d'une grille

```json
{
    "size": 9,
    "cells": [/* 81 cellules */],
    "constraints": [/* liste des contraintes */],
    "is_solved": false,
    "is_valid": true
}
```

## Extensions futures possibles

### Setup Mode

- [ ] Drag & drop pour les contraintes linéaires (palindrome, whispers)
- [ ] Preview visuel des contraintes avant ajout
- [ ] Bibliothèque de puzzles prédéfinis
- [ ] Validation de la grille (uniqueness check)

### Solver Mode

- [ ] Mode "hint" : suggérer la prochaine étape sans l'appliquer
- [ ] Historique avec undo/redo
- [ ] Comparaison de performances entre solveurs
- [ ] Export des logs en format texte
- [ ] Mode "explain" : explication détaillée de chaque déduction

### Backend

- [ ] Websockets pour le suivi en temps réel
- [ ] Base de données pour persistence des grilles
- [ ] Système de partage de grilles (URLs)
- [ ] API d'authentification pour sauvegarder des favoris

## Points d'attention

### Performance

- Les grilles sont stockées en mémoire côté backend (limite : RAM)
- Pas de nettoyage automatique des vieilles sessions
- Le mode auto-solve est limité à 100 steps pour éviter les boucles infinies

### Sécurité

- CORS activé (à restreindre en production)
- Pas d'authentification (à ajouter pour une version publique)
- Validation des inputs JSON à améliorer

### Compatibilité

- Requiert un navigateur moderne (ES6+)
- Testé sur Chrome/Firefox/Edge
- Responsive jusqu'à 768px

## Dépendances

### Backend

```
flask>=3.0.0
flask-cors>=4.0.0
loggerplusplus
pygame  (pour GUI locale)
```

### Frontend

Aucune dépendance externe (Vanilla JS)

## Structure des logs

Les logs sont cruciaux pour comprendre le processus de résolution. Voici leur structure détaillée :

### Format d'un log complet

```python
{
    "action": "solve_step",
    "timestamp": "2024-01-01T12:00:00",
    "solver": "HiddenSingleStrategy",
    "changed": True,
    "changes": [
        {
            "type": "value_set",
            "pos": "a1",
            "value": 5,
            "old_candidates": [5, 7, 9],
            "reason": "Hidden single in row0"
        },
        {
            "type": "candidates_eliminated",
            "pos": "a2",
            "eliminated": [2, 3],
            "remaining": [1, 4, 5, 6],
            "reason": "Naked pair elimination"
        }
    ]
}
```

### Interprétation des logs

- **action** : Type d'action (solve_step, manual_set, etc.)
- **solver** : Nom de la stratégie qui a été appliquée
- **changed** : Booléen indiquant si des modifications ont eu lieu
- **changes** : Liste détaillée de tous les changements
  - **value_set** : Une valeur a été définitivement placée
  - **candidates_eliminated** : Des possibilités ont été éliminées

Cette granularité permet de comprendre exactement pourquoi chaque déduction a été faite.
