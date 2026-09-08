from models.entities import Finding
class FindingCorrelator:
    def deduplicate(self,findings):
        seen=set(); out=[]
        for f in findings:
            key=(f.title.lower(),f.target,f.port,f.url)
            if key not in seen: seen.add(key); out.append(f)
        return out
    def severity_score(self,finding): return {"INFO":0,"LOW":1,"MEDIUM":2,"HIGH":3,"CRITICAL":4}[finding.severity.value]
