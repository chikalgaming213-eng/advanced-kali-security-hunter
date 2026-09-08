# Advanced Kali Security Hunter

A modular Python 3.11+ desktop and CLI workbench for **authorized, read-only security assessment**, CTFs, private labs, and security research. It uses local memory and JSON/JSONL files only; there is no database, backend, cloud service, persistence, credential theft, denial-of-service, or arbitrary Internet exploitation.

## Safety model

The default authorization is `READ_ONLY`. Intrusive operations are not implemented as arbitrary command strings. The command builder requires an executable allowlist, argument arrays, bounded timeout/output, sanitized environment, and process-group cancellation. Any future intrusive adapter must require `AUTHORIZED` plus `LAB_MODE` and an explicit confirmation.

## Install and run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py                 # localhost read-only sample
python main.py 127.0.0.1 --report localhost
python main.py --gui
python -m pytest -q
```

PySide6 is optional at runtime for CLI use. External security tools are system dependencies and are detected but never automatically installed.

## Layout

`core/` contains policy, scope validation, eventing, command execution, scheduling, and assessment orchestration. `tools/` contains a 620-entry Kali-oriented catalog, detector, registry, and adapter examples. `reporting/` writes JSON, Markdown, HTML, and TXT reports. `gui/` provides the dark desktop interface. `data/` stores local reports and logs.

## Extending

Add a catalog entry and a safe adapter exposing typed `CommandSpec` builders. Do not accept shell command strings from the GUI. Add mocked tests for new adapters and keep targets within explicit authorization scope.

## Troubleshooting

If `PySide6` is unavailable, use the CLI or install requirements. If an external tool is missing, the Tool Manager reports it as not installed; install it manually through the operating system after reviewing package provenance. A command rejected by the allowlist must be implemented as a reviewed adapter rather than bypassing the policy.
