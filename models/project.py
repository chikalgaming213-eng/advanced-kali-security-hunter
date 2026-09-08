from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any

class JobState(str, Enum): QUEUED='QUEUED'; RUNNING='RUNNING'; PAUSED='PAUSED'; COMPLETED='COMPLETED'; FAILED='FAILED'; CANCELLED='CANCELLED'
@dataclass(slots=True)
class Workspace:
    workspace_id: str
    name: str
    root_path: str
    projects: list[str] = field(default_factory=list)
    def to_dict(self): return asdict(self)
@dataclass(slots=True)
class Program:
    program_id: str
    name: str
    platform: str = ''
    policy_url: str = ''
    authorization_notes: str = ''
    def to_dict(self): return asdict(self)
@dataclass(slots=True)
class Project:
    project_id: str
    name: str
    program_id: str
    root_path: str
    authorization: str = 'READ_ONLY'
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    def to_dict(self): return asdict(self)
@dataclass(slots=True)
class Target:
    value: str
    kind: str = 'hostname'
    in_scope: bool = True
    exclusions: list[str] = field(default_factory=list)
    notes: str = ''
    def to_dict(self): return asdict(self)
@dataclass(slots=True)
class Asset:
    asset_id: str
    value: str
    asset_type: str
    source: str = ''
    confidence: float = 0.0
    properties: dict[str, Any] = field(default_factory=dict)
    def to_dict(self): return asdict(self)
@dataclass(slots=True)
class Job:
    job_id: str
    name: str
    state: JobState = JobState.QUEUED
    progress: float = 0.0
    profile: str = 'read_only'
    error: str = ''
    def to_dict(self):
        data = asdict(self); data['state'] = self.state.value; return data
@dataclass(slots=True)
class Evidence:
    evidence_id: str
    path: str
    sha256: str
    source: str
    collected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    def to_dict(self): return asdict(self)
@dataclass(slots=True)
class Report:
    report_id: str
    title: str
    path: str
    format: str
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    def to_dict(self): return asdict(self)
