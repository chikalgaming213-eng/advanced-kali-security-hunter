from __future__ import annotations
from dataclasses import dataclass,field
from pathlib import Path
from .events import EventBus
from .config import ConfigLoader
from .command_builder import CommandBuilder
from .executor import SafeExecutor,ExecutionPolicy
from storage.filesystem import SafeFilesystem
from storage.project_store import PortableProject
@dataclass(slots=True)
class ApplicationContext:
    root:Path
    events:EventBus=field(default_factory=EventBus)
    config:ConfigLoader|None=None
    commands:CommandBuilder|None=None
    executor:SafeExecutor|None=None
    filesystem:SafeFilesystem|None=None
    project:PortableProject|None=None
    def __post_init__(self):
        self.root=Path(self.root).resolve();self.config=ConfigLoader(self.root/'config');self.commands=CommandBuilder();self.executor=SafeExecutor(self.commands,ExecutionPolicy(dry_run=True));self.filesystem=SafeFilesystem(self.root/'data')
    def open_project(self,path:Path,name='Security Project',program='Authorized Program',authorization='READ_ONLY'):
        project_file=Path(path)/'project.json'
        self.project=PortableProject.create(Path(path),name,program,authorization) if not project_file.exists() else PortableProject(Path(path),PortableProject.create(Path(path),name,program,authorization).manifest)
        return self.project
    def publish(self,kind,message,**data): self.events.publish(__import__('models.entities',fromlist=['AssessmentEvent']).AssessmentEvent(kind,message,data=data))

