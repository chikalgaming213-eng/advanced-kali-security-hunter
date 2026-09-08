from __future__ import annotations
from pathlib import Path
import hashlib,json
class IntegrityMonitor:
    def digest(self,path:Path):return hashlib.sha256(path.read_bytes()).hexdigest()
    def baseline(self,paths):return {str(path):self.digest(path) for path in paths if path.exists()}
    def compare(self,baseline):
        events=[]
        for name,expected in baseline.items():
            path=Path(name)
            if not path.exists():events.append({'event':'FILE_DELETED','path':name})
            elif self.digest(path)!=expected:events.append({'event':'FILE_MODIFIED','path':name,'expected':expected,'actual':self.digest(path)})
        return events
    def save(self,baseline,path):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(baseline,indent=2),encoding='utf-8')

