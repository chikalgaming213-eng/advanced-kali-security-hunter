from __future__ import annotations
import json, html
from pathlib import Path
from models.entities import Finding
class ReportGenerator:
    def __init__(self,out_dir:Path): self.out_dir=out_dir; self.out_dir.mkdir(parents=True,exist_ok=True)
    def write(self,findings:list[Finding],stem="assessment"):
        data=[f.to_dict() for f in findings]
        (self.out_dir/f"{stem}.json").write_text(json.dumps(data,indent=2),encoding="utf-8")
        md=[f"# Assessment Report\n\nFindings: {len(data)}\n"]+[f"## {f.title} ({f.severity.value})\n\n- Target: {f.target}\n- Tool: {f.tool}\n- Description: {f.description}\n- Remediation: {f.remediation}\n" for f in findings]
        (self.out_dir/f"{stem}.md").write_text("\n".join(md),encoding="utf-8")
        rows="".join(f"<tr><td>{html.escape(f.finding_id)}</td><td>{html.escape(f.severity.value)}</td><td>{html.escape(f.title)}</td><td>{html.escape(f.target)}</td></tr>" for f in findings)
        (self.out_dir/f"{stem}.html").write_text(f"<html><body><h1>Assessment Report</h1><table><tr><th>ID</th><th>Severity</th><th>Title</th><th>Target</th></tr>{rows}</table></body></html>",encoding="utf-8")
        (self.out_dir/f"{stem}.txt").write_text("\n".join(f"{f.finding_id} [{f.severity.value}] {f.title} - {f.target}" for f in findings),encoding="utf-8")
        return self.out_dir
