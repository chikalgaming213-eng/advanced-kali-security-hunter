import json
from pathlib import Path
from models.entities import Finding,Severity,TargetScope
from tools.parsers import ToolOutputParser
from vulnerability.normalizer import FindingNormalizer
from vulnerability.scoring_engine import RiskScorer
from core.jsonl_store import JsonlStore
from core.workflow import AssessmentWorkflow,WorkflowContext

def test_parse_and_normalize_nuclei():
    raw=json.dumps({"template-id":"http-missing-security-headers","host":"127.0.0.1","info":{"name":"headers","severity":"low"}})
    records=ToolOutputParser().parse_nuclei_jsonl(raw); finding=FindingNormalizer().from_observation(ToolOutputParser().to_observations(records)[0]); assert finding.severity is Severity.LOW

def test_risk_scoring_is_bounded():
    finding=Finding("a","a",Severity.HIGH,"localhost",confidence=0.9); assert 0 <= RiskScorer().score(finding,1,1) <= 100

def test_jsonl_store(tmp_path:Path):
    store=JsonlStore(tmp_path/"events.jsonl"); store.append({"id":"a"}); store.append({"id":"b"}); assert store.count()==2; assert store.compact("id")==2

def test_workflow_read_only():
    workflow=AssessmentWorkflow(); workflow.attach_default_steps(); result=workflow.run(WorkflowContext(TargetScope(["127.0.0.1"]))); assert result.findings

