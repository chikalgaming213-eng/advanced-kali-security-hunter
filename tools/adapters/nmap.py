from models.entities import CommandSpec
class NmapAdapter:
    name="nmap"
    def build_read_only(self,target:str)->CommandSpec:
        return CommandSpec("nmap",["-sV",target],timeout=60)
