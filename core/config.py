from pathlib import Path
import json
class ConfigLoader:
    def __init__(self,root:Path): self.root=root
    def load(self,name:str):
        path=self.root/name
        with path.open(encoding="utf-8") as f: return json.load(f)
