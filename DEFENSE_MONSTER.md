# DEFENSE MONSTER X

DEFENSE MONSTER X is the defensive local SOC layer of BUG BOUNTY HUNTER X. It is designed for detection, classification, visualization, evidence collection, and assisted response on a workstation or authorized lab.

## Defense-in-depth layers

1. Network Shield: interfaces, addresses, routes, and local network metadata.
2. Firewall Monitor: safe detection of UFW, nftables, and iptables; rules are read-only.
3. Connection Monitor: local/remote addresses, ports, state, PID, and process metadata when permissions allow.
4. IDS Adapter Boundary: normalized events can receive Suricata, Zeek, Snort, TShark, or Wireshark output without assuming installation.
5. SSH Defense: authentication events can be classified as suspicious or likely abuse based on evidence and thresholds.
6. Web Defense: repeated 404, authentication-failure, rate, and method anomalies are represented as events.
7. Port Scan Detection: many ports and failed connections from one source generate a confidence-scored indicator.
8. Brute Force Detection: configurable failure threshold and time window.
9. Rate Anomaly Detection: moving-window observations and configurable multiplier.
10. Threat Intelligence: provider abstraction with local-only fallback; no API keys are hardcoded.
11. Behavior Engine: weighted signals produce a 0–100 operational score and threat level.
12. Incident Response: detected, triaged, investigating, contained, resolved, and closed lifecycle.

## Response safety

The default mode is `MANUAL`. Allowlist precedence is mandatory. Temporary blocks expire by default. Applying a block or transitioning an incident to containment/resolution requires explicit confirmation and creates an audit record. No retaliation, exploit-back, DDoS, credential theft, permanent block, or automatic firewall mutation is implemented.

## Forensic evidence

`defense/evidence.py` stores incident-scoped JSONL streams, copied artifacts, SHA256 hashes, timestamp, source, and collector metadata under `data/defense/incidents/<incident-id>/`. `defense/integrity.py` provides optional SHA256 baselines for selected configuration files.

## CLI

```bash
python defense_cli.py snapshot
python defense_cli.py firewall
python defense_cli.py score
```

All commands are non-invasive inspection or local calculation. Missing tools and insufficient privileges return empty or `NOT INSTALLED`-style data rather than crashing.

## Important limitation

A defense score is an operational indicator, not a guarantee of security. Geolocation, reputation, and a single event are never treated as definitive proof that an IP is an attacker.
