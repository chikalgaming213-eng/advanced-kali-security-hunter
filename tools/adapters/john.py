from models.entities import CommandSpec
class JohnAdapter:
    name="john"
    def build_read_only(self,target:str)->CommandSpec:
        return CommandSpec("nmap",["-sn",target],timeout=60)
