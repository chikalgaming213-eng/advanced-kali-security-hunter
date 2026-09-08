from __future__ import annotations
from dataclasses import dataclass,asdict
import socket,subprocess,shutil
@dataclass(slots=True)
class ShieldSnapshot:
    interfaces:dict[str,list[str]]; routes:list[str]; dns:list[str]; listening:list[str]; connections:list[str]
    def to_dict(self): return asdict(self)
class NetworkShield:
    def snapshot(self)->ShieldSnapshot:
        interfaces={};
        try:
            for info in socket.getaddrinfo(socket.gethostname(),None): interfaces.setdefault(info[0],[]).append(info[4][0])
        except socket.gaierror: pass
        routes=[]
        if shutil.which('ip'):
            try: routes=subprocess.run(['ip','route'],capture_output=True,text=True,timeout=2).stdout.splitlines()
            except OSError: pass
        return ShieldSnapshot(interfaces,routes,[],[],[])

