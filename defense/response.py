from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
import json
from .models import AllowlistEntry, DenylistEntry, Incident, IncidentStatus, ResponseMode
@dataclass(slots=True)
class ResponsePolicy:
    mode: ResponseMode = ResponseMode.MANUAL
    threshold: int = 80
    cooldown_seconds: int = 300
    default_block_seconds: int = 900
    allowlist: list[AllowlistEntry] = field(default_factory=list)
    denylist: list[DenylistEntry] = field(default_factory=list)
class ResponseEngine:
    def __init__(self, root: Path, policy=None): self.root=root; self.policy=policy or ResponsePolicy(); self.audit=[]
    def trusted(self, ip): return any(item.kind in ('ip','subnet') and item.value==ip for item in self.policy.allowlist)
    def propose_block(self, ip, score, reason):
        if self.trusted(ip): return {'action':'allow','reason':'allowlist precedence'}
        if score < self.policy.threshold: return {'action':'review','reason':'below threshold'}
        expires=(datetime.now(timezone.utc)+timedelta(seconds=self.policy.default_block_seconds)).isoformat(); return {'action':'block','ip':ip,'expires_at':expires,'reason':reason,'mode':self.policy.mode.value}
    def apply_block(self, ip, reason, operator_confirmed=False):
        if not operator_confirmed: raise PermissionError('blocking requires explicit confirmation')
        if self.trusted(ip): raise PermissionError('allowlisted source cannot be blocked')
        expires=(datetime.now(timezone.utc)+timedelta(seconds=self.policy.default_block_seconds)).isoformat(); entry=DenylistEntry(ip,reason,expires,manual=True); self.policy.denylist.append(entry); self.audit.append({'action':'block','ip':ip,'timestamp':datetime.now(timezone.utc).isoformat(),'expires_at':expires}); self.save(); return entry
    def transition(self, incident, status, operator_confirmed=False):
        if status in (IncidentStatus.CONTAINED, IncidentStatus.RESOLVED) and not operator_confirmed: raise PermissionError('incident response transition requires confirmation')
        incident.transition(status); self.audit.append({'action':'incident_transition','incident':incident.incident_id,'status':status.value}); self.save(); return incident
    def save(self):
        self.root.mkdir(parents=True, exist_ok=True); (self.root/'blocked_ips.json').write_text(json.dumps([item.__dict__ for item in self.policy.denylist], indent=2, default=str), encoding='utf-8'); (self.root/'response_audit.jsonl').write_text(''.join(json.dumps(item)+'\n' for item in self.audit), encoding='utf-8')
