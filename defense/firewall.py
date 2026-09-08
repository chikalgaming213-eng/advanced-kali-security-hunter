from __future__ import annotations
from dataclasses import dataclass,field,asdict
import shutil,subprocess
@dataclass(slots=True)
class FirewallStatus:
    backend:str; installed:bool; active:bool=False; rules:list[str]=field(default_factory=list); blocked_packets:int=0; allowed_packets:int=0; error:str=''
    def to_dict(self): return asdict(self)
class FirewallMonitor:
    BACKENDS=('ufw','nft','iptables')
    def detect(self):
        statuses=[]
        for backend in self.BACKENDS:
            binary=shutil.which(backend)
            if not binary: statuses.append(FirewallStatus(backend,False));continue
            try:
                args=[binary,'status'] if backend=='ufw' else [binary,'list','rules'] if backend=='nft' else [binary,'-S']
                result=subprocess.run(args,capture_output=True,text=True,timeout=3);statuses.append(FirewallStatus(backend,True,result.returncode==0,result.stdout.splitlines()[:200],error=result.stderr[:300]))
            except OSError as exc: statuses.append(FirewallStatus(backend,True,error=str(exc)))
        return statuses
    def require_confirmation(self,action,operator_confirmed=False):
        if not operator_confirmed: raise PermissionError(f'firewall {action} requires explicit confirmation')

