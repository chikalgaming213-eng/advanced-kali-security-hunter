from __future__ import annotations
import threading
from models.entities import TargetScope, AssessmentEvent, Finding
from .scope import ScopeValidator
from .authorization import AuthorizationGate
from .events import EventBus
class AssessmentEngine:
    STEPS=["asset_discovery","dns_enumeration","http_discovery","port_discovery","service_detection","technology_detection","endpoint_discovery","finding_correlation","report_generation"]
    def __init__(self, runner=None): self.scope_validator=ScopeValidator(); self.gate=AuthorizationGate(); self.events=EventBus(); self.cancel_event=threading.Event(); self.runner=runner
    def cancel(self): self.cancel_event.set(); self.events.publish(AssessmentEvent("cancelled","Cancellation requested"))
    def assess(self,scope:TargetScope)->list[Finding]:
        self.scope_validator.validate(scope); self.gate.check(scope,False); targets=[t for t in scope.normalized() if not self.scope_validator.is_excluded(t,scope)]; findings=[]
        total=len(self.STEPS)
        for i,step in enumerate(self.STEPS,1):
            if self.cancel_event.is_set(): break
            self.events.publish(AssessmentEvent("progress",step,i/total,{"targets":len(targets)}))
            if step=="asset_discovery":
                for t in targets: findings.append(Finding("AKSH-INFO-001","Assessment target registered",__import__('models.entities',fromlist=['Severity']).Severity.INFO,t,"Target accepted by scope validator","No impact; informational","Review authorization and scope records",tool="aksh-core",confidence=1.0))
        self.events.publish(AssessmentEvent("complete","Assessment completed",1.0,{"findings":len(findings)})); return findings
