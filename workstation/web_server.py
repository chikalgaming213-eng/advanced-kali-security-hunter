from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import shutil
@dataclass(slots=True)
class WebServerProfile:
    name:str; runtime:str; root_dir:str; port:int=8080; command:list[str]=None; health_path:str='/'
    def validate(self):
        if self.port<1024 or self.port>65535: raise ValueError('unprivileged port must be 1024..65535')
        if not Path(self.root_dir).exists(): raise ValueError('root directory missing')
class WebServerCatalog:
    def available(self): return {name:shutil.which(name) for name in ('nginx','apache2','python3','node')}
    def python_http(self,root,port=8080): return WebServerProfile('python-http','python3',str(Path(root).resolve()),port,['python3','-m','http.server',str(port)])
    def validate(self,profile): profile.validate();return profile

