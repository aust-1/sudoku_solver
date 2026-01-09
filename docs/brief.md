# Project Brief: CTC Sudoku Solver

## Executive Summary
- Concept: An interactive web app to solve CTC sudoku with many special constraints.
- Problem: Existing solvers are not interactive enough, are hard to configure, and lack progressive help levels.
- Target Market: Single primary user (you), with optional future expansion to other CTC fans.
- Value Proposition: Easy setup, rich UI, broad constraint support, and multi-level help.

## Problem Statement
- Current state: CTC puzzles use many constraint types, and few tools handle them consistently.
- Pain: Manual solving is slow and brittle; constraint changes often break the reasoning flow.
- Existing gaps: Tools lack interactive UI, are hard to configure, and rarely offer progressive help.
- Urgency: You need fast iteration now for your own puzzles.

## Proposed Solution
- Concept: A local-first interactive web UI for solving CTC sudoku.
- Differentiators: Wide constraint support, simple configuration, and progressive help levels (hint, next deduction, step-by-step, full solution).
- Why it works: Combines a Python solver backend (in progress) with a UI designed for rapid iteration.
- Vision: A personal platform that can evolve into a shareable tool.

## Target Users
### Primary User Segment: CTC creator/solver (you)
- Profile: Single user, comfortable installing a local tool.
- Workflow: Manual solving plus scripts, frequent constraint edits.
- Needs: Interactive UI, easy setup, configurable help levels, broad constraint support.
- Goals: Iterate quickly and solve with appropriate guidance.

### Secondary User Segment (optional): Other CTC fans/creators
- Needs: Clear UI, import/export, reusable constraint presets.

## Goals & Success Metrics
### Business Objectives
- M1: Local solver setup in under 10 minutes.
- M2: Support all prioritized MVP constraints.
- M3: Full interactive flow (load grid, configure constraints, assisted solving).

### User Success Metrics
- First hint in under 60 seconds.
- Complete an assisted solve without leaving the UI.
- Low configuration error rate.

### KPIs
- Setup time (target: < 10 min)
- Time to first hint (target: < 60 s)
- MVP constraint coverage (target: 100%)

## MVP Scope
### Core Features (Must Have)
- Interactive grid UI: edit, annotate, candidates, error highlighting.
- CTC constraint configuration in UI (add/edit/remove).
- Multi-level help: hint, next deduction, step-by-step, full solution.
- Import/export puzzles and constraints in JSON.
- Easy local setup (single command/script).
- MVP priority constraints:
  - Arrow, Ascending Sequences, Axia, Between Lines, Consecutive, Couples
  - Friendly-Cells, Jigsaw, Little Unique Killer, Lockout Lines, Non-Consecutive
  - Quadruple, Reflection, Renban, Running Cells, Sandwich, Skyscraper
  - Slingshot, Slow Thermo, Thermo, Twisted Consecutive, Windoku
  - X-Sum, Zipper Line

### Out of Scope for MVP
- Accounts, cloud hosting, advanced sharing.
- Community puzzle library.
- Heavy AI solvers or puzzle generation.

### MVP Success Criteria
- A complex CTC grid can be configured and solved with assisted mode in the UI without technical friction.

## Post-MVP Vision
### Phase 2 Features
- Reusable constraint presets and templates.
- Sharing/import from common CTC formats.
- Richer explanations and logical justifications.

### Long-term Vision
- A reference tool for CTC creation and solving with an extensible UI.

### Expansion Opportunities
- Optional community sharing or collaboration.
- Third-party constraint plugins.
- Optional hosted version.

## Technical Considerations
### Platform Requirements
- Target Platforms: Local web app (desktop browser)
- Browser/OS Support: Latest Chrome/Firefox/Edge
- Performance: UI responses under 200 ms for common actions

### Technology Preferences
- Frontend: No preferred stack
- Backend: Python (in progress)
- Database: None for MVP (JSON files)
- Hosting/Infrastructure: Local only

### Architecture Considerations
- Repository Structure: Monorepo with frontend + backend
- Service Architecture: Local REST API plus WebSocket for interactive help
- Integration: Command-style endpoints (e.g., solve/next-step) and event stream
- Security/Compliance: No strong requirements (local)

## Constraints & Assumptions
### Constraints
- Budget: Personal time only
- Timeline: Flexible
- Resources: 1 person
- Technical: Backend is partial; API not yet defined; UI must be highly interactive

### Key Assumptions
- MVP stays local-first
- Priority constraints can be listed and defined
- JSON is sufficient for puzzles and constraints
- UI is the primary value driver

## Risks & Open Questions
### Key Risks
- Scope creep from too many constraint types
- Complexity of a truly interactive UI
- Designing a flexible UI <-> solver API
- Performance if solver latency is high

### Open Questions
- Which CTC constraints are MVP priorities?
- Exact help levels and behaviors?
- Interaction style (overlays, drag/drop, etc.)?
- Formal JSON schema needed for MVP?

### Areas Needing Further Research
- UX patterns in existing CTC tools
- API patterns for UI to Python solver integration

## Appendices
- Research summary: None yet
- Stakeholder input: None yet
- References: None yet

## Next Steps
1. Define exact help levels and behaviors.
2. Sketch a JSON schema for grids and constraints.
3. Prototype a minimal interactive UI.
