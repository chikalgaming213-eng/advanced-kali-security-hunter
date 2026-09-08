from .models import SecurityEvent,ThreatCategory
class ThreatClassifier:
    def classify(self,event:SecurityEvent)->ThreatCategory:
        if event.category is not ThreatCategory.UNKNOWN:return event.category
        if event.kind.value=='authentication' and event.action in ('failed','failure'):return ThreatCategory.AUTH_ABUSE
        if event.kind.value=='connection' and event.action in ('failed','refused','timeout'):return ThreatCategory.SUSPICIOUS_CONNECTION
        if event.kind.value=='web' and event.action in ('404','auth_failed'):return ThreatCategory.WEB_ENUMERATION
        return ThreatCategory.UNKNOWN
    def explain(self,event): return {'category':self.classify(event).value,'confidence':event.confidence,'evidence':event.evidence}

