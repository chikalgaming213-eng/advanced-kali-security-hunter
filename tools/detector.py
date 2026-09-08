from __future__ import annotations
import shutil,subprocess
from dataclasses import dataclass
@dataclass
class ToolStatus: name:str; binary:str; installed:bool; version:str=""; error:str=""
class ToolDetector:
    def detect(self,entry):
        binary=entry["binary"]; path=shutil.which(binary)
        if not path:return ToolStatus(entry["name"],binary,False)
        try:
            p=subprocess.run([path,"--version"],capture_output=True,text=True,timeout=3)
            return ToolStatus(entry["name"],binary,True,(p.stdout or p.stderr).splitlines()[0][:200] if (p.stdout or p.stderr) else "unknown")
        except Exception as e:return ToolStatus(entry["name"],binary,True,error=str(e))
