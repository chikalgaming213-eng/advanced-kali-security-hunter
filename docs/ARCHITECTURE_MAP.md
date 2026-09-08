# Architecture Map

## Runtime boundary

The root launcher (`run.py`) dispatches to the unified desktop GUI (`main.py --gui`), read-only assessment (`main.py <targets>`), Defense Monster SOC (`defense_cli.py`), workstation monitoring (`workstation_cli.py`), and tests. The application is local-only and stores portable artifacts under `data/` or user-selected project folders.

## Domain layers

| Layer | Packages | Responsibility |
|---|---|---|
| Foundation | `core/`, `models/`, `utils/`, `logging/` | policy, events, secure execution, serialization, typed entities, logging |
| Project | `storage/`, `projects/` | portable workspace/program/project manifests and JSONL streams |
| Security Hunter | `recon/`, `network/`, `web/`, `osint/`, `vulnerability/` | scoped discovery, normalized observations, scoring, findings |
| Tools | `tools/` | catalog, detection, adapters, output parsers |
| Defense | `defense/` | local SOC, traffic indicators, malware-risk heuristics, response gates, evidence |
| Workstation | `workstation/` | environment models, system monitor, terminal, local service metadata |
| Presentation | `gui/`, root CLIs | unified operator experience and command-line entry points |
| Reporting | `reporting/`, `evidence/` | JSON, JSONL, Markdown, HTML, TXT, manifests, hashes |

## Critical security path

```text
Target
  -> ScopeEngine
  -> AuthorizationEngine
  -> PolicyEngine
  -> RateLimitEngine
  -> CommandSpec validation
  -> SafeExecutor
  -> bounded output
  -> parser
  -> normalized result
  -> evidence and audit log
```

No GUI text field may become a raw shell command. No adapter may bypass scope, authorization, policy, or rate limits.

## Reusable code audit

Existing reusable foundations include `core/command_builder.py`, `core/scope.py`, `core/authorization.py`, `core/events.py`, `core/jsonl_store.py`, `tools/tool_manager.py`, `tools/parsers.py`, `vulnerability/normalizer.py`, `defense/soc_facade.py`, `workstation/system_monitor.py`, and `reporting/generator.py`. The next phase adds a central `ApplicationContext` and portable project store without replacing these modules.

## Known gaps to close

The GUI currently has navigation placeholders for some workspaces. The project manifest and artifact paths need a single portable manager. Policy, rate limiting, and command execution need one explicit pipeline facade. The current test count is healthy but must grow around the new project and security boundaries.
