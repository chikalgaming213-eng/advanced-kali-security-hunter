from dataclasses import dataclass, field
from typing import Any
@dataclass(slots=True)
class AssessmentProfile:
    name:str
    steps:list[str]=field(default_factory=list)
    timeout:float=30.0
    rate_limit:float=2.0
    concurrency:int=1
    read_only:bool=True
    def validate(self):
        if not self.name.strip(): raise ValueError("profile name required")
        if self.timeout<=0 or self.timeout>3600: raise ValueError("timeout outside bounds")
        if self.rate_limit<=0: raise ValueError("rate limit outside bounds")
        if self.concurrency<1 or self.concurrency>32: raise ValueError("concurrency outside bounds")
    def permits(self,step): return step in self.steps
    def to_dict(self): return {"name":self.name,"steps":self.steps,"timeout":self.timeout,"rate_limit":self.rate_limit,"concurrency":self.concurrency,"read_only":self.read_only}
    @classmethod
    def from_dict(cls,data): return cls(**{k:data[k] for k in cls.__dataclass_fields__ if k in data})
class ProfileRegistry:
    def __init__(self,profiles=()): self.profiles={p.name:p for p in profiles}
    def add(self,p): p.validate(); self.profiles[p.name]=p
    def get(self,name): return self.profiles.get(name)
    def names(self): return sorted(self.profiles)
    def default(self): return self.get("read_only") or next(iter(self.profiles.values()),AssessmentProfile("read_only"))

