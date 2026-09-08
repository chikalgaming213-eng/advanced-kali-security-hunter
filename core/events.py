from collections.abc import Callable
from models.entities import AssessmentEvent
class EventBus:
    def __init__(self): self._subscribers:list[Callable[[AssessmentEvent],None]]=[]
    def subscribe(self, fn): self._subscribers.append(fn); return fn
    def publish(self,event):
        for fn in tuple(self._subscribers):
            try: fn(event)
            except Exception: pass
