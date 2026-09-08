from __future__ import annotations
import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass
@dataclass(slots=True)
class ParsedRecord:
    source:str
    target:str
    kind:str
    data:dict
class ToolOutputParser:
    """Parse bounded, local output without executing the originating tool."""
    def parse_nmap_xml(self,text:str)->list[ParsedRecord]:
        root=ET.fromstring(text); records=[]
        for host in root.findall(".//host"):
            address=host.find("address"); target=address.attrib.get("addr","") if address is not None else ""
            for port in host.findall(".//port"):
                state=port.find("state"); service=port.find("service"); records.append(ParsedRecord("nmap",target,"port",{"port":int(port.attrib.get("portid",0)),"protocol":port.attrib.get("protocol",""),"state":state.attrib.get("state","") if state is not None else "","service":service.attrib.get("name","") if service is not None else ""}))
        return records
    def parse_nuclei_jsonl(self,text:str)->list[ParsedRecord]:
        records=[]
        for line in text.splitlines():
            if not line.strip(): continue
            item=json.loads(line); info=item.get("info",{}); records.append(ParsedRecord("nuclei",str(item.get("host") or item.get("matched-at") or ""),"finding",{"id":item.get("template-id",""),"title":info.get("name",""),"severity":info.get("severity","info"),"description":info.get("description",""),"url":item.get("matched-at"),"evidence":[json.dumps(item,sort_keys=True)]}))
        return records
    def parse_json(self,text:str,source:str)->list[ParsedRecord]:
        data=json.loads(text); values=data if isinstance(data,list) else data.get("items",[data])
        return [ParsedRecord(source,str(item.get("target","")),str(item.get("kind","record")),item) for item in values if isinstance(item,dict)]
    def to_observations(self,records:list[ParsedRecord])->list[dict]:
        observations=[]
        for record in records:
            item=dict(record.data); item.setdefault("target",record.target); item.setdefault("tool",record.source); observations.append(item)
        return observations

