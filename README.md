# Sudoku CTC Solver Assistant

Ce projet fournit un assistant de résolution de Sudoku avec support pour les variantes CTC (Cracking The Cryptic). Il combine un solveur Python puissant avec une interface web interactive permettant de créer des grilles, ajouter des contraintes et résoudre les puzzles pas à pas avec des logs détaillés.

## 🚀 Démarrage rapide

### Installation des dépendances

Installez les dépendances avec [uv](https://github.com/astral-sh/uv) :

```bash
uv sync --group dev
```

### Lancement du site web

Le site web nécessite le backend Flask pour fonctionner. Lancez le serveur API :

```bash
uv run python src/api.py
```

Le serveur démarre sur `http://localhost:5000`

Ouvrez ensuite votre navigateur et accédez à :

```
http://localhost:5000
```

L'interface web devrait s'afficher avec deux modes disponibles : **Setup Mode** et **Solver Mode**.

### Utilisation de la GUI locale (alternative)

Pour utiliser la GUI PyGame locale sans le site web (à lancer depuis la racine du dépôt) :

```bash
uv run python src/main.py
```

Le script charge `board.json`, ajoute une contrainte palindrome codée en dur, puis ouvre une fenêtre PyGame avec le solveur Composite : **Step** exécute une étape, **Run** résout jusqu'au bout (stratégies logiques puis backtracking), et un clic sur une cellule surligne les cellules qu'elle voit.

## 📖 Guide d'utilisation du site web

### Mode Setup (Configuration)

Le mode Setup permet de créer et configurer une grille de Sudoku :

1. **Sélectionner une contrainte** dans la liste à gauche (Knight, Killer, Palindrome, etc.)
2. **Cliquer sur les cellules** de la grille pour les sélectionner (elles deviennent jaunes)
3. **Cliquer sur "Add Constraint to Board"** pour ajouter la contrainte
4. Répéter pour ajouter d'autres contraintes
5. **Exporter la grille** en JSON pour la réutiliser plus tard
6. **Importer une grille** depuis un fichier JSON

### Mode Solver (Résolution)

Le mode Solver permet de résoudre la grille pas à pas :

1. **Basculer en mode Solver** avec le bouton en haut à droite
2. **Choisir le type de solveur** :
   - **Simple** : Seulement l'élimination basique (`EliminationStrategy`)
   - **Composite** : Toutes les stratégies logiques, la première qui modifie la grille est appliquée (recommandé)
   - **Backtracking** : Force brute (stratégies logiques puis essais récursifs)
3. **Cliquer sur "Execute Step"** pour exécuter une étape de résolution
4. **Observer les changements** :
   - Cellules vertes : valeur placée
   - Cellules rouges : candidats éliminés
   - Cellules jaunes : cellule sélectionnée
   - Logs détaillés dans le panneau de droite
5. **Éditer manuellement** entre deux steps en cliquant sur une cellule
6. **Utiliser "Auto Solve"** pour enchaîner les steps automatiquement (100 steps maximum)
7. **Utiliser "Reset to Initial"** pour revenir à l'état de départ

### Logs détaillés

Chaque étape de résolution génère des logs qui montrent :

- Quel solveur a été utilisé (`CompositeSolver`, `BacktrackingSolver` ou `EliminationStrategy`)
- Quelles cellules ont été modifiées
- Quelles valeurs ont été placées
- Quels candidats ont été éliminés

Cela permet de comprendre exactement le raisonnement du solveur. Le nom de la stratégie précise appliquée par le solveur Composite apparaît dans les logs du serveur (console et dossier `logs/`).

## 🏗️ Architecture

Le projet est composé de trois parties :

### 1. Core Solver (Python)

- **Models** : `Board`, `Cell` - représentation de la grille
- **Constraints** : 17 classes de contraintes, dont 14 utilisables via JSON/API (Knight, King, Killer, Palindrome, etc.)
- **Strategies** : 12 stratégies de résolution logique
- **Solvers** : Composite, Backtracking

### 2. Backend API (Flask)

- **Endpoints REST** pour créer/modifier/résoudre des grilles (voir [API REST](#-api-rest))
- **Gestion d'état** des grilles actives (en mémoire, perdue au redémarrage du serveur)
- **Système de logs** détaillé pour chaque action
- **Sérialisation** Board ↔ JSON

### 3. Frontend Web (HTML/CSS/JS)

- **Setup Mode** : interface de création de grilles
- **Solver Mode** : résolution interactive pas à pas
- **Visualisation** : highlighting des changements, grille avec candidats
- **Communication** avec le backend via fetch API
- **Servi par Flask** : `site/` est servi directement par le backend, pas besoin de serveur séparé

Pour plus de détails, consultez [ARCHITECTURE.md](ARCHITECTURE.md).

## 📁 Structure du projet

```plaintext
sudoku_solver/
├── src/
│   ├── api.py                  # Backend Flask API
│   ├── main.py                 # GUI PyGame locale
│   ├── models/
│   │   ├── board.py            # Classe Board
│   │   └── cell.py             # Classe Cell
│   ├── solver/
│   │   ├── solver.py           # Interface Solver
│   │   ├── composite.py        # Composite Solver
│   │   ├── backtracking.py     # Backtracking Solver
│   │   ├── constraints/        # Contraintes
│   │   │   ├── base_constraint.py
│   │   │   ├── factory.py      # Registry des contraintes
│   │   │   ├── structs.py      # Enum ConstraintType
│   │   │   ├── killer.py
│   │   │   ├── knight.py
│   │   │   ├── palindrome.py
│   │   │   └── ...
│   │   └── strategies/         # Stratégies de résolution
│   │       ├── elimination.py
│   │       ├── single_hidden.py
│   │       ├── subset_naked.py
│   │       └── ...
│   └── utils/
│       ├── gui.py              # GUI PyGame
│       └── exceptions.py
├── site/                        # Interface web
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js              # Logique de l'interface et appels API
│       └── constraints.js      # Dessin des contraintes sur la grille
├── tests/                       # Tests unitaires (pytest)
├── test_api.py                  # Script de test manuel de l'API
├── board.json                   # Grille chargée par src/main.py
├── board.example.json           # Illustration du format JSON
├── ARCHITECTURE.md              # Documentation architecture
├── Makefile                     # Formatage, linting, typage
├── pyproject.toml
├── LICENSE
└── README.md
```

## 🌐 API REST

Toutes les routes sont définies dans `src/api.py`. Les grilles sont identifiées par un `board_id` (UUID) renvoyé à la création.

| Méthode | Route | Description |
| ------- | ----- | ----------- |
| `GET` | `/api/constraints` | Liste des types de contraintes disponibles |
| `POST` | `/api/board/new` | Crée une grille (corps JSON optionnel, grille vide 9×9 par défaut), renvoie `board_id` et l'état de la grille |
| `GET` | `/api/board/<board_id>` | État d'une grille (cellules, candidats, contraintes, `is_valid`, `is_solved`) |
| `PUT` | `/api/board/<board_id>/cell` | Modifie une cellule : `{"pos": "a1", "value": 5}` et/ou `{"candidates": [...]}` |
| `POST` | `/api/board/<board_id>/constraint` | Ajoute une contrainte (objet JSON avec `type`) |
| `DELETE` | `/api/board/<board_id>/constraint/<index>` | Supprime la contrainte à l'index donné |
| `POST` | `/api/board/<board_id>/solve/step` | Exécute une étape : `{"solver_type": "simple" \| "composite" \| "backtracking"}` (`composite` par défaut) |
| `GET` | `/api/board/<board_id>/logs` | Historique des steps de résolution |
| `GET` | `/api/board` | Exporte la grille courante au format JSON des grilles |
| `POST` | `/api/board/import` | Importe une grille au format JSON et en fait la grille courante |

Les routes `/` et `/<fichier>` servent l'interface web depuis `site/`.

## 🎯 Contraintes supportées

Contraintes enregistrées dans `src/solver/constraints/factory.py`, utilisables dans le JSON et via l'API :

| Type | Paramètres JSON | Règle |
| ---- | --------------- | ----- |
| `bishop` | `cells` | Les cellules listées contiennent des chiffres tous différents |
| `clone` | `cells` | Les cellules listées contiennent le même chiffre |
| `clone_zone` | `zones` (liste de listes de cellules) | Zones clones : les cellules de même rang dans chaque zone sont identiques |
| `dutch` | `cells` | Whispers hollandais : deux cellules voisines sur la ligne diffèrent d'au moins 4 (l'implémentation actuelle utilise 5, comme `german`) |
| `german` | `cells` | Whispers allemands : deux cellules voisines sur la ligne diffèrent d'au moins 5 |
| `greater_than` | `higher_value_cell`, `lower_value_cell` | Relation d'ordre entre deux cellules adjacentes |
| `killer` | `cells`, `sum`, `color` (optionnel) | Cage : somme imposée, chiffres différents |
| `king` | aucun | Anti-roi : deux cellules à un mouvement de roi ne contiennent pas le même chiffre |
| `knight` | aucun | Anti-cavalier : deux cellules à un mouvement de cavalier ne contiennent pas le même chiffre |
| `kropki` | `cell1`, `cell2`, `color` (`black` ou `white`) | Point noir : l'un est le double de l'autre ; point blanc : chiffres consécutifs |
| `palindrome` | `cells` | La ligne se lit de la même façon dans les deux sens |
| `parity` | `cell`, `rest` (`0` pair, `1` impair) | Parité d'une cellule |
| `universal` | aucun | Cellules occupant la même position dans chaque boîte 3×3, ajoutées comme régions supplémentaires |
| `x_v` (alias `xv`) | `cell1`, `cell2`, `sum` | Somme de deux cellules adjacentes : X (10) ou V (5) |

Contraintes implémentées dans `src/solver/constraints/` mais pas encore enregistrées dans la factory (non utilisables via JSON ou l'API pour le moment) :

- **axia** (`AxiaConstraint`, `cell`) : vérifie que la cellule ne partage pas son chiffre avec les cellules situées sur ses diagonales
- **couple** (`CoupleConstraint`, `cell1`, `cell2`, `same`) : deux cellules adjacentes de même parité (`same: true`) ou de parités différentes
- **friendly_cell** (`FriendlyCellConstraint`, `cell`) : la cellule contient son numéro de ligne, de colonne ou de boîte

## 🧠 Stratégies de résolution

Stratégies définies dans `src/solver/strategies/`, dans l'ordre où le solveur Composite les essaie :

1. **Elimination** : retire la valeur d'une cellule remplie des candidats de ses voisines
2. **Hidden Single** : un chiffre candidat dans une seule cellule d'une région y est placé
3. **Naked Pair**
4. **Hidden Pair**
5. **Constraint** : applique les éliminations propres à chaque contrainte
6. **Naked Triple**
7. **Hidden Triple**
8. **Naked Quad**
9. **Hidden Quad**
10. **X-Wing**
11. **W-Wing**
12. **Chain Violation Guard** : élimine les candidats qui mènent à une contradiction (par backtracking)

Le solveur **Backtracking** applique en boucle les mêmes stratégies, sauf W-Wing et Chain Violation Guard, puis essaie récursivement les candidats de la cellule qui en a le moins.

## 🧪 Tests

Les tests unitaires sont dans `tests/` (configuration pytest dans `pyproject.toml`, avec couverture de `src/models` activée par défaut) :

```bash
uv run pytest                      # Tous les tests de tests/
uv run pytest tests/test_board.py  # Test spécifique
```

`test_api.py`, à la racine, est un script de vérification manuelle de l'API : il n'est pas collecté par `uv run pytest` et nécessite que le serveur tourne sur `http://localhost:5000`.

```bash
uv run python src/api.py   # Terminal 1
uv run python test_api.py  # Terminal 2
```

## 🛠️ Développement

### Formatage et linting

```bash
make format    # Formater le code (isort, black, ruff format)
make lint      # Linter (ruff, pydoclint, pylint)
make typecheck # Vérification de types (mypy)
make check     # lint, puis format, puis typecheck
make all       # Équivalent à make check
make auto      # Relance make all en boucle, sans jamais s'arrêter (Ctrl+C pour sortir)
```

Les outils doivent être disponibles dans le `PATH` (par exemple dans l'environnement virtuel activé). `black` ne fait pas partie du groupe `dev` et doit être installé séparément. `make lint` réécrit `ruff-baseline.txt` et `pylint-baseline.txt`.

`make auto` fonctionne comme une boucle de type « watch » : la cible s'appelle elle-même récursivement après chaque `make all`, sans condition d'arrêt.

### Structure des commits

Ce projet utilise des commits sémantiques avec emojis :

- 🌟 `:sparkles:` Nouvelle fonctionnalité
- 🐛 `:bug:` Correction de bug
- 📝 `:memo:` Documentation
- ♻️ `:recycle:` Refactoring
- 🚧 `:construction:` Travail en cours

## 📊 Format JSON des grilles

Les grilles sont stockées au format JSON :

```json
{
  "size": 9,
  "cells": {
    "a1": [1, 2, 3],
    "a2": [5],
    "b1": [1, 2, 3, 4, 5, 6, 7, 8, 9]
  },
  "constraints": [
    {
      "type": "knight"
    },
    {
      "type": "killer",
      "cells": ["a1", "a2", "b1"],
      "sum": 15
    },
    {
      "type": "palindrome",
      "cells": ["a1", "b2", "c3", "d4", "e5"]
    }
  ]
}
```

Champs obligatoires :

- `size` (entier) : taille de la grille (généralement 9)
- `cells` (objet) : dictionnaire `position -> liste de candidats`

Champs optionnels :

- `constraints` (liste) : contraintes avec leurs paramètres (voir [Contraintes supportées](#-contraintes-supportées)), vide si aucune

Les positions utilisent le format `a1`, où `a` est la ligne 0 et `1` la colonne 0. Les lettres de ligne vont de `a` à `a + size - 1`, les colonnes de `1` à `size`.

Compatibilité : l'API accepte aussi la clé `constraint` à la place de `constraints`, et le type `xv` à la place de `x_v`.

Voir `board.json` pour un exemple complet. `board.example.json` illustre le format de chaque contrainte avec des `...` et n'est pas chargeable tel quel.

## 🔧 Configuration

### Backend

Le backend Flask peut être configuré via les variables :

```python
# src/api.py
app.run(debug=True, port=5000)  # Modifier le port si nécessaire
```

### Frontend

Le frontend appelle l'API sur la même origine que la page (il est servi par Flask) :

```javascript
// site/js/app.js
const API_BASE = `${window.location.origin}/api`;
```

Pour utiliser un backend sur une autre URL, modifier cette constante (CORS est activé côté Flask).

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** : Architecture détaillée du système
- **Docstrings** : Toutes les classes et fonctions sont documentées (style Google)

Générer la documentation HTML :

```bash
uv run pdoc src/models src/solver src/utils -o docs/
```

## 🤝 Contribution

Ce projet suit des standards stricts de qualité :

- Type hints complets (mypy strict mode)
- Docstrings Google style
- Tests unitaires (pytest)
- Formatage automatique (black, isort, ruff)

## 📄 Licence

Voir [LICENSE](LICENSE)

## 🎓 Inspiration

Ce projet s'inspire des puzzles de [Cracking The Cryptic](https://www.youtube.com/c/CrackingTheCryptic) et des outils comme [f-puzzles.com](https://f-puzzles.com/).
