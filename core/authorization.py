from models.entities import Authorization, TargetScope
from .exceptions import PolicyViolation
class AuthorizationGate:
    def check(self, scope:TargetScope, intrusive:bool=False)->None:
        if intrusive and (scope.authorization is not Authorization.AUTHORIZED or not scope.lab_mode):
            raise PolicyViolation("Intrusive operations require AUTHORIZED + LAB_MODE")
        if scope.authorization is Authorization.LAB_ONLY and not scope.lab_mode:
            raise PolicyViolation("LAB_ONLY scope requires LAB_MODE")
    def confirmation_text(self, operation:str, target:str)->str:
        return f"CONFIRM {operation} against {target}: authorized lab scope only"
