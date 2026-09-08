from pathlib import Path
from defense.models import *
from defense.detectors import DetectionEngine,DetectionConfig
from defense.response import ResponseEngine
from defense.evidence import EvidenceCollector
from defense.integrity import IntegrityMonitor
from defense.score import DefenseScoreEngine

def test_auth_detection():
    engine=DetectionEngine(DetectionConfig(failed_attempt_threshold=2));events=[]
    for i in range(2): events.extend(engine.ingest(SecurityEvent(str(i),EventKind.AUTHENTICATION,source_ip='10.0.0.1',action='failed',confidence=.5)))
    assert events and events[-1].category is ThreatCategory.BRUTE_FORCE

def test_response_requires_confirmation(tmp_path):
    response=ResponseEngine(tmp_path)
    try: response.apply_block('1.2.3.4','test')
    except PermissionError:return
    assert False

def test_allowlist_precedence(tmp_path):
    response=ResponseEngine(tmp_path);response.policy.allowlist.append(AllowlistEntry('1.2.3.4','ip'));assert response.propose_block('1.2.3.4',100,'x')['action']=='allow'

def test_integrity(tmp_path):
    p=tmp_path/'x';p.write_text('one');monitor=IntegrityMonitor();base=monitor.baseline([p]);p.write_text('two');assert monitor.compare(base)[0]['event']=='FILE_MODIFIED'

def test_evidence(tmp_path):
    source=tmp_path/'source';source.write_text('evidence');collector=EvidenceCollector(tmp_path);dest=collector.collect_file('INC-1',source);assert dest.exists() and (tmp_path/'incidents/INC-1/hashes.json').exists()

def test_score_disclaimer(): assert DefenseScoreEngine().calculate(90,80,90,70,80,60,80).total()>0

