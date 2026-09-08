from __future__ import annotations
import argparse
import json
from pathlib import Path
from defense.network_shield import NetworkShield
from defense.firewall import FirewallMonitor
from defense.connections import ConnectionMonitor
from defense.score import DefenseScoreEngine
ROOT = Path(__file__).parent

def parser():
    p=argparse.ArgumentParser(prog='defense-monster',description='DEFENSE MONSTER X local defensive SOC')
    sub=p.add_subparsers(dest='command')
    sub.add_parser('snapshot',help='collect non-invasive host and connection metadata')
    sub.add_parser('firewall',help='detect firewall backends without changing rules')
    sub.add_parser('score',help='calculate an operational defense indicator')
    return p

def main(argv=None):
    args=parser().parse_args(argv)
    if args.command=='snapshot':
        shield=NetworkShield().snapshot(); connections=ConnectionMonitor().snapshot(); print(json.dumps({'network':shield.to_dict(),'connections':connections},indent=2)); return 0
    if args.command=='firewall': print(json.dumps([item.to_dict() for item in FirewallMonitor().detect()],indent=2)); return 0
    if args.command=='score':
        score=DefenseScoreEngine().calculate(80,50,90,50,75,80,85); print(json.dumps({'score':score.total(),'disclaimer':score.disclaimer()})); return 0
    parser().print_help(); return 0
if __name__=='__main__': raise SystemExit(main())
