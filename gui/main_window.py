from __future__ import annotations
from pathlib import Path
import json
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QStackedWidget, QTextEdit, QLineEdit, QPushButton, QLabel, QProgressBar, QFormLayout, QTableWidget, QTableWidgetItem, QTabWidget
from models.entities import TargetScope, Authorization
from core.engine import AssessmentEngine
from reporting.generator import ReportGenerator
from workstation.environment_manager import EnvironmentManager
from workstation.system_monitor import SystemMonitor
from defense.soc_facade import DefenseSocFacade
from workstation.metasploit import MetasploitWorkspace

class UnifiedMainWindow(QMainWindow):
    """One GUI shell for the complete local authorized workstation."""
    def __init__(self, root: Path):
        super().__init__(); self.root=root; self.setWindowTitle('BUG BOUNTY HUNTER X — Unified Security Workstation'); self.resize(1440,900)
        self.setStyleSheet('''QWidget{background:#091017;color:#d7e3ea;font-size:13px} QListWidget,QTextEdit,QLineEdit,QTableWidget{background:#111d26;border:1px solid #294451;padding:7px} QPushButton{background:#00a878;color:white;border:0;border-radius:4px;padding:9px} QPushButton:hover{background:#16c995} QProgressBar{background:#111d26;border:1px solid #294451;text-align:center} QProgressBar::chunk{background:#00a878} QTabWidget::pane{border:1px solid #294451}''')
        self.environment=EnvironmentManager(root); self.monitor=SystemMonitor(); self.soc=DefenseSocFacade(root); self.msf=MetasploitWorkspace(); self.pages={}
        nav=QListWidget(); nav.addItems(['MAIN SECURITY HUNTER','DEFENSE MONSTER SOC','ANTI DOS / DDOS MONITOR','MALWARE RISK MONITOR','UBUNTU KDE ENVIRONMENT','DEBIAN XFCE ENVIRONMENT','ADVANCED TERMINAL','METASPLOIT WORKSPACE','TOOL CENTER','RECON CENTER','WEB / API SECURITY','NETWORK CENTER','OSINT CENTER','EVIDENCE CENTER','REPORT CENTER','SYSTEM MONITOR','SETTINGS','AUDIT LOGS'])
        self.stack=QStackedWidget(); self.build_pages(); nav.currentRowChanged.connect(self.stack.setCurrentIndex); nav.setCurrentRow(0)
        rootw=QWidget(); layout=QHBoxLayout(rootw); layout.addWidget(nav,1); layout.addWidget(self.stack,5); self.setCentralWidget(rootw)
        self.timer=QTimer(self); self.timer.timeout.connect(self.refresh_all); self.timer.start(5000); self.refresh_all()
    def title(self,text): label=QLabel(text); label.setStyleSheet('font-size:20px;font-weight:bold;color:#52e0bd;padding:8px'); return label
    def metric(self,name): bar=QProgressBar();bar.setFormat(f'{name}: %p%');bar.setRange(0,100);return bar
    def build_pages(self):
        self.add_page('MAIN SECURITY HUNTER',self.hunter_page()); self.add_page('DEFENSE MONSTER SOC',self.soc_page()); self.add_page('ANTI DOS / DDOS MONITOR',self.traffic_page()); self.add_page('MALWARE RISK MONITOR',self.malware_page()); self.add_page('UBUNTU KDE ENVIRONMENT',self.environment_page('ubuntu_kde','Ubuntu KDE Control Center')); self.add_page('DEBIAN XFCE ENVIRONMENT',self.environment_page('debian_xfce','Debian XFCE Security Desktop'))
        for name in ['ADVANCED TERMINAL','METASPLOIT WORKSPACE','TOOL CENTER','RECON CENTER','WEB / API SECURITY','NETWORK CENTER','OSINT CENTER','EVIDENCE CENTER','REPORT CENTER','SYSTEM MONITOR','SETTINGS','AUDIT LOGS']: self.add_page(name,self.placeholder_page(name))
    def add_page(self,name,widget): self.pages[name]=widget;self.stack.addWidget(widget)
    def hunter_page(self):
        page=QWidget();layout=QVBoxLayout(page);layout.addWidget(self.title('BUG BOUNTY HUNTER X — MAIN SECURITY HUNTER'))
        form=QFormLayout();self.target=QLineEdit('127.0.0.1');form.addRow('Authorized target scope',self.target);layout.addLayout(form);button=QPushButton('START READ-ONLY ASSESSMENT');button.clicked.connect(self.run_assessment);layout.addWidget(button)
        layout.addWidget(QLabel('Integrated workspaces: Recon • Scanner • Web/API • OSINT • Vulnerability • Evidence • Reports • Tools'));self.hunter_output=QTextEdit();self.hunter_output.setReadOnly(True);layout.addWidget(self.hunter_output);return page
    def soc_page(self):
        page=QWidget();layout=QVBoxLayout(page);layout.addWidget(self.title('DEFENSE MONSTER X — LOCAL SECURITY OPERATIONS CENTER'));self.soc_output=QTextEdit();self.soc_output.setReadOnly(True);layout.addWidget(QLabel('Read-only host defense overview. No retaliation, counter-attack, auto-kill, or silent firewall changes.'));refresh=QPushButton('REFRESH DEFENSE SOC');refresh.clicked.connect(self.refresh_soc);layout.addWidget(refresh);layout.addWidget(self.soc_output);return page
    def traffic_page(self):
        page=QWidget();layout=QVBoxLayout(page);layout.addWidget(self.title('ANTI DOS / DDOS MONITOR'));layout.addWidget(QLabel('Detects traffic pressure indicators only. It does not block, retaliate, or attack sources.'));self.traffic_table=QTableWidget(0,6);self.traffic_table.setHorizontalHeaderLabels(['Source','Event','Score','Level','Confidence','Rationale']);layout.addWidget(self.traffic_table);return page
    def malware_page(self):
        page=QWidget();layout=QVBoxLayout(page);layout.addWidget(self.title('MALWARE RISK MONITOR'));layout.addWidget(QLabel('Conservative heuristics produce review signals, not malware verdicts. Processes are never killed automatically.'));self.malware_output=QTextEdit();self.malware_output.setReadOnly(True);scan=QPushButton('SCAN PROCESS RISK INDICATORS');scan.clicked.connect(self.refresh_malware);layout.addWidget(scan);layout.addWidget(self.malware_output);return page
    def environment_page(self,kind,title):
        page=QWidget();layout=QVBoxLayout(page);layout.addWidget(self.title(title));env=self.environment.get(kind);layout.addWidget(QLabel(f'Independent logical environment: {kind}'));self.env_cpu=self.metric('CPU');self.env_ram=self.metric('RAM');self.env_disk=self.metric('DISK');layout.addWidget(self.env_cpu);layout.addWidget(self.env_ram);layout.addWidget(self.env_disk);layout.addWidget(QLabel('Services, processes, files, and package actions are displayed through explicit reviewed operations.'));return page
    def placeholder_page(self,name):
        page=QWidget();layout=QVBoxLayout(page);layout.addWidget(self.title(name));layout.addWidget(QLabel('Workspace integrated into unified navigation. Backend services remain local, database-free, and policy controlled.'));return page
    def run_assessment(self):
        engine=AssessmentEngine();engine.events.subscribe(lambda event:self.hunter_output.append(f'{event.progress:.0%} {event.message}'));findings=engine.assess(TargetScope([self.target.text()],authorization=Authorization.READ_ONLY));ReportGenerator(self.root/'data/reports').write(findings,'unified_gui_assessment');self.hunter_output.append(f'Completed: {len(findings)} finding(s). Reports saved locally.')
    def refresh_soc(self):
        try:self.soc_output.setPlainText(json.dumps(self.soc.snapshot(),indent=2,default=str))
        except Exception as exc:self.soc_output.setPlainText(f'SOC collection unavailable: {exc}')
    def refresh_malware(self):
        values=self.soc.malware.process_indicators();self.malware_output.setPlainText(json.dumps([x.to_dict() for x in values],indent=2))
    def refresh_all(self):
        snap=self.monitor.snapshot();
        if hasattr(self,'env_cpu'): self.env_cpu.setValue(int(snap.cpu_percent));self.env_ram.setValue(int(snap.ram_percent));self.env_disk.setValue(int(snap.disk_percent))
        self.refresh_soc();self.refresh_malware()
