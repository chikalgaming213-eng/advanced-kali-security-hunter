from models.entities import CommandSpec
class NucleiAdapter:
    name="nuclei"
    def build_read_only(self,target:str)->CommandSpec:
        return CommandSpec("nuclei",["-u",target],timeout=60)
