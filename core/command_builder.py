from __future__ import annotations
import os, signal, subprocess, time, threading
from models.entities import CommandSpec, CommandResult
from .exceptions import CommandNotAllowed
class CommandBuilder:
    SAFE_EXECUTABLES={"nmap","naabu","rustscan","nc","tshark","dig","host","nslookup","whois","httpx","nuclei","nikto","subfinder","amass","assetfinder","findomain","theharvester","curl","python3"}
    def __init__(self, allowlist=None): self.allowlist=set(allowlist or self.SAFE_EXECUTABLES)
    def validate(self,spec:CommandSpec)->list[str]:
        if not spec.executable or os.path.basename(spec.executable) not in self.allowlist: raise CommandNotAllowed(spec.executable)
        if any("\x00" in a or "\n" in a or "\r" in a for a in spec.arguments): raise CommandNotAllowed("Invalid argument")
        if spec.timeout<=0 or spec.timeout>3600: raise CommandNotAllowed("Timeout outside bounds")
        return [spec.executable,*spec.arguments]
    def run(self,spec:CommandSpec, cancel:threading.Event|None=None)->CommandResult:
        command=self.validate(spec); started=time.monotonic(); env={"PATH":os.environ.get("PATH","")}
        if spec.env: env.update({k:v for k,v in spec.env.items() if k in {"PATH","LANG","LC_ALL"}})
        proc=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,cwd=spec.cwd,env=env,start_new_session=True)
        timed=False; cancelled=False
        try:
            out,err=proc.communicate(timeout=spec.timeout)
        except subprocess.TimeoutExpired:
            timed=True; os.killpg(proc.pid,signal.SIGTERM); out,err=proc.communicate()
        if cancel and cancel.is_set() and proc.poll() is None:
            cancelled=True; os.killpg(proc.pid,signal.SIGTERM); out,err=proc.communicate()
        out=(out or "")[:spec.max_output]; err=(err or "")[:spec.max_output]
        return CommandResult(command,proc.returncode or 0,out,err,time.monotonic()-started,timed,cancelled)
