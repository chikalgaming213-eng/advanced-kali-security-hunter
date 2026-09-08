import json
from pathlib import Path
from tools.tool_manager import ToolManager
def test_catalog():
    p=Path(__file__).parents[1]/"tools/tool_catalog.json"; data=json.loads(p.read_text()); assert len(data)>=600; assert {"name","category","binary"}<=data[0].keys()
def test_manager():
    m=ToolManager(Path(__file__).parents[1]/"tools/tool_catalog.json"); assert len(m.by_category())>=10
