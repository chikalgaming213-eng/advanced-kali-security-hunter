from dataclasses import dataclass
@dataclass(slots=True)
class DefenseScore:
    firewall:float;ids:float;monitoring:float;patch_status:float;open_ports:float;threat_activity:float;configuration:float
    def total(self):return round(sum((self.firewall,self.ids,self.monitoring,self.patch_status,self.open_ports,self.threat_activity,self.configuration))/7,2)
    def disclaimer(self):return 'Defense score is an operational indicator, not a guarantee of security.'
class DefenseScoreEngine:
    def calculate(self,firewall,ids,monitoring,patch_status,open_ports,threat_activity,configuration):return DefenseScore(firewall,ids,monitoring,patch_status,open_ports,threat_activity,configuration)

