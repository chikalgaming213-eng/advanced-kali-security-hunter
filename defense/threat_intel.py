from __future__ import annotations
from dataclasses import dataclass
import os
@dataclass(slots=True)
class IntelligenceResult:
    indicator:str;reputation:str='unknown';confidence:float=0;source:str='LOCAL ANALYSIS ONLY';country:str='';asn:str='';organization:str=''
class ThreatIntelProvider:
    def lookup(self,indicator):raise NotImplementedError
class LocalThreatIntel:
    def __init__(self,denylist=None):self.denylist=set(denylist or [])
    def lookup(self,indicator):return IntelligenceResult(indicator,'listed' if indicator in self.denylist else 'unknown',1.0,'LOCAL ANALYSIS ONLY')
class ThreatIntelRegistry:
    def __init__(self):self.providers=[]
    def add(self,provider):self.providers.append(provider)
    def lookup(self,indicator):
        for provider in self.providers:
            try:return provider.lookup(indicator)
            except Exception:continue
        return LocalThreatIntel().lookup(indicator)
    @staticmethod
    def configured_provider_names():return [key for key in ('THREAT_INTEL_API_KEY','ABUSEIPDB_API_KEY') if os.getenv(key)]

