class AdapterRegistry:
    def __init__(self): self._adapters={}
    def register(self,name,adapter): self._adapters[name]=adapter
    def get(self,name): return self._adapters.get(name)
    def names(self): return sorted(self._adapters)
