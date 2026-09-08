from __future__ import annotations
from dataclasses import dataclass, field
from fnmatch import fnmatch
from ipaddress import ip_address, ip_network
from models.entities import Authorization, TargetScope
from .exceptions import PolicyViolation, ScopeError

@dataclass(slots=True)
class ScopeEngine:
    targets: list[str] = field(default_factory=list)
    exclusions: list[str] = field(default_factory=list)
    def matches(self, target: str) -> bool:
        return target in self.targets or any(fnmatch(target, pattern) for pattern in self.targets)
    def excluded(self, target: str) -> bool:
        return any(fnmatch(target, pattern) for pattern in self.exclusions)
    def check(self, target: str) -> None:
        if not target or any(char in target for char in ('\n','\r','\x00',' ')): raise ScopeError('invalid target')
        if not self.matches(target) or self.excluded(target): raise ScopeError('target is outside explicit scope')
    def check_network(self, target: str, allow_cidr=False) -> None:
        self.check(target)
        if '/' in target:
            if not allow_cidr: raise ScopeError('CIDR requires explicit scope permission')
            try: ip_network(target, strict=False)
            except ValueError as exc: raise ScopeError('invalid CIDR') from exc

@dataclass(slots=True)
class AuthorizationEngine:
    authorization: Authorization = Authorization.READ_ONLY
    lab_mode: bool = False
    operator: str = ''
    def check(self, intrusive: bool = False) -> None:
        if intrusive and not (self.authorization is Authorization.AUTHORIZED and self.lab_mode): raise PolicyViolation('intrusive operation requires AUTHORIZED + LAB_MODE')
        if self.authorization is Authorization.LAB_ONLY and not self.lab_mode: raise PolicyViolation('LAB_ONLY operation requires LAB_MODE')

@dataclass(slots=True)
class PolicyEngine:
    passive_only: bool = True
    deny_persistence: bool = True
    deny_credential_access: bool = True
    deny_destructive: bool = True
    denied_operations: set[str] = field(default_factory=lambda: {'retaliation','counter_attack','ddos','credential_theft','ransomware','persistence','mass_exploitation'})
    def check(self, operation: str, intrusive=False) -> None:
        normalized=operation.casefold().replace(' ','_')
        if normalized in self.denied_operations: raise PolicyViolation(f'operation denied by policy: {operation}')
        if intrusive and self.passive_only: raise PolicyViolation('passive-only policy blocks intrusive operation')
        if normalized=='persistence' and self.deny_persistence: raise PolicyViolation('persistence is denied')
        if normalized=='credential_access' and self.deny_credential_access: raise PolicyViolation('credential access is denied')
        if normalized in {'delete','destroy','wipe'} and self.deny_destructive: raise PolicyViolation('destructive operation is denied')

@dataclass(slots=True)
class RateLimitEngine:
    requests_per_minute: int = 60
    _timestamps: list[float] = field(default_factory=list, init=False, repr=False)
    def allow(self, now: float | None = None) -> bool:
        import time
        current=now if now is not None else time.monotonic(); self._timestamps=[value for value in self._timestamps if current-value<60]
        if len(self._timestamps)>=self.requests_per_minute: return False
        self._timestamps.append(current); return True
    def require(self, now: float | None = None) -> None:
        if not self.allow(now): raise PolicyViolation('rate limit exceeded')

@dataclass(slots=True)
class SecurityBoundary:
    scope: ScopeEngine
    authorization: AuthorizationEngine
    policy: PolicyEngine = field(default_factory=PolicyEngine)
    rate_limit: RateLimitEngine = field(default_factory=RateLimitEngine)
    def validate(self, target: str, operation: str = 'read_only', intrusive=False) -> None:
        self.scope.check(target); self.authorization.check(intrusive); self.policy.check(operation, intrusive); self.rate_limit.require()
    @classmethod
    def from_target_scope(cls, scope: TargetScope) -> 'SecurityBoundary':
        return cls(ScopeEngine(scope.normalized(), scope.exclusions), AuthorizationEngine(scope.authorization, scope.lab_mode))
