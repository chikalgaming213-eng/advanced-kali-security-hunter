import json, logging
from pathlib import Path
class JsonlHandler(logging.Handler):
    def __init__(self,path:Path): super().__init__(); path.parent.mkdir(parents=True,exist_ok=True); self.path=path
    def emit(self,record):
        with self.path.open("a",encoding="utf-8") as f: f.write(json.dumps({"time":self.format(record),"level":record.levelname,"message":record.getMessage()})+"\n")
def configure(path:Path):
    logger=logging.getLogger("aksh"); logger.setLevel(logging.INFO); logger.handlers.clear(); logger.addHandler(JsonlHandler(path)); return logger
