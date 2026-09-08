from models.entities import CommandSpec
class HydraAdapter:
    name="hydra"
    def build_read_only(self,target:str)->CommandSpec:
        return CommandSpec("nmap",["-sn",target],timeout=60)
