from __future__ import annotations
from pathlib import Path
import json,platform,shutil,time
from .models import Environment,EnvironmentKind,ServiceState
class EnvironmentManager:
    """Reads environment capabilities; it never silently changes the host."""
    def __init__(self,root:Path): self.root=root;self.path=root/'data/environments.json';self.environments=self._load()
    def _load(self):
        values=[]
        for kind in EnvironmentKind:
            values.append(Environment(kind.value,kind,ServiceState.UNKNOWN,metadata={'platform':platform.platform(),'python':platform.python_version()}))
        if self.path.exists():
            try:
                raw=json.loads(self.path.read_text()); by={x['name']:x for x in raw}
                for env in values:
                    if env.name in by: env.metadata.update(by[env.name].get('metadata',{}))
            except (OSError,ValueError): pass
        return {item.name:item for item in values}
    def get(self,name): return self.environments.get(name)
    def list(self): return list(self.environments.values())
    def detect_binaries(self,names): return {name:shutil.which(name) for name in names}
    def save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True);self.path.write_text(json.dumps([x.to_dict() for x in self.list()],indent=2),encoding='utf-8')
    def update_status(self,name,status,**metadata):
        env=self.environments[name];env.status=status;env.metadata.update(metadata);self.save();return env
    def capabilities(self): return {'os':platform.system(),'release':platform.release(),'machine':platform.machine(),'binaries':self.detect_binaries(['python3','node','npm','docker','nmap','msfconsole','nginx'])}

