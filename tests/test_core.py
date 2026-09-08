import threading
from pathlib import Path
from models.entities import CommandSpec,TargetScope,Authorization,Severity,Finding
from core.command_builder import CommandBuilder
from core.scope import ScopeValidator
from core.authorization import AuthorizationGate
from core.exceptions import CommandNotAllowed,PolicyViolation
from reporting.correlation import FindingCorrelator
from reporting.generator import ReportGenerator
def test_command_allowlist():
    try: CommandBuilder().validate(CommandSpec("rm",[]))
    except CommandNotAllowed: return
    assert False
def test_scope(): ScopeValidator().validate(TargetScope(["127.0.0.1"]))
def test_authorization_gate():
    try: AuthorizationGate().check(TargetScope(["127.0.0.1"],authorization=Authorization.READ_ONLY),True)
    except PolicyViolation: return
    assert False
def test_dedupe_and_report(tmp_path:Path):
    f=Finding("x","x",Severity.LOW,"127.0.0.1"); fs=FindingCorrelator().deduplicate([f,f]); assert len(fs)==1; assert (ReportGenerator(tmp_path).write(fs)/"assessment.json").exists()
