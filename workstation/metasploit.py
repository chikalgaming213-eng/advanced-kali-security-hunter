from __future__ import annotations
from dataclasses import dataclass
import shutil,subprocess
from .models import MetasploitModule
@dataclass(slots=True)
class MetasploitStatus:
    installed:bool;binary:str|None;version:str='';error:str=''
class MetasploitWorkspace:
    def __init__(self): self.modules:list[MetasploitModule]=[];self.lab_mode=False;self.authorized=False
    def detect(self)->MetasploitStatus:
        binary=shutil.which('msfconsole')
        if not binary:return MetasploitStatus(False,None)
        try:
            result=subprocess.run([binary,'--version'],capture_output=True,text=True,timeout=3);return MetasploitStatus(True,binary,(result.stdout or result.stderr).splitlines()[0][:200])
        except Exception as exc:return MetasploitStatus(True,binary,error=str(exc))
    def register(self,module): self.modules.append(module)
    def search(self,query): return [m for m in self.modules if query.casefold() in (m.name+' '+m.description).casefold()]
    def permitted_modules(self): return [m for m in self.modules if m.permitted(self.lab_mode,self.authorized)]
    def module_info(self,name): return next((m for m in self.modules if m.name==name),None)
    def enable_lab(self,authorized:bool): self.authorized=authorized;self.lab_mode=authorized

