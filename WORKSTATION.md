# BUG BOUNTY HUNTER X Workstation Layer

The workstation layer adds logical independent environments while keeping the core database-free and local. Ubuntu KDE, Debian XFCE, Terminal, Metasploit, Security Engine, and Local Server are represented as typed environment records. The implementation does not claim to create operating-system desktops or cloud VPS instances; it provides a safe control-plane abstraction that can be connected to explicitly provisioned local environments.

## System monitor

`workstation/system_monitor.py` collects CPU, RAM, disk, network counters, processes, threads, uptime, and optional temperature using `psutil` when available. It falls back gracefully when a metric is unavailable. Resource limits are modeled and validated without automatically changing system state.

## Local server and bot supervisor

`workstation/process_supervisor.py` provides explicit local process registration and lifecycle controls. Commands use argument arrays, a runtime allowlist, sanitized environment variables, process groups, bounded graceful shutdown, crash state detection, and per-service stdout/stderr logs. It does not accept shell strings, silently install dependencies, or manage remote infrastructure.

The models support Local VPS Center and Bot Server Center records. A future UI can request confirmation before starting or stopping a process. The default restart policy is `never`.

## Asset graph

`workstation/asset_graph.py` models program, domain, host, port, service, technology, endpoint, and finding relationships. It supports search, neighbor queries, subgraph extraction, JSON export, and Mermaid export for local documentation.

## Metasploit workspace

`workstation/metasploit.py` detects `msfconsole` and supports local module metadata/search. Intrusive modules remain disabled unless both `lab_mode` and explicit authorization are enabled. No automatic exploit execution is provided.

## Operator CLI

```bash
python workstation_cli.py environments
python workstation_cli.py monitor
python workstation_cli.py graph --output data/reports/asset_graph.json
```

These commands are local read-only inspection/export operations. Privileged system changes, package installation, firewall changes, remote VPS creation, and arbitrary Internet operations remain outside the core and require separate reviewed integrations and confirmation.
