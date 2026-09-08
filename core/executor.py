from __future__ import annotations
from dataclasses import dataclass
from threading import Event
from models.entities import CommandSpec, CommandResult
from .command_builder import CommandBuilder
@dataclass(slots=True)
class ExecutionPolicy:
    max_parallel:int=2
    max_commands:int=100
    dry_run:bool=True
class SafeExecutor:
    def __init__(self,builder=None,policy=None): self.builder=builder or CommandBuilder(); self.policy=policy or ExecutionPolicy(); self.count=0
    def execute(self,spec:CommandSpec,cancel:Event|None=None)->CommandResult:
        if self.count>=self.policy.max_commands: raise RuntimeError("command budget exhausted")
        self.count+=1
        if self.policy.dry_run: return CommandResult([spec.executable,*spec.arguments],0,"DRY-RUN: command not executed","",0.0)
        return self.builder.run(spec,cancel)
    def reset_budget(self): self.count=0

