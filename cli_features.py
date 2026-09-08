from __future__ import annotations
import argparse,json
from pathlib import Path
from models.entities import TargetScope,Authorization
from core.workflow import AssessmentWorkflow,WorkflowContext
from reporting.generator import ReportGenerator
def run_workflow(targets:list[str],output:Path,report_name:str)->Path:
    workflow=AssessmentWorkflow(); workflow.attach_default_steps(); context=workflow.run(WorkflowContext(TargetScope(targets,authorization=Authorization.READ_ONLY))); return ReportGenerator(output).write(context.findings,report_name)
def build_parser()->argparse.ArgumentParser:
    parser=argparse.ArgumentParser(prog="aksh"); sub=parser.add_subparsers(dest="command")
    scan=sub.add_parser("scan"); scan.add_argument("targets",nargs="+",default=["127.0.0.1"]); scan.add_argument("--output",default="data/reports"); scan.add_argument("--name",default="assessment")
    return parser
def dispatch(argv=None):
    args=build_parser().parse_args(argv)
    if args.command=="scan": return run_workflow(args.targets,Path(args.output),args.name)
    return None

