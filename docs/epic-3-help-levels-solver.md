# Epic 3 - Niveaux d'aide / solver

**Goal**  
Deliver three interchangeable help modes (guide, step, full) via the solver API with consistent explanations.

**Stories**
1. **Solver interface**: Define `Solver` base class and implement `guide`, `step`, `full`.  
   **Acceptance criteria**
   - All three modes share a common interface and are swappable at runtime.
   - Each mode returns a consistent result shape (message + delta or full solution).
   - Mode selection does not require UI reload.
2. **Solve endpoints**: Implement `POST /api/solve/guide|step|full` returning `help.message` + stateDelta.  
   **Acceptance criteria**
   - Endpoints respond within acceptable time for typical puzzles.
   - `guide` applies ongoing assistance without breaking user edits.
   - `step` applies exactly one deduction and explains it.
   - `full` returns a completed grid and optional explanation.
3. **History and consistency**: Maintain minimal history and guarantee deterministic deltas per action.  
   **Acceptance criteria**
   - Repeated requests on the same state yield consistent deltas.
   - History does not grow unbounded and can be reset.
   - Deltas are valid and replayable by the UI.

**Compatibility Requirements**
- Solver classes remain swappable.
- API contracts stable for UI.
- No regressions in existing solver logic.

**Risk Mitigation**
- Primary risk: Solver latency or inconsistent deltas.
- Mitigation: Timeboxed operations + delta validation tests.
- Rollback plan: Fallback to full solution-only mode.

**Definition of Done**
- All three modes return expected outputs.
- UI can switch modes without reload.
- Deterministic behavior for repeated requests.
