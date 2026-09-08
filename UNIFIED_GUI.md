# Unified GUI

The application now uses one PySide6 shell to expose the platform workspaces without manual launch steps.

## Launch

```bash
source .venv/bin/activate
python main.py --gui
```

The navigation includes:

- Main Security Hunter
- Defense Monster SOC
- Anti DoS / DDoS Monitor
- Malware Risk Monitor
- Ubuntu KDE Environment
- Debian XFCE Environment
- Advanced Terminal
- Metasploit Workspace
- Tool Center
- Recon Center
- Web/API Security
- Network Center
- OSINT Center
- Evidence Center
- Report Center
- System Monitor
- Settings
- Audit Logs

## Defensive behavior

The SOC page displays firewall detection, network metadata, connections, traffic windows, and malware-risk signals from the local backend. The anti-DoS/DDoS page identifies high connection rates, many ports, and repeated failures as indicators. It does not perform blocking, retaliation, counter-attack, DDoS, or traffic generation.

The malware page uses conservative process and script heuristics. A signal is a review indicator, not a malware verdict. The GUI never kills a process automatically. Investigation, isolation, and termination must remain explicit, policy-controlled operations.

The Ubuntu KDE and Debian XFCE pages are logical environment workspaces within the application. They display system metrics and environment state; they do not claim to create a second operating-system desktop inside PySide6.

Metasploit remains metadata/search oriented and disabled for intrusive operations unless the existing lab and authorization gates are satisfied.
