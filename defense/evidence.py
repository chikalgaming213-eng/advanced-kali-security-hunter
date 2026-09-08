from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

class EvidenceCollector:
    def __init__(self, root: Path):
        self.root = root

    def incident_dir(self, incident_id):
        path = self.root / "incidents" / incident_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def append_event(self, incident_id, stream, record):
        path = self.incident_dir(incident_id) / (stream + ".jsonl")
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
        return path

    def collect_file(self, incident_id, source: Path, label="artifact"):
        dest = self.incident_dir(incident_id) / label
        shutil.copy2(source, dest)
        digest = hashlib.sha256(dest.read_bytes()).hexdigest()
        manifest = self.incident_dir(incident_id) / "hashes.json"
        existing = json.loads(manifest.read_text()) if manifest.exists() else {}
        existing[str(dest)] = {"sha256": digest, "timestamp": datetime.now(timezone.utc).isoformat(), "source": str(source), "collector": "DEFENSE_MONSTER"}
        manifest.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        return dest

    def export_incident(self, incident_id):
        return sorted(str(path) for path in self.incident_dir(incident_id).rglob("*") if path.is_file())
