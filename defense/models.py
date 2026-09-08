from __future__ import annotations
from dataclasses import dataclass,field,asdict
from enum import Enum
from datetime import datetime,timezone
from typing import Any
class EventKind(str,Enum): CONNECTION="connection"; FIREWALL="firewall"; IDS="ids"; AUTHENTICATION="authentication"; PROCESS="process"; DNS="dns"; WEB="web"; FILE="file"; INCIDENT="incident"
class ThreatCategory(str,Enum): PORT_SCAN="PORT_SCAN"; BRUTE_FORCE="BRUTE_FORCE"; AUTH_ABUSE="AUTH_ABUSE"; WEB_ENUMERATION="WEB_ENUMERATION"; TRAFFIC_ANOMALY="TRAFFIC_ANOMALY"; MALICIOUS_PATTERN="MALICIOUS_PATTERN"; SUSPICIOUS_CONNECTION="SUSPICIOUS_CONNECTION"; POLICY_VIOLATION="POLICY_VIOLATION"; UNKNOWN="UNKNOWN"
class ThreatLevel(str,Enum): NORMAL="NORMAL"; LOW="LOW"; MEDIUM="MEDIUM"; HIGH="HIGH"; CRITICAL="CRITICAL"
class IncidentStatus(str,Enum): DETECTED="DETECTED"; TRIAGED="TRIAGED"; INVESTIGATING="INVESTIGATING"; CONTAINED="CONTAINED"; RESOLVED="RESOLVED"; CLOSED="CLOSED"; FALSE_POSITIVE="FALSE_POSITIVE"
class ResponseMode(str,Enum): MANUAL="MANUAL"; ASSISTED="ASSISTED"; AUTOMATIC="AUTOMATIC"
@dataclass(slots=True)
class SecurityEvent:
    event_id:str; kind:EventKind; source_ip:str=''; target:str=''; protocol:str=''; port:int|None=None; action:str='observed'; severity:ThreatLevel=ThreatLevel.NORMAL; category:ThreatCategory=ThreatCategory.UNKNOWN; confidence:float=0.0; timestamp:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat()); evidence:dict[str,Any]=field(default_factory=dict); process:str=''; pid:int|None=None
    def to_dict(self): d=asdict(self);d['kind']=self.kind.value;d['severity']=self.severity.value;d['category']=self.category.value;return d
@dataclass(slots=True)
class ThreatProfile:
    source_ip:str; score:int=0; confidence:float=0; country:str=''; asn:str=''; organization:str=''; first_seen:str=''; last_seen:str=''; event_count:int=0; blocked_events:int=0; allowed_events:int=0; ports:set[int]=field(default_factory=set); protocols:set[str]=field(default_factory=set); processes:set[str]=field(default_factory=set); categories:set[str]=field(default_factory=set)
    def level(self): return ThreatLevel.CRITICAL if self.score>=80 else ThreatLevel.HIGH if self.score>=60 else ThreatLevel.MEDIUM if self.score>=40 else ThreatLevel.LOW if self.score>=20 else ThreatLevel.NORMAL
    def to_dict(self):
        d=asdict(self);d['ports']=sorted(self.ports);d['protocols']=sorted(self.protocols);d['processes']=sorted(self.processes);d['categories']=sorted(self.categories);d['level']=self.level().value;return d
@dataclass(slots=True)
class Incident:
    incident_id:str; title:str; severity:ThreatLevel; status:IncidentStatus=IncidentStatus.DETECTED; source_ips:list[str]=field(default_factory=list); indicators:list[str]=field(default_factory=list); event_ids:list[str]=field(default_factory=list); recommended_actions:list[str]=field(default_factory=list); created_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat()); updated_at:str=''
    def transition(self,status): self.status=status;self.updated_at=datetime.now(timezone.utc).isoformat()
    def to_dict(self): d=asdict(self);d['severity']=self.severity.value;d['status']=self.status.value;return d
@dataclass(slots=True)
class AllowlistEntry:
    value:str; kind:str; reason:str=''; created_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
@dataclass(slots=True)
class DenylistEntry:
    ip:str; reason:str; expires_at:str; source:str='DEFENSE_MONSTER'; manual:bool=False; created_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())

