from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import hashlib, json, time
@dataclass(slots=True)
class ArtifactStore:
    root: Path
    index: dict[str, dict] = field(default_factory=dict)
    def __post_init__(self): self.root.mkdir(parents=True, exist_ok=True)
    def put_text(self, name: str, text: str) -> Path:
        safe = Path(name).name; path=self.root/safe; path.write_text(text,encoding="utf-8"); return self.record(path)
    def put_bytes(self, name: str, data: bytes) -> Path:
        safe=Path(name).name; path=self.root/safe; path.write_bytes(data); return self.record(path)
    def record(self,path:Path)->Path:
        digest=hashlib.sha256(path.read_bytes()).hexdigest(); self.index[str(path)]={"size":path.stat().st_size,"sha256":digest,"recorded":time.time()}; self.flush(); return path
    def flush(self): (self.root/"manifest.json").write_text(json.dumps(self.index,indent=2),encoding="utf-8")
    def verify(self,path:Path)->bool:
        item=self.index.get(str(path)); return bool(item and hashlib.sha256(path.read_bytes()).hexdigest()==item["sha256"])
    def list_paths(self): return sorted(Path(p) for p in self.index)
    def remove(self,path:Path)->bool:
        if str(path) not in self.index:return False
        path.unlink(missing_ok=True); del self.index[str(path)]; self.flush(); return True

