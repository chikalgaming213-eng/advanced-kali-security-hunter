from __future__ import annotations
from pathlib import Path
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QTextEdit, QLineEdit, QPushButton, QLabel, QTabWidget, QFormLayout, QProgressBar
from models.entities import TargetScope, Authorization
from core.engine import AssessmentEngine
from reporting.generator import ReportGenerator
from workstation.environment_manager import EnvironmentManager
from workstation.system_monitor import SystemMonitor

class MainWindow(QMainWindow):
    """Modern operator dashboard; all actions remain local and explicit."""
    def __init__(self, root: Path):
        super().__init__()
        self.root = root
        self.setWindowTitle("BUG BOUNTY HUNTER X — Security Workstation")
        self.resize(1280, 800)
        self.setStyleSheet("""
            QWidget { background:#0b1117; color:#d6e2ea; font-size:13px; }
            QListWidget,QTextEdit,QLineEdit { background:#121c25; border:1px solid #284150; padding:8px; }
            QPushButton { background:#00a878; color:white; border:0; border-radius:4px; padding:10px; }
            QPushButton:hover { background:#16c995; }
            QProgressBar { border:1px solid #284150; text-align:center; background:#121c25; }
            QProgressBar::chunk { background:#00a878; }
        """)
        self.environment_manager = EnvironmentManager(root)
        self.monitor = SystemMonitor()
        navigation = QListWidget()
        navigation.addItems(["Dashboard", "Security Hunter", "Ubuntu KDE Workspace", "Debian XFCE Workspace", "Advanced Terminal", "Local VPS Center", "Bot Server Center", "Network Center", "Recon Center", "Web/API Security", "Vulnerability Center", "OSINT Center", "Evidence Center", "Report Center", "Metasploit Workspace", "Tool Center", "System Monitor", "Settings", "Logs"])
        self.output = QTextEdit(); self.output.setReadOnly(True)
        self.target = QLineEdit("127.0.0.1")
        start = QPushButton("START READ-ONLY ASSESSMENT")
        start.clicked.connect(lambda: self.run_assessment(self.target.text()))
        refresh = QPushButton("REFRESH SYSTEM MONITOR")
        refresh.clicked.connect(self.refresh_monitor)
        self.cpu = self.metric("CPU"); self.ram = self.metric("RAM"); self.disk = self.metric("DISK")
        overview = QWidget(); overview_layout = QVBoxLayout(overview)
        title = QLabel("BUG BOUNTY HUNTER X  |  AUTHORIZED SECURITY WORKSTATION")
        overview_layout.addWidget(title)
        cards = QHBoxLayout()
        for label, widget in (("CPU", self.cpu), ("RAM", self.ram), ("DISK", self.disk)): cards.addWidget(self.card(label, widget))
        overview_layout.addLayout(cards)
        form = QFormLayout(); form.addRow("Authorized target", self.target); overview_layout.addLayout(form); overview_layout.addWidget(start); overview_layout.addWidget(refresh)
        overview_layout.addWidget(QLabel("Workspaces"))
        workspace_text = "\n".join(f"• {env.name}: {env.kind.value} — {env.status.value}" for env in self.environment_manager.list())
        overview_layout.addWidget(QLabel(workspace_text)); overview_layout.addWidget(QLabel("Terminal Output / Findings")); overview_layout.addWidget(self.output)
        tabs = QTabWidget(); tabs.addTab(overview, "Dashboard"); tabs.addTab(self.workspace_panel(), "Workspace Control")
        root_widget = QWidget(); layout = QHBoxLayout(root_widget); layout.addWidget(navigation, 1); layout.addWidget(tabs, 4); self.setCentralWidget(root_widget)
        self.timer = QTimer(self); self.timer.timeout.connect(self.refresh_monitor); self.timer.start(5000); self.refresh_monitor()

    def metric(self, label: str) -> QProgressBar:
        bar = QProgressBar(); bar.setRange(0, 100); bar.setFormat(f"{label} %p%"); return bar

    def card(self, label: str, widget: QProgressBar) -> QWidget:
        card = QWidget(); layout = QVBoxLayout(card); layout.addWidget(QLabel(label)); layout.addWidget(widget); return card

    def workspace_panel(self) -> QWidget:
        panel = QWidget(); layout = QVBoxLayout(panel); layout.addWidget(QLabel("Independent workspace backends are local and database-free."))
        for env in self.environment_manager.list(): layout.addWidget(QLabel(f"{env.name}  |  status: {env.status.value}  |  purpose: {env.kind.value}"))
        return panel

    def refresh_monitor(self) -> None:
        snapshot = self.monitor.snapshot(); self.cpu.setValue(int(snapshot.cpu_percent)); self.ram.setValue(int(snapshot.ram_percent)); self.disk.setValue(int(snapshot.disk_percent))

    def run_assessment(self, target: str) -> None:
        engine = AssessmentEngine(); engine.events.subscribe(lambda event: self.output.append(f"{event.progress:.0%} {event.message}"))
        findings = engine.assess(TargetScope([target], authorization=Authorization.READ_ONLY))
        ReportGenerator(self.root / "data/reports").write(findings, "gui_assessment")
        self.output.append(f"Completed: {len(findings)} finding(s). Reports saved locally.")
