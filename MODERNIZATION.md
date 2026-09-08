# Modernization Release

This release expands the project from a security assessment engine into a local, database-free cybersecurity workstation control plane.

## Added capabilities

| Area | Capability |
|---|---|
| Environment Manager | Ubuntu KDE, Debian XFCE, Terminal, Metasploit, Security Engine, and Local Server logical workspaces |
| System Monitor | CPU, RAM, disk, network counters, process count, threads, uptime, and optional temperature |
| Local VPS / Bot foundation | Typed local server and bot project models, resource limits, lifecycle state, and log paths |
| ServiceSupervisor | Explicit argv-only registration, runtime allowlist, sanitized environment, process groups, graceful stop, crash detection, and per-service stdout/stderr logs |
| Terminal Center | Profiles, session history, environment selection, output recording, and local JSONL history |
| Asset Graph | Nodes and relationships from program through finding, search, neighbors, subgraphs, JSON export, and Mermaid export |
| Metasploit Workspace | Availability/version detection, module metadata/search, and lab-only permission gate |
| Web Server Center | Local Python HTTP profile and safe unprivileged port validation |
| Network Center | Hostname, address, route, and safe DNS resolution inspection |
| GUI | Modern dashboard with workspace navigation, resource cards, live monitor refresh, and read-only assessment action |

## Safety boundaries

The core does not create cloud VPS instances, alter firewall rules, install packages, execute arbitrary shell strings, or perform remote exploitation. Privileged operations and intrusive security actions remain disabled by default and require explicit authorization and lab mode in the existing policy layer.

## Validation

The release has 108 Python files, 7,273 Python source lines, 620 catalog entries, valid JSON configuration, 16 passing tests, successful bytecode compilation, and successful workstation CLI smoke tests.
