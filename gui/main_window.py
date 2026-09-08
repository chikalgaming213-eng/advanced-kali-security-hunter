from pathlib import Path
from PySide6.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QListWidget,QTextEdit,QLineEdit,QPushButton,QLabel
from models.entities import TargetScope,Authorization
from core.engine import AssessmentEngine
from reporting.generator import ReportGenerator
class MainWindow(QMainWindow):
    def __init__(self,root:Path):
        super().__init__(); self.root=root; self.setWindowTitle("ADVANCED KALI SECURITY HUNTER"); self.resize(1100,700); self.setStyleSheet("QWidget{background:#10151b;color:#d6e2ea} QPushButton{background:#00a878;padding:10px} QLineEdit,QTextEdit{background:#18232d;border:1px solid #31505d;padding:8px}")
        left=QListWidget(); left.addItems(["Dashboard","Target Manager","Recon","Network Scanner","Web Scanner","Vulnerability Scanner","OSINT","Tool Manager","Metasploit Manager","Reports","Settings","Logs"])
        target=QLineEdit("127.0.0.1"); start=QPushButton("START READ-ONLY ASSESSMENT"); self.output=QTextEdit(); self.output.setReadOnly(True); start.clicked.connect(lambda:self.run(target.text()))
        panel=QWidget(); lay=QVBoxLayout(panel); lay.addWidget(QLabel("Target (authorized scope)")); lay.addWidget(target); lay.addWidget(start); lay.addWidget(QLabel("Terminal Output / Findings")); lay.addWidget(self.output)
        rootw=QWidget(); h=QHBoxLayout(rootw); h.addWidget(left,1); h.addWidget(panel,4); self.setCentralWidget(rootw)
    def run(self,target):
        e=AssessmentEngine(); e.events.subscribe(lambda ev:self.output.append(f"{ev.progress:.0%} {ev.message}")); fs=e.assess(TargetScope([target],authorization=Authorization.READ_ONLY)); ReportGenerator(self.root/"data/reports").write(fs,"gui_assessment"); self.output.append(f"Completed: {len(fs)} finding(s). Reports saved locally.")
