"""Target Manager page model; Qt widgets are intentionally kept out of core logic."""
from dataclasses import dataclass, field
@dataclass(slots=True)
class PageState:
    title: str = "Target Manager"
    status: str = "ready"
    messages: list[str] = field(default_factory=list)
    def add(self,message: str) -> None: self.messages.append(message)
    def clear(self) -> None: self.messages.clear()
    def summary(self) -> dict: return {"title":self.title,"status":self.status,"messages":len(self.messages)}

