from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from models.entities import TargetScope, Authorization
from core.engine import AssessmentEngine
from reporting.generator import ReportGenerator
ROOT=Path(__file__).parent
def main():
    p=argparse.ArgumentParser(description="Advanced Kali Security Hunter — authorized read-only assessment")
    p.add_argument("targets",nargs="*",default=["127.0.0.1"]); p.add_argument("--gui",action="store_true"); p.add_argument("--report",default="assessment")
    args=p.parse_args()
    if args.gui:
        from gui.application import run_gui; return run_gui(ROOT)
    scope=TargetScope(args.targets or ["127.0.0.1"],authorization=Authorization.READ_ONLY)
    engine=AssessmentEngine(); engine.events.subscribe(lambda e: print(f"[{e.progress:>5.0%}] {e.message}"))
    findings=engine.assess(scope); out=ReportGenerator(ROOT/"data/reports").write(findings,args.report); print(f"Wrote reports to {out}")
if __name__=="__main__": main()
