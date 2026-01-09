# Epic 4 - UI grille interactive

**Goal**  
Build a fast, intuitive grid UI with editing, candidates, notes, and error highlighting.

**Stories**
1. **Grid editor**: 9x9 grid with keyboard input, selection, and basic validation.  
   **Acceptance criteria**
   - Users can select cells via mouse and keyboard and enter values 1-9.
   - Invalid inputs are blocked or clearly indicated.
   - Edits sync to backend state via API calls.
2. **Candidates and notes**: Candidate entry, pencil marks, and per-cell notes.  
   **Acceptance criteria**
   - Users can toggle candidate mode and enter multiple candidates per cell.
   - Notes are editable per cell and persist across reloads (via API).
   - Candidates/notes are rendered distinctly from final values.
3. **Feedback**: Error highlighting and optional auto-candidates toggle.  
   **Acceptance criteria**
   - Conflicts and invalid states are visibly highlighted.
   - Auto-candidates can be enabled/disabled without losing manual edits.
   - UI remains responsive (< 200 ms) during edits.

**Compatibility Requirements**
- Works on latest desktop browsers.
- UI response < 200 ms for common actions.
- Follows existing interaction patterns if any exist.

**Risk Mitigation**
- Primary risk: UI performance degradation.
- Mitigation: Optimize rendering and limit reflow.
- Rollback plan: Disable advanced highlights to keep UI responsive.

**Definition of Done**
- Core grid interactions are smooth and reliable.
- Candidates and notes are persisted via API.
- Error display is accurate and togglable.
