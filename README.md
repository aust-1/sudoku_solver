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

Pour utiliser la GUI PyGame locale sans le site web :

```bash
uv run python src/main.py
```

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
   - **Simple** : Seulement l'élimination basique
   - **Composite** : Toutes les stratégies logiques (recommandé)
   - **Backtracking** : Force brute
3. **Cliquer sur "Execute Step"** pour exécuter une étape de résolution
4. **Observer les changements** :
   - Cellules vertes : valeur placée
   - Cellules rouges : candidats éliminés
   - Logs détaillés dans le panneau de droite
5. **Éditer manuellement** entre deux steps en cliquant sur une cellule
6. **Utiliser "Auto Solve"** pour résoudre automatiquement
7. **Utiliser "Reset to Initial"** pour revenir à l'état de départ

### Logs détaillés

Chaque étape de résolution génère des logs qui montrent :

- Quelle stratégie a été utilisée
- Quelles cellules ont été modifiées
- Quelles valeurs ont été placées
- Quels candidats ont été éliminés

Cela permet de comprendre exactement le raisonnement du solveur.

## 🏗️ Architecture

Le projet est composé de trois parties :

### 1. Core Solver (Python)

- **Models** : `Board`, `Cell` - représentation de la grille
- **Constraints** : 15+ types de contraintes (Knight, King, Killer, Palindrome, etc.)
- **Strategies** : 10+ stratégies de résolution logique
- **Solvers** : Composite, Backtracking

### 2. Backend API (Flask)

- **Endpoints REST** pour créer/modifier/résoudre des grilles
- **Gestion d'état** des grilles actives
- **Système de logs** détaillé pour chaque action
- **Sérialisation** Board ↔ JSON

### 3. Frontend Web (HTML/CSS/JS)

- **Setup Mode** : interface de création de grilles
- **Solver Mode** : résolution interactive pas à pas
- **Visualisation** : highlighting des changements, grille avec candidats
- **Communication** avec le backend via fetch API

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
│   │   ├── constraints/        # 15+ contraintes
│   │   │   ├── base_constraint.py
│   │   │   ├── factory.py      # Registry des contraintes
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
│       └── app.js
├── tests/                       # Tests unitaires
├── board.json                   # Exemple de configuration
├── ARCHITECTURE.md              # Documentation architecture
├── CLAUDE.md                    # Guide pour Claude Code
├── pyproject.toml
└── README.md
```

## 🎯 Contraintes supportées

- **bishop** : Diagonales (mouvement fou échecs)
- **clone** : Zones identiques
- **dutch** : Whispers hollandais (différence ≥ 4)
- **german** : Whispers allemands (différence ≥ 5)
- **greater_than** : Relation d'ordre
- **killer** : Somme de cellules
- **king** : Mouvement roi échecs
- **knight** : Mouvement cavalier échecs
- **kropki** : Points noirs/blancs
- **palindrome** : Ligne palindromique
- **parity** : Parité (pair/impair)
- **universal** : Toutes contraintes de position
- **x_v** : Somme X (10) ou V (5)

## 🧪 Tests

Exécuter les tests :

```bash
uv run pytest                    # Tous les tests
uv run pytest tests/test_board.py  # Test spécifique
uv run pytest --cov              # Avec couverture
```

## 🛠️ Développement

### Formatage et linting

```bash
make format    # Formater le code (isort, black, ruff)
make lint      # Linter (ruff, pydoclint, pylint)
make typecheck # Vérification de types (mypy)
make check     # Tout en une fois
```

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

- **cells** : dictionnaire `position -> liste de candidats`
- **constraints** : liste de contraintes avec leurs paramètres

Required fields:

- `size` (int): grid size (usually 9)
- `cells` (object): map of cell id to candidate list

Optional fields:

- `constraints` (array): constraint objects, empty if none

Cell ids use the `a1` format where `a` is row 0, `1` is column 0. Row letters
go from `a` to `a + size - 1`, columns go from `1` to `size`.

Legacy compatibility: the API also accepts `constraint` as the key name.

Voir `board.json` et `board.example.json` pour des exemples complets.

## 🔧 Configuration

### Backend

Le backend Flask peut être configuré via les variables :

```python
# src/api.py
app.run(debug=True, port=5000)  # Modifier le port si nécessaire
```

### Frontend

Le frontend se connecte par défaut à `http://localhost:5000`. Pour changer :

```javascript
// site/js/app.js
const API_BASE = 'http://localhost:5000/api';  // Modifier l'URL
```

## 📚 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** : Architecture détaillée du système
- **[CLAUDE.md](CLAUDE.md)** : Guide pour Claude Code
- **Docstrings** : Toutes les classes et fonctions sont documentées (style Google)

Générer la documentation HTML :

```bash
uv run pdoc src -o docs/
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
