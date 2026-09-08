from __future__ import annotations
from pathlib import Path
import os
class SafeFilesystem:
    """Restricts project-local file operations to prevent path traversal."""
    def __init__(self,root:Path):self.root=Path(root).resolve();self.root.mkdir(parents=True,exist_ok=True)
    def resolve(self,relative:str)->Path:
        candidate=(self.root/relative).resolve()
        if candidate!=self.root and self.root not in candidate.parents:raise PermissionError('path escapes project root')
        return candidate
    def ensure_dir(self,relative):path=self.resolve(relative);path.mkdir(parents=True,exist_ok=True);return path
    def write_text(self,relative,text):path=self.resolve(relative);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8');return path
    def read_text(self,relative):return self.resolve(relative).read_text(encoding='utf-8')
    def list_files(self,relative='.'):
        base=self.resolve(relative);return sorted(path for path in base.rglob('*') if path.is_file())
    def remove(self,relative,confirmed=False):
        if not confirmed:raise PermissionError('destructive file operation requires confirmation')
        path=self.resolve(relative);path.unlink();return path

