# Epic 6 - Packaging local & DX

**Goal**  
Ensure a frictionless local setup and a clear first-run flow to the first hint.

**Stories**
1. **One-command launch**: Script to start frontend + backend locally.  
   **Acceptance criteria**
   - Single command starts both services on a clean machine.
   - Clear errors are shown if dependencies are missing.
   - Services can be stopped cleanly.
2. **README install**: Simple steps, < 10 min setup.  
   **Acceptance criteria**
   - Fresh install completes within 10 minutes following README.
   - README includes prerequisites and troubleshooting.
   - Steps are OS-aware if needed.
3. **First hint flow**: Document and verify "first hint < 60s".  
   **Acceptance criteria**
   - A new user can load a sample puzzle and request a hint in < 60 s.
   - The flow is documented step-by-step.
   - The measured time is repeatable.

**Compatibility Requirements**
- Local-only operation.
- Works on Windows/macOS/Linux (if targeted).
- No external services required.

**Risk Mitigation**
- Primary risk: Setup friction or broken scripts.
- Mitigation: Add sanity checks and clear error messages.
- Rollback plan: Provide manual steps as fallback.

**Definition of Done**
- Setup succeeds in < 10 minutes.
- First hint flow verified.
- Documentation is complete and accurate.
