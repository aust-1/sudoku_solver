# CTC Sudoku Solver Fullstack Architecture Document

## Introduction
This document defines the fullstack architecture for CTC Sudoku Solver, covering frontend UX-driven needs and backend solver/API concerns in a single source of truth. It targets a local-only deployment with a responsive web UI, a solver engine exposed via a lightweight API, and a shared data model aligned with `board.example.json`. The goal is to make development consistent across UI, state management, and solver interactions while preserving fast feedback (<200ms) and a simple local setup.

### Starter Template or Existing Project
N/A - Greenfield project. No starter or existing codebase is referenced in the PRD or UX spec. We will choose a stack and optional starter once platform and repo structure are validated.

### Change Log
| Date | Version | Description | Author |
| --- | --- | --- | --- |
| YYYY-MM-DD | 0.1 | Initial architecture draft (intro created) | Winston (Architect) |

## High Level Architecture
### Technical Summary
CTC Sudoku Solver will be a local-only web application with a fast, interactive frontend and a lightweight backend API that hosts solver logic and state. The frontend is a single-page app optimized for low-latency grid interactions and rich constraint editing, while the backend exposes command and state endpoints plus optional WS events. The system uses a shared JSON data model aligned with `board.example.json` and maintains state in memory for responsiveness. No database is required for MVP; import/export uses local JSON files. This architecture meets the PRD goals for simplicity (one-command local setup), responsiveness (<200ms actions), and multi-level solver assistance.

### Platform and Infrastructure Choice
**Platform:** Localhost (self-hosted)  
**Key Services:** None (local process only)  
**Deployment Host and Regions:** N/A (local)

### Repository Structure
**Structure:** Monorepo  
**Monorepo Tool:** npm workspaces (lightweight, zero extra tooling)  
**Package Organization:** `apps/web` (frontend SPA), `apps/api` (local API/solver host), `packages/shared` (types + data model + helpers)

### High Level Architecture Diagram
```mermaid
graph TD
  U[User Browser] --> FE[Web UI (SPA)]
  FE -->|REST| API[Local API Server]
  FE -->|WS Events (optional)| WS[WS Event Stream]
  API --> SOLVER[Solver Engine]
  API --> STATE[In-Memory State Store]
  API --> CONSTRAINTS[Constraint Registry]
  API --> FS[Local File Import/Export]
  STATE --> SOLVER
  CONSTRAINTS --> SOLVER
```

### Architectural Patterns
- **Local-First Architecture:** Single-machine deployment with local API - _Rationale:_ meets MVP local-only requirement and minimizes setup.  
- **SPA + API Split:** Web UI decoupled from solver API - _Rationale:_ clean separation between UI concerns and solver logic.  
- **Command/State API Pattern:** Commands mutate state, state endpoint provides snapshot/delta - _Rationale:_ aligns with PRD endpoints and fast UI updates.  
- **Event-Driven Updates (Optional WS):** Push deltas to UI - _Rationale:_ supports "accompagnement" with minimal polling.  
- **Shared Type Model:** Shared TypeScript types for `board` and `stateDelta` - _Rationale:_ prevents schema drift across UI/backend.

## Tech Stack
### Technology Stack Table
| Category | Technology | Version | Purpose | Rationale |
| --- | --- | --- | --- | --- |
| Frontend Language | TypeScript | 5.x | Type-safe UI + shared types | Strong typing for grid/state complexity |
| Frontend Framework | React | 18.x | SPA UI | Fits interactive grid + componentized UI |
| UI Component Library | Radix UI (headless) | 1.x | Accessible primitives | Accessibility-first without visual lock-in |
| State Management | Zustand | 4.x | UI + solver state | Simple, fast, minimal boilerplate |
| Backend Language | Python | 3.11 | Solver + API | Matches existing codebase (`src/`) |
| Backend Framework | FastAPI | 0.110.x | Local REST API + WS | Fast dev, async, good typing |
| API Style | REST + WS (optional) | N/A | Commands + state + events | Matches PRD endpoints and deltas |
| Database | None (in-memory) | N/A | MVP state | PRD: no DB for MVP |
| Cache | None | N/A | N/A | In-memory state is sufficient |
| File Storage | Local filesystem | N/A | Import/export JSON | PRD: board JSON files |
| Authentication | None | N/A | Local-only | Out of scope for MVP |
| Frontend Testing | Vitest + React Testing Library | 1.x / 15.x | Unit/component tests | Fast + standard React tooling |
| Backend Testing | Pytest | 8.x | API/solver tests | Existing Python testing ecosystem |
| E2E Testing | Playwright | 1.4x | UI workflows | Reliable cross-browser testing |
| Build Tool | Vite (FE) + uv (BE) | 5.x / 0.4x | Build + env mgmt | Fast frontend builds, modern Python tooling |
| Bundler | Vite/Rollup | 5.x | Bundle SPA | Default Vite pipeline |
| IaC Tool | N/A | N/A | Local-only | No infra provisioning |
| CI/CD | GitHub Actions | N/A | Tests + lint | Standard, free, simple |
| Monitoring | None (local) | N/A | N/A | MVP local-only |
| Logging | Python logging + browser console | N/A | Debugging | Adequate for local-only MVP |
| CSS Framework | Tailwind CSS | 3.4.x | Rapid UI styling | Fits custom design system quickly |

