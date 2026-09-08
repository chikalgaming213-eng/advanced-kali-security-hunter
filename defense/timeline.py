from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
@dataclass(slots=True)
class TimelineEntry:
    timestamp: str
    kind: str
    summary: str
    source: str = ''
    severity: str = 'NORMAL'
    data: dict | None = None
    def to_dict(self): return asdict(self)
class SecurityTimeline:
    def __init__(self): self.entries=[]
    def add(self, kind, summary, source='', severity='NORMAL', data=None, timestamp=None): self.entries.append(TimelineEntry(timestamp or datetime.now(timezone.utc).isoformat(), kind, summary, source, severity, data or {}))
    def search(self, query): return [item for item in self.entries if query.casefold() in json.dumps(item.to_dict()).casefold()]
    def filter(self, kind=None, severity=None): return [item for item in self.entries if (kind is None or item.kind==kind) and (severity is None or item.severity==severity)]
    def export(self, path): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(''.join(json.dumps(item.to_dict())+'\n' for item in sorted(self.entries, key=lambda item:item.timestamp)), encoding='utf-8'); return path
