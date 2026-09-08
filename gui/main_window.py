from __future__ import annotations
from pathlib import Path
import json
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QStackedWidget, QTextEdit, QLineEdit, QPushButton, QLabel, QProgressBar, QFormLayout, QTableWidget
from models.entities import TargetScope, Authorization
from core.engine import AssessmentEngine
from reporting.generator import ReportGenerator
from workstation.environment_manager import EnvironmentManager
from workstation.system_monitor import SystemMonitor
from defense.soc_facade import DefenseSocFacade
from gui.workspace_factory import WorkspaceFactory

class UnifiedMainWindow(QMainWindow):
    """Single GUI shell integrating all local research and defensive workspaces."""
    NAVIGATION=['MAIN SECURITY HUNTER','DEFENSE MONSTER SOC','ANTI DOS / DDOS MONITOR','MALWARE RISK MONITOR','UBUNTU KDE ENVIRONMENT','DEBIAN XFCE ENVIRONMENT','ADVANCED TERMINAL','METASPLOIT WORKSPACE','TOOL CENTER','RECON CENTER','WEB / API SECURITY','NETWORK CENTER','OSINT CENTER','EVIDENCE CENTER','REPORT CENTER','SYSTEM MONITOR','SETTINGS','AUDIT LOGS']
    def __init__(self,root:Path):
        super().__init__();self.root=root;self.setWindowTitle('KALI SECURITY HUNTER PRO ULTIMATE — Unified Workstation');self.resize(1440,900)
        self.setStyleSheet('''QWidget{background:#091017;color:#d7e3ea;font-size:13px} QListWidget,QTextEdit,QLineEdit,QTableWidget{background:#111d26;border:1px solid #294451;padding:7px} QPushButton{background:#00a878;color:white;border:0;border-radius:4px;padding:9px} QPushButton:hover{background:#16c995} QProgressBar{background:#111d26;border:1px solid #294451;text-align:center} QProgressBar::chunk{background:#00a878}''')
        self.environment=EnvironmentManager(root);self.monitor=SystemMonitor();self.soc=DefenseSocFacade(root);self.factory=WorkspaceFactory(root)
        self.navigation=QListWidget();self.navigation.addItems(self.NAVIGATION);self.stack=QStackedWidget();self.build_pages();self.navigation.currentRowChanged.connect(self.stack.setCurrentIndex);self.navigation.setCurrentRow(0)
        root_widget=QWidget();layout=QHBoxLayout(root_widget);layout.addWidget(self.navigation,1);layout.addWidget(self.stack,5);self.setCentralWidget(root_widget)
        self.timer=QTimer(self);self.timer.timeout.connect(self.refresh_all);self.timer.start(5000);self.refresh_all()
    def title(self,text):label=QLabel(text);label.setStyleSheet('font-size:20px;font-weight:bold;color:#52e0bd;padding:8px');return label
    def metric(self,name):bar=QProgressBar();bar.setFormat(f'{name}: %p%');bar.setRange(0,100);return bar
    def add(self,widget):self.stack.addWidget(widget)
    def build_pages(self):
        self.add(self.hunter_page());self.add(self.soc_page());self.add(self.traffic_page());self.add(self.malware_page());self.add(self.environment_page('ubuntu_kde','UBUNTU KDE CONTROL CENTER'));self.add(self.environment_page('debian_xfce','DEBIAN XFCE SECURITY DESKTOP'))
        for page in (self.factory.terminal(),self.factory.metasploit(),self.factory.tool_center(),self.factory.recon(),self.factory.web(),self.factory.network(),self.factory.osint(),self.factory.evidence(),self.factory.reports(),self.factory.system(self.monitor),self.factory.settings(),self.factory.audit()):self.add(page)
    def hunter_page(self):
        page=QWidget();layout=QVBoxLayout(page);layout.addWidget(self.title('KALI SECURITY HUNTER PRO ULTIMATE'))
        form=QFormLayout();self.target=QLineEdit('127.0.0.1');form.addRow('Authorized target scope',self.target);layout.addLayout(form);button=QPushButton('START READ-ONLY ASSESSMENT');button.clicked.connect(self.run_assessment);layout.addWidget(button);layout.addWidget(QLabel('Core engine: scope → authorization → policy → rate limit → command validation → evidence → report'));self.hunter_output=QTextEdit();self.hunter_output.setReadOnly(True);layout.addWidget(self.hunter_output);return page
    def soc_page(self):
        page=QWidget();layout=QVBoxLayout(page);layout.addWidget(self.title('DEFENSE MONSTER X — LOCAL SOC'));layout.addWidget(QLabel('Read-only defense telemetry. No retaliation, counter-attack, auto-kill, or silent firewall mutation.'));self.soc_output=QTextEdit();self.soc_output.setReadOnly(True);layout.addWidget(self.soc_output);refresh=QPushButton('REFRESH SOC');refresh.clicked.connect(self.refresh_soc);layout.addWidget(refresh);return page
    def traffic_page(self):
        page=QWidget();layout=QVBoxLayout(page);layout.addWidget(self.title('ANTI DOS / DDOS MONITOR'));layout.addWidget(QLabel('Traffic pressure indicators only; the system never floods, blocks, or attacks a source automatically.'));self.traffic_output=QTextEdit();self.traffic_output.setReadOnly(True);layout.addWidget(self.traffic_output);return page
    def malware_page(self):
        page=QWidget();layout=QVBoxLayout(page);layout.addWidget(self.title('MALWARE RISK MONITOR'));layout.addWidget(QLabel('Conservative heuristics require manual review and never terminate processes automatically.'));self.malware_output=QTextEdit();self.malware_output.setReadOnly(True);layout.addWidget(self.malware_output);return page
    def environment_page(self,kind,title):
        page=QWidget();layout=QVBoxLayout(page);layout.addWidget(self.title(title));layout.addWidget(QLabel(f'Logical environment: {kind}'));cpu=self.metric('CPU');ram=self.metric('RAM');disk=self.metric('DISK');setattr(self,f'{kind}_cpu',cpu);setattr(self,f'{kind}_ram',ram);setattr(self,f'{kind}_disk',disk);layout.addWidget(cpu);layout.addWidget(ram);layout.addWidget(disk);layout.addWidget(QLabel('Services, processes, filesystem, and package actions are displayed through explicit reviewed operations.'));return page
    def run_assessment(self):
        engine=AssessmentEngine();engine.events.subscribe(lambda event:self.hunter_output.append(f'{event.progress:.0%} {event.message}'));findings=engine.assess(TargetScope([self.target.text()],authorization=Authorization.READ_ONLY));ReportGenerator(self.root/'data/reports').write(findings,'unified_gui_assessment');self.hunter_output.append(f'Completed: {len(findings)} finding(s). Reports saved locally.')
    def refresh_soc(self):
        try:self.soc_output.setPlainText(json.dumps(self.soc.snapshot(),indent=2,default=str))
        except Exception as exc:self.soc_output.setPlainText(f'SOC collection unavailable: {exc}')
    def refresh_all(self):
        snapshot=self.monitor.snapshot()
        for kind in ('ubuntu_kde','debian_xfce'):
            getattr(self,f'{kind}_cpu').setValue(int(snapshot.cpu_percent));getattr(self,f'{kind}_ram').setValue(int(snapshot.ram_percent));getattr(self,f'{kind}_disk').setValue(int(snapshot.disk_percent))
        self.refresh_soc();self.malware_output.setPlainText(json.dumps([item.to_dict() for item in self.soc.malware.process_indicators()],indent=2));self.traffic_output.setPlainText(json.dumps(self.soc.traffic.snapshot(),indent=2))
