from __future__ import annotations
import ipaddress, fnmatch
from urllib.parse import urlparse
from .exceptions import ScopeError
from models.entities import TargetScope
class ScopeValidator:
    def validate(self, scope: TargetScope) -> None:
        if not scope.normalized(): raise ScopeError("At least one target is required")
        if len(scope.targets)>1000: raise ScopeError("Target list exceeds safe limit")
        for target in scope.normalized():
            if any(fnmatch.fnmatch(target, pat) for pat in scope.exclusions): continue
            if " " in target or "\n" in target: raise ScopeError("Whitespace is not allowed in target")
            if "/" in target:
                try: ipaddress.ip_network(target, strict=False)
                except ValueError:
                    parsed=urlparse(target)
                    if not parsed.hostname: raise ScopeError(f"Invalid target: {target}")
    def is_excluded(self, target:str, scope:TargetScope)->bool:
        return any(fnmatch.fnmatch(target,p) for p in scope.exclusions)
