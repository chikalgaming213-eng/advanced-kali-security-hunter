from __future__ import annotations
from dataclasses import dataclass,field,asdict
from enum import Enum
from datetime import datetime,timezone
from typing import Any
class EnvironmentKind(str,Enum): UBUNTU_KDE="ubuntu_kde"; DEBIAN_XFCE="debian_xfce"; TERMINAL="terminal"; METASPLOIT="metasploit"; SECURITY="security_engine"; LOCAL_SERVER="local_server"
class RuntimeKind(str,Enum): PYTHON="python"; NODE="node"; WEBHOOK="webhook"; SCHEDULED="scheduled"; BACKGROUND="background"
class ServiceState(str,Enum): STOPPED="STOPPED"; STARTING="STARTING"; RUNNING="RUNNING"; STOPPING="STOPPING"; CRASHED="CRASHED"; UNKNOWN="UNKNOWN"
class LimitAction(str,Enum): WARN="warn"; THROTTLE="throttle"; STOP="stop"
@dataclass(slots=True)
class Environment:
    name:str; kind:EnvironmentKind; status:ServiceState=ServiceState.UNKNOWN; cpu_percent:float=0; ram_percent:float=0; disk_percent:float=0; network_rx:int=0; network_tx:int=0; uptime_seconds:float=0; services:list[str]=field(default_factory=list); metadata:dict[str,Any]=field(default_factory=dict)
    def to_dict(self): d=asdict(self);d['kind']=self.kind.value;d['status']=self.status.value;return d
@dataclass(slots=True)
class ResourceLimits:
    cpu_percent:float=90; ram_percent:float=90; disk_percent:float=95; process_count:int=200; action:LimitAction=LimitAction.WARN
    def validate(self):
        if not 1<=self.cpu_percent<=100 or not 1<=self.ram_percent<=100 or not 1<=self.disk_percent<=100: raise ValueError('limits must be 1..100')
        if self.process_count<1: raise ValueError('process limit must be positive')
@dataclass(slots=True)
class LocalServer:
    server_id:str; name:str; root_dir:str; command:list[str]; port:int|None=None; state:ServiceState=ServiceState.STOPPED; cpu_limit:float=80; ram_limit_mb:int=512; environment:dict[str,str]=field(default_factory=dict); restart_policy:str='never'; created_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
    def validate(self):
        if not self.server_id or not self.name: raise ValueError('server identity required')
        if not self.command or any(not isinstance(item,str) or not item for item in self.command): raise ValueError('argv command required')
        if self.port is not None and not 1<=self.port<=65535: raise ValueError('invalid port')
@dataclass(slots=True)
class BotProject:
    bot_id:str; name:str; runtime:RuntimeKind; project_dir:str; entrypoint:list[str]; state:ServiceState=ServiceState.STOPPED; pid:int|None=None; restart_policy:str='never'; env_keys:list[str]=field(default_factory=list); log_dir:str='';
    def validate(self):
        if not self.bot_id or not self.name or not self.project_dir: raise ValueError('bot identity required')
        if not self.entrypoint or any(not isinstance(x,str) or x.startswith('-') and x not in ('-m','-u') for x in self.entrypoint): raise ValueError('safe argv entrypoint required')
@dataclass(slots=True)
class TerminalProfile:
    name:str; environment:EnvironmentKind; cwd:str; executable:str; arguments:list[str]=field(default_factory=list); history_file:str='data/terminal/history.jsonl'; safe_mode:bool=True
@dataclass(slots=True)
class AssetNode:
    node_id:str; node_type:str; label:str; properties:dict[str,Any]=field(default_factory=dict)
@dataclass(slots=True)
class AssetEdge:
    source:str; target:str; relationship:str; confidence:float=1.0
@dataclass(slots=True)
class MetasploitModule:
    name:str; module_type:str; description:str=''; rank:str='unknown'; references:list[str]=field(default_factory=list); options:dict[str,str]=field(default_factory=dict); intrusive:bool=False
    def permitted(self,lab_mode:bool,authorized:bool)->bool: return not self.intrusive or (lab_mode and authorized)

