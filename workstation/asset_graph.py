from __future__ import annotations
from dataclasses import asdict
import json
from .models import AssetNode,AssetEdge
class AssetGraph:
    """In-memory directed asset graph exportable as JSON or Mermaid."""
    def __init__(self): self.nodes={};self.edges=[]
    def add_node(self,node): self.nodes[node.node_id]=node;return node
    def add_edge(self,edge):
        if edge.source not in self.nodes or edge.target not in self.nodes: raise KeyError('edge endpoint missing')
        if not any(x.source==edge.source and x.target==edge.target and x.relationship==edge.relationship for x in self.edges): self.edges.append(edge)
        return edge
    def neighbors(self,node_id,relationship=None): return [self.nodes[e.target] for e in self.edges if e.source==node_id and (relationship is None or e.relationship==relationship)]
    def search(self,query):
        q=query.casefold();return [n for n in self.nodes.values() if q in n.label.casefold() or q in json.dumps(n.properties).casefold()]
    def subgraph(self,node_ids):
        ids=set(node_ids);return {'nodes':[asdict(n) for n in self.nodes.values() if n.node_id in ids],'edges':[asdict(e) for e in self.edges if e.source in ids and e.target in ids]}
    def to_dict(self): return {'nodes':[asdict(n) for n in self.nodes.values()],'edges':[asdict(e) for e in self.edges]}
    def to_mermaid(self):
        lines=['graph TD']
        for node in self.nodes.values(): lines.append(f' {node.node_id}["{node.label}"]')
        for edge in self.edges: lines.append(f' {edge.source} -->|{edge.relationship}| {edge.target}')
        return '\n'.join(lines)
    def save(self,path): path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(self.to_dict(),indent=2),encoding='utf-8');return path

