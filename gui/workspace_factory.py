from __future__ import annotations
from pathlib import Path
import json
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit
from workstation.network_center import NetworkCenter
from workstation.metasploit import MetasploitWorkspace
from tools.tool_manager import ToolManager
from defense.timeline import SecurityTimeline
from core.jsonl_store import JsonlStore

class WorkspaceFactory:
    """Builds real read-only pages from the existing backend services."""
    def __init__(self, root: Path):
        self.root=root
        self.timeline=SecurityTimeline()
        self.msf=MetasploitWorkspace()
        self.tools=ToolManager(root/'tools/tool_catalog.json')
    def title(self,text):
        label=QLabel(text);label.setStyleSheet('font-size:20px;font-weight:bold;color:#52e0bd;padding:8px');return label
    def text_page(self,title,text,refresh=None):
        page=QWidget();layout=QVBoxLayout(page);layout.addWidget(self.title(title));layout.addWidget(QLabel(text));output=QTextEdit();output.setReadOnly(True);layout.addWidget(output)
        if refresh:
            button=QPushButton('REFRESH');layout.insertWidget(2,button);button.clicked.connect(lambda:self.fill(output,refresh()))
            self.fill(output,refresh())
        return page
    def fill(self,output,value):output.setPlainText(json.dumps(value,indent=2,default=str) if not isinstance(value,str) else value)
    def terminal(self):
        return self.text_page('ADVANCED TERMINAL','Terminal profiles are controlled through safe argv execution and local JSONL history. Arbitrary shell strings are not accepted.',lambda:{'profiles':['Ubuntu','Debian','Kali','Host','Project','Python','Node'],'history':str(self.root/'data/terminal/history.jsonl')})
    def metasploit(self):
        status=self.msf.detect();return self.text_page('METASPLOIT WORKSPACE','Module browsing and metadata only by default. Intrusive modules require LAB_MODE plus explicit authorization.',lambda:{'installed':status.installed,'binary':status.binary,'version':status.version,'error':status.error,'permitted_modules':len(self.msf.permitted_modules())})
    def tool_center(self):
        def data():
            statuses=self.tools.scan();return {'catalog_entries':len(self.tools.entries),'categories':len(self.tools.by_category()),'installed':sum(item.installed for item in statuses.values()),'missing':sum(not item.installed for item in statuses.values())}
        return self.text_page('TOOL CENTER','Catalog-driven detection. Missing tools are reported and never installed automatically.',data)
    def recon(self):return self.text_page('RECON CENTER','Passive and low-impact recon adapters share scope validation, rate limits, parsers, and local evidence storage.',lambda:{'adapters':['amass','subfinder','assetfinder','findomain','dig','whois'],'default_mode':'PASSIVE','evidence_root':str(self.root/'data/evidence')})
    def web(self):return self.text_page('WEB / API SECURITY','HTTP discovery, endpoint models, headers, robots rules, and normalized scanner observations are available to the read-only workflow.',lambda:{'parsers':['HTTP JSON','Nuclei JSONL','generic JSON'],'reports':str(self.root/'data/reports'),'safety':'READ_ONLY'})
    def network(self):return self.text_page('NETWORK CENTER','Network metadata is inspected without changing interfaces, routes, firewall rules, or DNS configuration.',lambda:NetworkCenter().snapshot().to_dict())
    def osint(self):return self.text_page('OSINT CENTER','Local normalization for DNS, WHOIS, passive sources, and historical observations. Provider keys are never hardcoded.',lambda:{'providers':['LOCAL ANALYSIS ONLY'],'storage':'JSON/JSONL','api_keys':'environment variables only'})
    def evidence(self):return self.text_page('EVIDENCE CENTER','Incident artifacts, JSONL event streams, SHA256 manifests, and chain-of-custody records are stored locally.',lambda:{'root':str(self.root/'data/defense/incidents'),'formats':['JSON','JSONL','TXT'],'hash':'SHA256'})
    def reports(self):return self.text_page('REPORT CENTER','Reports are generated locally from findings and JSON/JSONL evidence.',lambda:{'formats':['JSON','HTML','Markdown','TXT'],'directory':str(self.root/'data/reports')})
    def system(self,monitor):return self.text_page('SYSTEM MONITOR','Host telemetry is collected through psutil when available. Metrics are informative and do not imply a security guarantee.',lambda:monitor.snapshot().to_dict())
    def settings(self):return self.text_page('SETTINGS','Configuration is local JSON. Privileged actions and destructive changes require explicit review and confirmation.',lambda:{'default_authorization':'READ_ONLY','database':False,'automatic_installation':False,'intrusive_operations':'LAB_MODE + AUTHORIZED + confirmation'})
    def audit(self):return self.text_page('AUDIT LOGS','Security actions, workflow events, command metadata, and response decisions are written to local JSONL.',lambda:{'files':[str(self.root/'data/logs/aksh.jsonl'),str(self.root/'data/defense/response_audit.jsonl')],'retention':'local operator controlled'})
