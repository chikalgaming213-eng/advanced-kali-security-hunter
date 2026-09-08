from __future__ import annotations
from pathlib import Path
from typing import Any,Iterator
import json,threading
class JsonlStore:
    """Atomic append-only local store suitable for resumable assessments."""
    def __init__(self,path:Path): self.path=path; self.path.parent.mkdir(parents=True,exist_ok=True); self.lock=threading.RLock()
    def append(self,record:dict[str,Any])->None:
        encoded=json.dumps(record,sort_keys=True,ensure_ascii=False)
        with self.lock,self.path.open("a",encoding="utf-8") as handle: handle.write(encoded+"\n"); handle.flush()
    def append_many(self,records:list[dict[str,Any]])->int:
        with self.lock,self.path.open("a",encoding="utf-8") as handle:
            for record in records: handle.write(json.dumps(record,sort_keys=True,ensure_ascii=False)+"\n")
        return len(records)
    def __iter__(self)->Iterator[dict[str,Any]]:
        if not self.path.exists(): return iter(())
        def rows():
            with self.path.open(encoding="utf-8") as handle:
                for line in handle:
                    if line.strip():
                        try: yield json.loads(line)
                        except json.JSONDecodeError: continue
        return rows()
    def read_all(self)->list[dict[str,Any]]: return list(iter(self))
    def compact(self,key:str)->int:
        unique={}
        for record in self: unique[str(record.get(key,""))]=record
        temp=self.path.with_suffix(".tmp"); temp.write_text("".join(json.dumps(x,sort_keys=True)+"\n" for x in unique.values()),encoding="utf-8"); temp.replace(self.path); return len(unique)
    def count(self)->int: return sum(1 for _ in self)

