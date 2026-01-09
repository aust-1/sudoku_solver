# Epic 1 - Modele de donnees + import/export JSON

**Goal**  
Define and implement the MVP JSON board format with import/export and basic validation to ensure consistent puzzle data flow between UI and backend.

**Stories**
1. **Schema de board**: Document the `board.example.json` format (cells/constraints) and add a minimal validator on the backend.  
   **Acceptance criteria**
   - `board.example.json` is documented with required/optional fields and examples.
   - Backend accepts valid boards and rejects malformed payloads with clear error messages.
   - Validation is fast and does not block normal UI interactions.
2. **Import/Export**: Implement `GET /api/board` and `POST /api/board/import` with state delta support.  
   **Acceptance criteria**
   - `GET /api/board` returns JSON strictly compatible with `board.example.json`.
   - `POST /api/board/import` replaces current state and returns a coherent state delta.
   - Import/export round-trip preserves grid, candidates, notes, and constraints.
3. **Cas limites**: Handle empty grid, unknown constraints, and partial candidates gracefully.  
   **Acceptance criteria**
   - Empty grid imports without errors and exports correctly.
   - Unknown constraint types are either ignored with warnings or rejected consistently.
   - Partial candidates do not crash the solver or UI; state remains coherent.

**Compatibility Requirements**
- Existing APIs remain unchanged.
- JSON format stays aligned with `board.example.json`.
- Performance impact is minimal.

**Risk Mitigation**
- Primary risk: Schema drift between UI and backend.
- Mitigation: Single source of truth + regression tests for import/export.
- Rollback plan: Revert to previous board format handler and keep old endpoints.

**Definition of Done**
- All stories completed with acceptance criteria met.
- Import/export works with `board.example.json`.
- Edge cases covered by tests.
