# Epic 5 - UI contraintes & overlays

**Goal**  
Enable visual creation and editing of constraints through overlays and drag/drop, covering MVP constraint set.

**Stories**
1. **Constraint editor**: Add/edit/remove constraints via UI overlays.  
   **Acceptance criteria**
   - Users can add a constraint with required parameters via UI.
   - Constraints are editable and deletable without page reload.
   - UI actions map directly to API add/update/remove.
2. **Constraint rendering**: Visual representation for MVP constraint types.  
   **Acceptance criteria**
   - All MVP constraints render clearly on the grid.
   - Visuals update immediately after edits.
   - Rendering does not degrade grid interaction performance.
3. **Workflow accelerators**: Hotkeys and efficient editing flow.  
   **Acceptance criteria**
   - Hotkeys speed common actions without conflicting with browser defaults.
   - Drag/drop or overlay placement is reliable and repeatable.
   - Power-user flow reduces clicks for frequent edits.

**Compatibility Requirements**
- UI patterns consistent with grid interactions.
- Constraints map directly to API payloads.
- Performance impact remains minimal.

**Risk Mitigation**
- Primary risk: UI complexity and inconsistent constraint payloads.
- Mitigation: Schema-driven UI + validation feedback.
- Rollback plan: Provide basic form-based editor.

**Definition of Done**
- MVP constraints can be created and edited in UI.
- Constraint visuals match backend state.
- Editing flow is fast and reliable.
