from __future__ import annotations
from dataclasses import dataclass, field
from collections import defaultdict, deque
from datetime import datetime, timezone
from .models import ThreatLevel
@dataclass(slots=True)
class TrafficIndicator:
    source: str
    event: str
    score: int
    level: ThreatLevel
    confidence: float
    ports: set[int] = field(default_factory=set)
    connections: int = 0
    first_seen: str = ''
    last_seen: str = ''
    rationale: str = ''
    def to_dict(self):
        return {'source':self.source,'event':self.event,'score':self.score,'level':self.level.value,'confidence':self.confidence,'ports':sorted(self.ports),'connections':self.connections,'first_seen':self.first_seen,'last_seen':self.last_seen,'rationale':self.rationale}
class TrafficGuard:
    """Detects traffic pressure indicators; it never blocks or retaliates."""
    def __init__(self, window_seconds=60, connection_threshold=100, source_threshold=40):
        self.window_seconds=window_seconds; self.connection_threshold=connection_threshold; self.source_threshold=source_threshold; self.events=defaultdict(deque)
    def observe(self, source, port=0, timestamp=None, failed=False):
        now=timestamp or datetime.now(timezone.utc).timestamp(); queue=self.events[source]; queue.append((now,port,failed))
        while queue and now-queue[0][0]>self.window_seconds: queue.popleft()
        count=len(queue); failed_count=sum(item[2] for item in queue); ports={item[1] for item in queue if item[1]}
        if count>=self.connection_threshold or len(ports)>=self.source_threshold:
            score=min(100,40+(count//max(1,self.connection_threshold))*20+min(30,len(ports)))
            level=ThreatLevel.CRITICAL if score>=80 else ThreatLevel.HIGH if score>=60 else ThreatLevel.MEDIUM
            return TrafficIndicator(source,'DOS_DDOS_INDICATOR',score,level,min(1,score/100),ports,count,datetime.fromtimestamp(queue[0][0],timezone.utc).isoformat(),datetime.fromtimestamp(now,timezone.utc).isoformat(),f'{count} connections, {len(ports)} ports, {failed_count} failures in window')
        return None
    def snapshot(self): return {source:len(queue) for source,queue in self.events.items()}

