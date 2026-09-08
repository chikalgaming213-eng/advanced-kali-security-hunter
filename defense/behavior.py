from __future__ import annotations
from dataclasses import dataclass
from .models import SecurityEvent,ThreatLevel
@dataclass(slots=True)
class BehaviorWeights:
    port_scan:int=25;authentication_failures:int=30;abnormal_rate:int=20;known_ioc:int=40;suspicious_process:int=25
class BehaviorEngine:
    def __init__(self,weights=None):self.weights=weights or BehaviorWeights()
    def score(self,signals:dict[str,bool])->int:return min(100,sum(getattr(self.weights,key) for key,value in signals.items() if value and hasattr(self.weights,key)))
    def level(self,score):return ThreatLevel.CRITICAL if score>=80 else ThreatLevel.HIGH if score>=60 else ThreatLevel.MEDIUM if score>=40 else ThreatLevel.LOW if score>=20 else ThreatLevel.NORMAL
    def profile(self,source_ip,events,signals):
        score=self.score(signals);return {'source_ip':source_ip,'score':score,'level':self.level(score).value,'event_count':len(events),'signals':signals}

