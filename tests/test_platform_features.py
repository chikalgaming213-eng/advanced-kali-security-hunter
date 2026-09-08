from pathlib import Path
from workstation.models import *
from workstation.asset_graph import AssetGraph
from workstation.system_monitor import SystemMonitor
from workstation.process_supervisor import ProcessSupervisor
from workstation.terminal import TerminalManager
from workstation.web_server import WebServerCatalog

def test_environment_and_limits():
    ResourceLimits().validate(); Environment('x',EnvironmentKind.SECURITY).to_dict()

def test_asset_graph():
    g=AssetGraph();g.add_node(AssetNode('a','domain','example.com'));g.add_node(AssetNode('b','host','api'));g.add_edge(AssetEdge('a','b','resolves'));assert g.search('example');assert 'resolves' in g.to_mermaid()

def test_process_supervisor_rejects_shell():
    s=ProcessSupervisor(Path('/tmp/aksh-test-logs'))
    try:s.register('bad',['sh','-c','echo unsafe'])
    except ValueError:return
    assert False

def test_terminal_history(tmp_path):
    m=TerminalManager(tmp_path/'history.jsonl');p=TerminalProfile('host',EnvironmentKind.TERMINAL,'.','python3');m.add_profile(p);m.open('one','host');m.record('one','python3 --version','ok');assert m.search_history('version')

def test_local_web_profile(tmp_path):
    profile=WebServerCatalog().python_http(tmp_path);profile.validate();assert profile.port==8080

def test_monitor(): assert SystemMonitor().snapshot().process_count>=0

