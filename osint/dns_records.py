from __future__ import annotations
"""Reusable OSINT DNS records components for authorized local assessments."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

@dataclass(slots=True)
class OsintDns:
    """One normalized OSINT DNS records observation."""
    name: str = ""
    kind: str = ""
    value: float | int | str = 0
    source: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "OsintDns":
        known = {k: value[k] for k in cls.__dataclass_fields__ if k in value}
        return cls(**known)

    def identity(self) -> str:
        parts = [str(getattr(self, name, "")) for name in self.__dataclass_fields__ if name not in {"metadata", "created_at"}]
        return "|".join(parts).lower()

    def is_complete(self) -> bool:
        required = [name for name in self.__dataclass_fields__ if name not in {"metadata", "created_at"}]
        return all(getattr(self, name, None) not in (None, "") for name in required)

    def with_metadata(self, **values: Any) -> "OsintDns":
        merged = dict(self.metadata); merged.update(values)
        data = self.to_dict(); data["metadata"] = merged; return type(self).from_dict(data)

class OsintDnsCollection:
    """Deterministic in-memory collection with JSON/JSONL persistence."""
    def __init__(self, values: Iterable[OsintDns] = ()) -> None:
        self._values: list[OsintDns] = []
        self._index: dict[str, OsintDns] = {}
        for value in values: self.add(value)

    def add(self, value: OsintDns) -> bool:
        key = value.identity()
        if key in self._index: return False
        self._index[key] = value; self._values.append(value); return True

    def extend(self, values: Iterable[OsintDns]) -> int:
        count = 0
        for value in values: count += int(self.add(value))
        return count

    def remove(self, identity: str) -> bool:
        value = self._index.pop(identity, None)
        if value is None: return False
        self._values = [item for item in self._values if item.identity() != identity]; return True

    def get(self, identity: str) -> OsintDns | None: return self._index.get(identity)

    def filter(self, **criteria: Any) -> list[OsintDns]:
        return [item for item in self._values if all(getattr(item, key, None) == expected for key, expected in criteria.items())]

    def sort_by(self, field_name: str, reverse: bool = False) -> list[OsintDns]:
        if not self._values: return []
        if field_name not in self._values[0].__dataclass_fields__: raise ValueError(field_name)
        return sorted(self._values, key=lambda item: str(getattr(item, field_name, "")), reverse=reverse)

    def __len__(self) -> int: return len(self._values)
    def __iter__(self) -> Iterator[OsintDns]: return iter(tuple(self._values))
    def __getitem__(self, index: int) -> OsintDns: return self._values[index]

    def to_list(self) -> list[dict[str, Any]]: return [item.to_dict() for item in self._values]

    def save_json(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(self.to_list(), indent=2), encoding="utf-8"); return path

    def save_jsonl(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            for item in self._values: handle.write(json.dumps(item.to_dict(), sort_keys=True) + "\n")
        return path

    @classmethod
    def load_json(cls, path: Path) -> "OsintDnsCollection":
        if not path.exists(): return cls()
        raw = json.loads(path.read_text(encoding="utf-8")); return cls(OsintDns.from_dict(item) for item in raw)

    @classmethod
    def load_jsonl(cls, path: Path) -> "OsintDnsCollection":
        if not path.exists(): return cls()
        values = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip(): values.append(OsintDns.from_dict(json.loads(line)))
        return cls(values)

    def merge(self, other: "OsintDnsCollection") -> "OsintDnsCollection":
        result = OsintDnsCollection(self._values); result.extend(other); return result

    def summarize(self) -> dict[str, Any]:
        complete = sum(item.is_complete() for item in self._values)
        return {"count": len(self), "complete": complete, "incomplete": len(self) - complete}

class OsintDnsParser:
    """Conservative parser accepting mappings or delimited text."""
    def parse_mapping(self, value: Mapping[str, Any]) -> OsintDns:
        return OsintDns.from_dict(value)

    def parse_many(self, values: Iterable[Mapping[str, Any]]) -> OsintDnsCollection:
        return OsintDnsCollection(self.parse_mapping(value) for value in values)

    def parse_lines(self, text: str, delimiter: str = "|") -> OsintDnsCollection:
        rows = []
        names = list(OsintDns.__dataclass_fields__.keys())
        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith("#"): continue
            pieces = [piece.strip() for piece in line.split(delimiter)]
            row = {name: pieces[index] for index, name in enumerate(names[:len(pieces)])}
            rows.append(OsintDns.from_dict(row))
        return OsintDnsCollection(rows)

    def normalize(self, value: OsintDns) -> OsintDns:
        data = value.to_dict()
        for key, item in list(data.items()):
            if isinstance(item, str): data[key] = item.strip()
        return OsintDns.from_dict(data)

class OsintDnsValidator:
    """Validation rules shared by adapters and report generators."""
    def validate(self, value: OsintDns) -> list[str]:
        errors = []
        if not value.is_complete(): errors.append("required fields are incomplete")
        for key, item in value.to_dict().items():
            if isinstance(item, str) and ("\x00" in item or "\n" in item): errors.append(f"invalid characters in {key}")
        return errors

    def require_valid(self, value: OsintDns) -> OsintDns:
        errors = self.validate(value)
        if errors: raise ValueError("; ".join(errors))
        return value

    def validate_collection(self, values: OsintDnsCollection) -> dict[str, list[str]]:
        return {value.identity(): self.validate(value) for value in values if self.validate(value)}

class OsintDnsIndex:
    """Small query index for deterministic local analysis."""
    def __init__(self, values: OsintDnsCollection) -> None:
        self.values = values
        self.by_identity = {value.identity(): value for value in values}

    def search(self, query: str) -> list[OsintDns]:
        needle = query.casefold(); return [value for value in self.values if needle in json.dumps(value.to_dict()).casefold()]

    def group(self, field_name: str) -> dict[str, list[OsintDns]]:
        groups: dict[str, list[OsintDns]] = {}
        for value in self.values:
            key = str(getattr(value, field_name, "")); groups.setdefault(key, []).append(value)
        return groups

    def export_summary(self) -> dict[str, Any]:
        return {"records": len(self.values), "identities": len(self.by_identity), "fields": list(OsintDns.__dataclass_fields__)}


def load_records(path: str | Path) -> OsintDnsCollection:
    return OsintDnsCollection.load_json(Path(path))


def save_records(values: OsintDnsCollection, path: str | Path) -> Path:
    return values.save_json(Path(path))


def build_records(**values: Any) -> OsintDns:
    return OsintDns.from_dict(values)

