from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BUG BOUNTY HUNTER X root launcher")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("gui", help="launch the unified PySide6 GUI")
    scan = sub.add_parser("scan", help="run a read-only authorized assessment")
    scan.add_argument("targets", nargs="+", default=["127.0.0.1"])
    scan.add_argument("--report", default="root_assessment")
    sub.add_parser("defense", help="run the defensive SOC snapshot")
    sub.add_parser("monitor", help="show workstation environment metrics")
    sub.add_parser("test", help="run the full test suite")
    return parser

def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "gui":
        return subprocess.call([sys.executable, "main.py", "--gui"], cwd=ROOT)
    if args.command == "scan":
        return subprocess.call([sys.executable, "main.py", *args.targets, "--report", args.report], cwd=ROOT)
    if args.command == "defense":
        return subprocess.call([sys.executable, "defense_cli.py", "snapshot"], cwd=ROOT)
    if args.command == "monitor":
        return subprocess.call([sys.executable, "workstation_cli.py", "monitor"], cwd=ROOT)
    if args.command == "test":
        return subprocess.call([sys.executable, "-m", "pytest", "-q"], cwd=ROOT)
    build_parser().print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(run())
