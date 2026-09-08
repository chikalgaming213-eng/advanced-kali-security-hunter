from __future__ import annotations
from dataclasses import dataclass,asdict
from datetime import datetime,timezone
import os,platform,time
try: import psutil
except ImportError: psutil=None
@dataclass(slots=True)
class SystemSnapshot:
    timestamp:str; cpu_percent:float; ram_percent:float; disk_percent:float; network_rx:int; network_tx:int; process_count:int; thread_count:int; uptime_seconds:float; temperature:float|None=None
    def to_dict(self): return asdict(self)
class SystemMonitor:
    def snapshot(self)->SystemSnapshot:
        if psutil:
            memory=psutil.virtual_memory(); disk=psutil.disk_usage('/'); net=psutil.net_io_counters(); processes=psutil.process_iter(['pid','num_threads']); threads=sum((p.info.get('num_threads') or 0) for p in processes)
            uptime=max(0,time.time()-psutil.boot_time()); temps=None
            try:
                values=psutil.sensors_temperatures(); flat=[x.current for group in values.values() for x in group if x.current is not None];temps=sum(flat)/len(flat) if flat else None
            except (AttributeError,NotImplementedError): pass
            return SystemSnapshot(datetime.now(timezone.utc).isoformat(),psutil.cpu_percent(interval=0.05),memory.percent,disk.percent,net.bytes_recv,net.bytes_sent,len(psutil.pids()),threads,uptime,temps)
        return SystemSnapshot(datetime.now(timezone.utc).isoformat(),0,0,0,0,0,0,0,0)
    def as_environment_metrics(self):
        snap=self.snapshot();return {'cpu':snap.cpu_percent,'ram':snap.ram_percent,'disk':snap.disk_percent,'network_rx':snap.network_rx,'network_tx':snap.network_tx,'processes':snap.process_count,'threads':snap.thread_count,'uptime':snap.uptime_seconds}
    def within(self,snapshot,limits): return snapshot.cpu_percent<=limits.cpu_percent and snapshot.ram_percent<=limits.ram_percent and snapshot.disk_percent<=limits.disk_percent and snapshot.process_count<=limits.process_count

