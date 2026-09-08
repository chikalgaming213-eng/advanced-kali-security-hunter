from __future__ import annotations
import argparse
import json
from pathlib import Path
from workstation.environment_manager import EnvironmentManager
from workstation.system_monitor import SystemMonitor
from workstation.asset_graph import AssetGraph
from workstation.models import AssetNode, AssetEdge

ROOT = Path(__file__).parent

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bbhx", description="BUG BOUNTY HUNTER X local workstation control plane")
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("environments", help="list logical workspaces")
    commands.add_parser("monitor", help="print a local system snapshot")
    graph = commands.add_parser("graph", help="export a small JSON asset graph")
    graph.add_argument("--output", default="data/reports/asset_graph.json")
    return parser

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manager = EnvironmentManager(ROOT)
    if args.command == "environments":
        print(json.dumps([item.to_dict() for item in manager.list()], indent=2))
        return 0
    if args.command == "monitor":
        print(json.dumps(SystemMonitor().snapshot().to_dict(), indent=2))
        return 0
    if args.command == "graph":
        graph = AssetGraph()
        graph.add_node(AssetNode("program", "program", "Authorized Program"))
        graph.add_node(AssetNode("target", "domain", "Target in explicit scope"))
        graph.add_edge(AssetEdge("program", "target", "includes", 1.0))
        path = graph.save(ROOT / args.output)
        print(path)
        return 0
    build_parser().print_help()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
