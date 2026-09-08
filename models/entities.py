from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any

class Authorization(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    LAB_ONLY = "LAB_ONLY"
    READ_ONLY = "READ_ONLY"
class Severity(str, Enum):
    INFO="INFO"; LOW="LOW"; MEDIUM="MEDIUM"; HIGH="HIGH"; CRITICAL="CRITICAL"
@dataclass(slots=True)
class TargetScope:
    targets: list[str]
    exclusions: list[str] = field(default_factory=list)
    authorization: Authorization = Authorization.READ_ONLY
    lab_mode: bool = False
    cidr_allowed: bool = False
    def normalized(self) -> list[str]: return [x.strip() for x in self.targets if x.strip()]
@dataclass(slots=True)
class CommandSpec:
    executable: str
    arguments: list[str] = field(default_factory=list)
    timeout: float = 30.0
    max_output: int = 1_000_000
    cwd: str | None = None
    env: dict[str,str] | None = None
@dataclass(slots=True)
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    duration: float
    timed_out: bool = False
    cancelled: bool = False
@dataclass(slots=True)
class Finding:
    finding_id: str
    title: str
    severity: Severity
    target: str
    description: str = ""
    impact: str = ""
    remediation: str = ""
    evidence: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    tool: str = "internal"
    cvss: float | None = None
    port: int | None = None
    protocol: str | None = None
    url: str | None = None
    confidence: float = 0.5
    status: str = "open"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    def to_dict(self) -> dict[str, Any]:
        d=asdict(self); d['severity']=self.severity.value; return d
@dataclass(slots=True)
class AssessmentEvent:
    kind: str
    message: str
    progress: float = 0.0
    data: dict[str,Any] = field(default_factory=dict)
