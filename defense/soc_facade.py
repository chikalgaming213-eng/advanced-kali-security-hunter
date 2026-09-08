from __future__ import annotations
from pathlib import Path
from .firewall import FirewallMonitor
from .network_shield import NetworkShield
from .connections import ConnectionMonitor
from .traffic_guard import TrafficGuard
from .malware_monitor import MalwareMonitor
from .score import DefenseScoreEngine
class DefenseSocFacade:
    """Single read-only facade consumed by the unified desktop GUI."""
    def __init__(self,root:Path): self.root=root;self.firewall=FirewallMonitor();self.shield=NetworkShield();self.connections=ConnectionMonitor();self.traffic=TrafficGuard();self.malware=MalwareMonitor()
    def snapshot(self):
        return {'network':self.shield.snapshot().to_dict(),'firewall':[item.to_dict() for item in self.firewall.detect()],'connections':self.connections.snapshot(),'traffic_windows':self.traffic.snapshot(),'malware_processes':[item.to_dict() for item in self.malware.process_indicators()]}
    def defense_score(self):
        firewall=100 if any(item.active for item in self.firewall.detect()) else 50
        return DefenseScoreEngine().calculate(firewall,50,90,50,75,80,85)
    def inspect_source(self,source,port=0,failed=False):
        indicator=self.traffic.observe(source,port,failed=failed);return indicator.to_dict() if indicator else None

