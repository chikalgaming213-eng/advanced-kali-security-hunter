from __future__ import annotations
from dataclasses import dataclass,asdict
from datetime import datetime,timezone
@dataclass(slots=True)
class ConnectionObservation:
    local_ip:str; local_port:int; remote_ip:str; remote_port:int; protocol:str; state:str; pid:int|None=None; process:str=''; username:str=''; timestamp:str=''
    def __post_init__(self): self.timestamp=self.timestamp or datetime.now(timezone.utc).isoformat()
    def to_dict(self):return asdict(self)
class ConnectionMonitor:
    def snapshot(self):
        try:
            import psutil
            values=[]
            for item in psutil.net_connections(kind='inet'):
                local=item.laddr;remote=item.raddr;values.append(ConnectionObservation(local.ip,local.port,remote.ip if remote else '',remote.port if remote else 0,str(item.type),str(item.status),item.pid or None).to_dict())
            return values
        except (ImportError,PermissionError): return []

