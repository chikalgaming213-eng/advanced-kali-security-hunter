# Professional Workflows

## Safe assessment workflow

`core/workflow.py` provides a composable workflow facade. A `WorkflowContext` carries an explicit `TargetScope`, observations, findings, and resumable state. `WorkflowStep` handlers can be enabled or disabled without changing the engine. The default workflow delegates to the existing read-only `AssessmentEngine` and publishes progress events for desktop consumers.

## External scanner output

`tools/parsers.py` parses bounded Nmap XML, Nuclei JSONL, or generic JSON. Parsing never executes the source tool. `vulnerability/normalizer.py` converts observations into stable `Finding` records, applying conservative severity and remediation rules.

## Risk prioritization

`vulnerability/scoring_engine.py` calculates a transparent 0–100 score from severity, confidence, exposure, and exploitability factors. It produces P1–P4 priority labels and never performs exploitation.

## Local persistence

`core/jsonl_store.py` is an append-only, thread-safe JSONL store for local assessment events. It supports append, batch append, read, counting, and compaction. No database or backend service is used.

## CLI workflow

```bash
python -c 'from cli_features import dispatch; dispatch(["scan", "127.0.0.1", "--name", "workflow"])'
```

All workflows remain read-only by default and are subject to scope validation and authorization policy.
