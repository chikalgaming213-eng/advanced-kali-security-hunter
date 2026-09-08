from __future__ import annotations
from dataclasses import dataclass, field
from threading import Event
from models.entities import CommandSpec,CommandResult,TargetScope
from .authorization import AuthorizationGate
from .scope import ScopeValidator
from .exceptions import PolicyViolation
@dataclass(slots=True)
class RateLimit:
    requests_per_minute:int=60
    timestamps:list[float]=field(default_factory=list, init=False, repr=False)
    def allow(self)->bool:
        import time
        now=time.monotonic();self.timestamps=[value for value in self.timestamps if now-value<60]
        if len(self.timestamps)>=self.requests_per_minute:return False
        self.timestamps.append(now);return True
class GuardedExecutionPipeline:
    """Single target-to-execution boundary used by future adapters."""
    def __init__(self,executor,scope=None,authorization=None,rate_limit=None):self.executor=executor;self.scope=scope or ScopeValidator();self.authorization=authorization or AuthorizationGate();self.rate_limit=rate_limit or RateLimit()
    def execute(self,spec:CommandSpec,target:str,scope:TargetScope,cancel:Event|None=None,intrusive=False)->CommandResult:
        if target not in scope.normalized() or self.scope.is_excluded(target,scope):raise PolicyViolation('target is outside explicit scope')
        self.scope.validate(scope);self.authorization.check(scope,intrusive)
        if not self.rate_limit.allow():raise PolicyViolation('rate limit exceeded')
        return self.executor.execute(spec,cancel)
