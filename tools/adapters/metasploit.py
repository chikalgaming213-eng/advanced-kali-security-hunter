from models.entities import CommandSpec
class MetasploitAdapter:
    name="metasploit"
    def build_read_only(self,target:str)->CommandSpec:
        return CommandSpec("nmap",["-sn",target],timeout=60)
