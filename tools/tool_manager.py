import json
from pathlib import Path
from .detector import ToolDetector
class ToolManager:
    def __init__(self,catalog_path:Path): self.entries=json.loads(catalog_path.read_text()); self.detector=ToolDetector(); self.status={}
    def scan(self): self.status={e["name"]:self.detector.detect(e) for e in self.entries}; return self.status
    def by_category(self):
        out={}
        for e in self.entries: out.setdefault(e["category"],[]).append(e)
        return out