## Data Models
### BoardFile
Purpose: portable puzzle representation for import/export aligned with `board.example.json`.

Key Attributes:
- size: number - grid size (9 for standard)
- cells: Record<string, number[]> - map of cell id (e.g., "a1") to candidates
- constraints: Constraint[] - list of constraint definitions

TypeScript Interface:
```typescript
export interface BoardFile {
  size: number;
  cells: Record<string, number[]>;
  constraints: Constraint[];
}
```

Relationships:
- BoardFile.constraints uses Constraint
- BoardFile is converted to/from AppState for runtime

### CellCoord
Purpose: canonical coordinate for API deltas and UI interactions.

Key Attributes:
- row: number - 0-based row index
- col: number - 0-based column index
- id: string - "a1" style cell id (derived)

TypeScript Interface:
```typescript
export interface CellCoord {
  row: number;
  col: number;
  id: string;
}
```

Relationships:
- Used by StateDelta updates and UI grid selection
- Derived from or converted to BoardFile cell ids

### Constraint
Purpose: generic constraint definition to support many CTC types.

Key Attributes:
- id: string - unique constraint id
- type: string - constraint type (e.g., "kropki", "thermo")
- payload: Record<string, unknown> - type-specific data

TypeScript Interface:
```typescript
export interface Constraint {
  id: string;
  type: string;
  payload: Record<string, unknown>;
}
```

Relationships:
- Used in BoardFile and AppState
- UI renders overlays based on Constraint.type and payload

### AppState
Purpose: full runtime state served by `GET /api/state`.

Key Attributes:
- grid: number[][] - 9x9 values (0 for empty)
- candidates: number[][][] - candidates per cell
- notes: string[][] - user annotations per cell
- constraints: Constraint[] - active constraints
- helpMode: "guide" | "step" | "full"
- dirty: boolean - modified since last solve/import

TypeScript Interface:
```typescript
export interface AppState {
  grid: number[][];
  candidates: number[][][];
  notes: string[][];
  constraints: Constraint[];
  helpMode: "guide" | "step" | "full";
  dirty: boolean;
}
```

Relationships:
- AppState.constraints uses Constraint
- AppState is source of StateDelta comparisons

### StateDelta
Purpose: minimal change set for fast UI updates after commands.

Key Attributes:
- grid: { row, col, value }[]
- candidates: { row, col, set?: number[]; clear?: number[] }[]
- notes: { row, col, text }[]
- constraints: { added?: Constraint[]; updated?: { id: string; payload: Record<string, unknown> }[]; removed?: string[] }
- help?: { message: string; rule?: string }

TypeScript Interface:
```typescript
export interface StateDelta {
  grid?: Array<{ row: number; col: number; value: number }>;
  candidates?: Array<{
    row: number;
    col: number;
    set?: number[];
    clear?: number[];
  }>;
  notes?: Array<{ row: number; col: number; text: string }>;
  constraints?: {
    added?: Constraint[];
    updated?: Array<{ id: string; payload: Record<string, unknown> }>;
    removed?: string[];
  };
  help?: { message: string; rule?: string };
}
```

Relationships:
- References Constraint for added items
- Consumed by frontend state store to patch AppState

## API Specification
### REST API Specification (OpenAPI 3.0 draft)
```yaml
openapi: 3.0.0
info:
  title: CTC Sudoku Solver API
  version: 0.1.0
  description: Local-only API for solver commands and state snapshots/deltas.
servers:
  - url: http://127.0.0.1:8000
    description: Local development server
paths:
  /api/state:
    get:
      summary: Get full app state
      responses:
        "200":
          description: Full state snapshot
  /api/constraints:
    get:
      summary: List supported constraint types and minimal UI schema
      responses:
        "200":
          description: Constraint catalog
  /api/board:
    get:
      summary: Export current board as board.example.json format
      responses:
        "200":
          description: Board file
  /api/board/import:
    post:
      summary: Import board file and replace current state
      requestBody:
        required: true
      responses:
        "200":
          description: State delta or full state
  /api/grid/set:
    post:
      summary: Set a grid cell value
      requestBody:
        required: true
      responses:
        "200":
          description: State delta
  /api/candidates/set:
    post:
      summary: Set candidates for a cell
      requestBody:
        required: true
      responses:
        "200":
          description: State delta
  /api/notes/set:
    post:
      summary: Set notes for a cell
      requestBody:
        required: true
      responses:
        "200":
          description: State delta
  /api/constraints/add:
    post:
      summary: Add a constraint
      requestBody:
        required: true
      responses:
        "200":
          description: State delta
  /api/constraints/update:
    post:
      summary: Update a constraint payload
      requestBody:
        required: true
      responses:
        "200":
          description: State delta
  /api/constraints/remove:
    post:
      summary: Remove a constraint
      requestBody:
        required: true
      responses:
        "200":
          description: State delta
  /api/solve/guide:
    post:
      summary: Apply guide mode assistance
      responses:
        "200":
          description: State delta with help message
  /api/solve/step:
    post:
      summary: Apply one deduction step
      responses:
        "200":
          description: State delta with explanation
  /api/solve/full:
    post:
      summary: Solve the puzzle completely
      responses:
        "200":
          description: Full solution + optional explanation
  /api/reset:
    post:
      summary: Reset grid, notes, constraints
      responses:
        "200":
          description: State delta or full state
```
