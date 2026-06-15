# Post-Generation Cleanup Checklist (Stage 9.5)

Critical:
- Perform systematic cleanup before evaluation.

1) Event/listener cleanup:
- [ ] Identify signals/events/listeners tied to removed logic
- [ ] Search all emit/trigger call sites
- [ ] Search all listener/subscription sites
- [ ] Remove obsolete emit/trigger sites
- [ ] Remove obsolete subscriptions/listener blocks
- [ ] Remove obsolete event definitions

2) Dead code function detection:
- [ ] Identify functions only used by removed logic
- [ ] Verify no remaining invocations
- [ ] Remove functions with 0 invocations

3) Orphaned variable/parameter removal:
- [ ] Identify variables passed only into removed calls
- [ ] Verify not used elsewhere
- [ ] Remove orphaned variables and listener definitions

4) Verification:
- [ ] Run compiler/type-checker on modified files (0 errors)
- [ ] Run linter/style check (no new violations)
- [ ] Final search pass for orphan references
- [ ] Final search includes test + mocks + assembler/router
