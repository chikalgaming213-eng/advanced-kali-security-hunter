from __future__ import annotations
from dataclasses import dataclass,asdict
import socket,subprocess,shutil
@dataclass(slots=True)
class NetworkSnapshot:
    hostname:str; addresses:list[str]; routes:list[str]; dns_servers:list[str]; listening_services:list[str]
    def to_dict(self): return asdict(self)
class NetworkCenter:
    def snapshot(self)->NetworkSnapshot:
        host=socket.gethostname();addresses=[]
        try: addresses=sorted({x[4][0] for x in socket.getaddrinfo(host,None)})
        except socket.gaierror: pass
        routes=[]
        if shutil.which('ip'):
            try: routes=subprocess.run(['ip','route'],capture_output=True,text=True,timeout=2).stdout.splitlines()
            except OSError: pass
        return NetworkSnapshot(host,addresses,routes,[],[])
    def resolve(self,hostname):
        try:return sorted({x[4][0] for x in socket.getaddrinfo(hostname,None)})
        except socket.gaierror:return []

