from __future__ import annotations
from dataclasses import dataclass,asdict
from pathlib import Path
from datetime import datetime,timezone
from typing import Any,Iterator
import json
@dataclass(slots=True)
class ProjectManifest:
    name:str; program:str; created_at:str; version:str='1.0'; authorization:str='READ_ONLY'
    def to_dict(self):return asdict(self)
class PortableProject:
    """Self-contained project directory; no database or server is required."""
    STREAMS=('targets','assets','findings','jobs','events')
    def __init__(self,root:Path,manifest:ProjectManifest):self.root=root;self.manifest=manifest
    @classmethod
    def create(cls,root:Path,name:str,program:str,authorization='READ_ONLY'):
        root=Path(root);root.mkdir(parents=True,exist_ok=True);project=cls(root,ProjectManifest(name,program,datetime.now(timezone.utc).isoformat(),authorization=authorization));project.initialize();return project
    def initialize(self):
        for folder in ('evidence','scans','reports','logs'): (self.root/folder).mkdir(parents=True,exist_ok=True)
        self.write_json('project.json',self.manifest.to_dict())
        for stream in self.STREAMS: (self.root/f'{stream}.jsonl').touch(exist_ok=True)
    def write_json(self,name,value):
        path=self.root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2,ensure_ascii=False),encoding='utf-8');return path
    def append(self,stream,record):
        if stream not in self.STREAMS:raise ValueError(f'unsupported stream: {stream}')
        path=self.root/f'{stream}.jsonl'
        with path.open('a',encoding='utf-8') as handle:
            handle.write(json.dumps(record,sort_keys=True,ensure_ascii=False)+'\n')
        return path
    def read(self,stream)->Iterator[dict[str,Any]]:
        if stream not in self.STREAMS:raise ValueError(f'unsupported stream: {stream}')
        path=self.root/f'{stream}.jsonl'
        if not path.exists():return iter(())
        def rows():
            for line in path.read_text(encoding='utf-8').splitlines():
                if line.strip():yield json.loads(line)
        return rows()
    def export_manifest(self):return {'project':self.manifest.to_dict(),'root':str(self.root),'streams':{name:sum(1 for _ in self.read(name)) for name in self.STREAMS}}
    def report_path(self,name):return self.root/'reports'/name
