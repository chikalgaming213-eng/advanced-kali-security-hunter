from __future__ import annotations
from dataclasses import dataclass,field
from pathlib import Path
import json,time
from .models import TerminalProfile
@dataclass(slots=True)
class TerminalSession:
    session_id:str; profile:TerminalProfile; history:list[str]=field(default_factory=list); output:list[str]=field(default_factory=list); active:bool=True
    def record(self,command,result): self.history.append(command);self.output.append(result)
class TerminalManager:
    def __init__(self,history_path:Path): self.history_path=history_path;self.sessions={};self.profiles={}
    def add_profile(self,profile): self.profiles[profile.name]=profile
    def open(self,session_id,profile_name):
        if profile_name not in self.profiles: raise KeyError(profile_name)
        session=TerminalSession(session_id,self.profiles[profile_name]);self.sessions[session_id]=session;return session
    def close(self,session_id): self.sessions[session_id].active=False
    def record(self,session_id,command,result):
        session=self.sessions[session_id];session.record(command,result);self.history_path.parent.mkdir(parents=True,exist_ok=True)
        with self.history_path.open('a',encoding='utf-8') as handle: handle.write(json.dumps({'session':session_id,'command':command,'timestamp':time.time()})+'\n')
    def search_history(self,query):
        if not self.history_path.exists():return []
        return [json.loads(line) for line in self.history_path.read_text().splitlines() if query.casefold() in line.casefold()]

