from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os
import signal
import subprocess
import threading
import time
from .models import ServiceState

@dataclass(slots=True)
class ManagedProcess:
    identity: str
    argv: list[str]
    process: subprocess.Popen | None = None
    state: ServiceState = ServiceState.STOPPED
    started_at: float | None = None
    restarts: int = 0
    stdout_path: Path | None = None
    stderr_path: Path | None = None

class ProcessSupervisor:
    """Explicitly controlled argv-only supervisor for local authorized services."""
    ALLOWED = {"python", "python3", "node", "nodejs", "uvicorn", "npm"}

    def __init__(self, log_root: Path):
        self.log_root = log_root
        self.log_root.mkdir(parents=True, exist_ok=True)
        self.processes: dict[str, ManagedProcess] = {}
        self.lock = threading.RLock()

    def validate_argv(self, argv: list[str]) -> None:
        if not argv or Path(argv[0]).name not in self.ALLOWED:
            raise ValueError("runtime not allowed")
        if any("\x00" in item or "\n" in item or item.startswith(">") or item.startswith("|") for item in argv):
            raise ValueError("unsafe argument")

    def register(self, identity: str, argv: list[str]) -> ManagedProcess:
        self.validate_argv(argv)
        item = ManagedProcess(identity, list(argv))
        self.processes[identity] = item
        return item

    def start(self, identity: str, cwd: str | None = None, env: dict[str, str] | None = None) -> ManagedProcess:
        with self.lock:
            item = self.processes[identity]
            self.validate_argv(item.argv)
            item.state = ServiceState.STARTING
            folder = self.log_root / identity
            folder.mkdir(parents=True, exist_ok=True)
            item.stdout_path = folder / "stdout.log"
            item.stderr_path = folder / "stderr.log"
            stdout = item.stdout_path.open("a", encoding="utf-8")
            stderr = item.stderr_path.open("a", encoding="utf-8")
            safe_env = {"PATH": os.environ.get("PATH", "")}
            safe_env.update({key: value for key, value in (env or {}).items() if key.isidentifier() and len(key) < 64})
            item.process = subprocess.Popen(item.argv, cwd=cwd, env=safe_env, stdout=stdout, stderr=stderr, start_new_session=True)
            item.started_at = time.time()
            item.state = ServiceState.RUNNING
            return item

    def poll(self, identity: str) -> ManagedProcess:
        item = self.processes[identity]
        if item.process is None:
            return item
        code = item.process.poll()
        if code is not None:
            item.state = ServiceState.STOPPED if code == 0 else ServiceState.CRASHED
        return item

    def stop(self, identity: str, timeout: float = 5) -> ManagedProcess:
        with self.lock:
            item = self.processes[identity]
            if item.process is None:
                return item
            item.state = ServiceState.STOPPING
            if item.process.poll() is None:
                os.killpg(item.process.pid, signal.SIGTERM)
                try:
                    item.process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    os.killpg(item.process.pid, signal.SIGKILL)
                    item.process.wait()
            item.state = ServiceState.STOPPED
            return item

    def restart(self, identity: str, cwd: str | None = None, env: dict[str, str] | None = None) -> ManagedProcess:
        self.stop(identity)
        item = self.processes[identity]
        item.restarts += 1
        return self.start(identity, cwd, env)

    def status(self) -> dict[str, str]:
        return {key: self.poll(key).state.value for key in self.processes}

    def shutdown(self) -> None:
        for identity in list(self.processes):
            try:
                self.stop(identity)
            except (KeyError, ProcessLookupError):
                pass
