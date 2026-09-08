from models.entities import CommandSpec
class WiresharkAdapter:
    name="wireshark"
    def build_read_only(self,target:str)->CommandSpec:
        return CommandSpec("tshark",["--version",target],timeout=60)
