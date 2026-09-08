from __future__ import annotations
from dataclasses import dataclass,field
from datetime import datetime,timezone
from typing import Callable,Any
from models.entities import AssessmentEvent,TargetScope,Finding
from core.engine import AssessmentEngine
@dataclass(slots=True)
class WorkflowContext:
    scope:TargetScope
    findings:list[Finding]=field(default_factory=list)
    observations:list[dict[str,Any]]=field(default_factory=list)
    state:dict[str,Any]=field(default_factory=dict)
    started_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
@dataclass(slots=True)
class WorkflowStep:
    name:str
    handler:Callable[[WorkflowContext],None]
    enabled:bool=True
class AssessmentWorkflow:
    """Composable workflow facade around the safe assessment engine."""
    def __init__(self,engine:AssessmentEngine|None=None): self.engine=engine or AssessmentEngine(); self.steps:list[WorkflowStep]=[]
    def add_step(self,name,handler,enabled=True): self.steps.append(WorkflowStep(name,handler,enabled)); return self
    def attach_default_steps(self):
        self.add_step("assessment",lambda ctx:ctx.findings.extend(self.engine.assess(ctx.scope))); return self
    def run(self,context:WorkflowContext)->WorkflowContext:
        total=sum(step.enabled for step in self.steps)
        complete=0
        for step in self.steps:
            if not step.enabled: continue
            self.engine.events.publish(AssessmentEvent("workflow_step",step.name,complete/max(total,1),{"state":context.state}))
            step.handler(context); complete+=1
        self.engine.events.publish(AssessmentEvent("workflow_complete","Workflow completed",1.0,{"findings":len(context.findings)})); return context

