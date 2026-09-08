class AKSHError(Exception): pass
class PolicyViolation(AKSHError): pass
class ScopeError(AKSHError): pass
class CommandNotAllowed(AKSHError): pass
class CommandTimeout(AKSHError): pass
class ConfigurationError(AKSHError): pass
