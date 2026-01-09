# Epic 2 - API d'etat + commandes de base

**Goal**  
Provide a complete, fast API for reading state and applying core edits to the grid, candidates, notes, and constraints.

**Stories**
1. **State endpoints**: Implement `GET /api/state` and `GET /api/constraints` (types + payload schema).  
   **Acceptance criteria**
   - `GET /api/state` returns full, coherent state in < 200 ms for typical puzzles.
   - `GET /api/constraints` lists all supported types with required payload fields.
   - Responses are stable and backward compatible for the UI.
2. **Grid/candidates/notes**: Implement `POST /api/grid/set`, `POST /api/candidates/set`, `POST /api/notes/set`.  
   **Acceptance criteria**
   - Each endpoint updates only the targeted cell data and returns a minimal state delta.
   - Invalid inputs are rejected with clear, consistent errors.
   - Updates remain consistent with server-side solver state.
3. **Constraints CRUD**: Implement `POST /api/constraints/add|update|remove` with unique IDs.  
   **Acceptance criteria**
   - New constraints receive unique, stable IDs.
   - Updates modify only the specified payload fields without side effects.
   - Removing a constraint cleans up UI state and related overlays.

**Compatibility Requirements**
- Backward compatible JSON responses.
- UI patterns remain consistent.
- Minimal latency (< 200 ms for common actions).

**Risk Mitigation**
- Primary risk: Incomplete state consistency across endpoints.
- Mitigation: Centralized state model and stateDelta tests.
- Rollback plan: Disable new endpoints and fall back to full state refresh.

**Definition of Done**
- All endpoints return coherent state and deltas.
- Performance meets MVP target.
- CRUD operations are stable and tested.
