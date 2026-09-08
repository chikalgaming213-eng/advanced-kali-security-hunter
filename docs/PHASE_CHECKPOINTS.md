# Development Phase Checkpoints

## Phase 00 — Audit

The repository audit found 131 Python files before this checkpoint, no `shell=True`, no broken pip requirements, and a passing baseline test suite. Reusable modules were retained rather than duplicated. The architecture map is in `docs/ARCHITECTURE_MAP.md`.

## Phase 01–02 — Foundation and project system

The application now has `ApplicationContext`, `SafeFilesystem`, `PortableProject`, typed project entities, JSONL streams, manifest export, and a root-level `project` command. A project is portable and database-free.

```bash
python run.py project projects/example --name "Example" --program "Authorized Program"
```

## Phase 03 — Scope and authorization

`core/policy_engine.py` adds `ScopeEngine`, `AuthorizationEngine`, `PolicyEngine`, `RateLimitEngine`, and `SecurityBoundary`. The boundary denies out-of-scope targets, denied operations, passive-policy violations, unauthorized intrusive operations, and rate-limit violations before execution.

## Validation

At this checkpoint, the project passes 34 tests and Python compilation. The next planned phase is integration of `SecurityBoundary` into every adapter-facing execution path and replacement of remaining GUI placeholder pages with real read-only page models.
