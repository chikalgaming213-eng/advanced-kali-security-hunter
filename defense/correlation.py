from __future__ import annotations
from collections import defaultdict
from .models import SecurityEvent,Incident,ThreatLevel
class EventCorrelator:
    def correlate(self,events):
        groups=defaultdict(list)
        for event in events:
            if event.source_ip:groups[event.source_ip].append(event)
        incidents=[]
        for source,values in groups.items():
            categories={x.category.value for x in values};score=min(100,len(values)*2+sum(25 for x in categories if x!='UNKNOWN'));severity=ThreatLevel.CRITICAL if score>=80 else ThreatLevel.HIGH if score>=60 else ThreatLevel.MEDIUM if score>=40 else ThreatLevel.LOW if score>=20 else ThreatLevel.NORMAL
            if severity is not ThreatLevel.NORMAL: incidents.append(Incident(f'INC-{len(incidents)+1:06d}',f'Correlated activity from {source}',severity,source_ips=[source],indicators=sorted(categories),event_ids=[x.event_id for x in values],recommended_actions=['collect evidence','review allowlist']))
        return incidents

