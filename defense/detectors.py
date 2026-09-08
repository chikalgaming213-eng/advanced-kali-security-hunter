from __future__ import annotations
from collections import defaultdict,deque
from dataclasses import dataclass
from datetime import datetime,timezone
from .models import SecurityEvent,EventKind,ThreatCategory,ThreatLevel
@dataclass(slots=True)
class DetectionConfig:
    failed_attempt_threshold:int=20;window_seconds:int=120;cooldown_seconds:int=300;scan_port_threshold:int=10;anomaly_multiplier:float=5.0
class DetectionEngine:
    def __init__(self,config=None): self.config=config or DetectionConfig();self.events=deque(maxlen=10000);self.last_alert={}
    def ingest(self,event:SecurityEvent): self.events.append(event);return self.detect(event)
    def detect(self,event):
        findings=[]
        if event.kind is EventKind.AUTHENTICATION and event.action in ('failed','failure'):
            recent=[x for x in self.events if x.source_ip==event.source_ip and x.kind is EventKind.AUTHENTICATION and x.action in ('failed','failure')]
            if len(recent)>=self.config.failed_attempt_threshold: findings.append(self._alert(event,ThreatCategory.BRUTE_FORCE,ThreatLevel.HIGH,'repeated authentication failures'))
        if event.kind is EventKind.CONNECTION and event.source_ip:
            ports={x.port for x in self.events if x.source_ip==event.source_ip and x.kind is EventKind.CONNECTION and x.port}
            failed=sum(x.action in ('failed','refused','timeout') for x in self.events if x.source_ip==event.source_ip and x.kind is EventKind.CONNECTION)
            if len(ports)>=self.config.scan_port_threshold and failed>=self.config.scan_port_threshold: findings.append(self._alert(event,ThreatCategory.PORT_SCAN,ThreatLevel.MEDIUM,'many ports and failed connections'))
        if event.kind is EventKind.WEB and event.action in ('404','auth_failed'):
            similar=[x for x in self.events if x.source_ip==event.source_ip and x.kind is EventKind.WEB and x.action==event.action]
            if len(similar)>=self.config.failed_attempt_threshold: findings.append(self._alert(event,ThreatCategory.WEB_ENUMERATION,ThreatLevel.MEDIUM,'repeated web anomalies'))
        return findings
    def _alert(self,event,category,level,rationale):
        event.category=category;event.severity=level;event.confidence=min(1.0,event.confidence+0.25);event.evidence['rationale']=rationale;return event
class RateAnomalyDetector:
    def __init__(self,window=60,multiplier=5.0):self.window=window;self.multiplier=multiplier;self.history=defaultdict(deque)
    def observe(self,key,timestamp=None):
        now=timestamp or datetime.now(timezone.utc).timestamp();queue=self.history[key];queue.append(now)
        while queue and now-queue[0]>self.window:queue.popleft()
        baseline=max(1,len(queue)/10);return len(queue)>baseline*self.multiplier

