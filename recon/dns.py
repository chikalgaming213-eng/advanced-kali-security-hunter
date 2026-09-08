from __future__ import annotations
"""Reusable DNS enumeration components for authorized local assessments."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

@dataclass(slots=True)
class DnsRecord:
    """One normalized DNS enumeration observation."""
    name: str = ""
    record_type: str = ""
    value: float | int | str = 0
    ttl: float | int | str = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "DnsRecord":
        known = {k: value[k] for k in cls.__dataclass_fields__ if k in value}
        return cls(**known)

    def identity(self) -> str:
        parts = [str(getattr(self, name, "")) for name in self.__dataclass_fields__ if name not in {"metadata", "created_at"}]
        return "|".join(parts).lower()

    def is_complete(self) -> bool:
        required = [name for name in self.__dataclass_fields__ if name not in {"metadata", "created_at"}]
        return all(getattr(self, name, None) not in (None, "") for name in required)

    def with_metadata(self, **values: Any) -> "DnsRecord":
        merged = dict(self.metadata); merged.update(values)
        data = self.to_dict(); data["metadata"] = merged; return type(self).from_dict(data)

class DnsRecordCollection:
    """Deterministic in-memory collection with JSON/JSONL persistence."""
    def __init__(self, values: Iterable[DnsRecord] = ()) -> None:
        self._values: list[DnsRecord] = []
        self._index: dict[str, DnsRecord] = {}
        for value in values: self.add(value)

    def add(self, value: DnsRecord) -> bool:
        key = value.identity()
        if key in self._index: return False
        self._index[key] = value; self._values.append(value); return True

    def extend(self, values: Iterable[DnsRecord]) -> int:
        count = 0
        for value in values: count += int(self.add(value))
        return count

    def remove(self, identity: str) -> bool:
        value = self._index.pop(identity, None)
        if value is None: return False
        self._values = [item for item in self._values if item.identity() != identity]; return True

    def get(self, identity: str) -> DnsRecord | None: return self._index.get(identity)

    def filter(self, **criteria: Any) -> list[DnsRecord]:
        return [item for item in self._values if all(getattr(item, key, None) == expected for key, expected in criteria.items())]

    def sort_by(self, field_name: str, reverse: bool = False) -> list[DnsRecord]:
        if not self._values: return []
        if field_name not in self._values[0].__dataclass_fields__: raise ValueError(field_name)
        return sorted(self._values, key=lambda item: str(getattr(item, field_name, "")), reverse=reverse)

    def __len__(self) -> int: return len(self._values)
    def __iter__(self) -> Iterator[DnsRecord]: return iter(tuple(self._values))
    def __getitem__(self, index: int) -> DnsRecord: return self._values[index]

    def to_list(self) -> list[dict[str, Any]]: return [item.to_dict() for item in self._values]

    def save_json(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(self.to_list(), indent=2), encoding="utf-8"); return path

    def save_jsonl(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            for item in self._values: handle.write(json.dumps(item.to_dict(), sort_keys=True) + "\n")
        return path

    @classmethod
    def load_json(cls, path: Path) -> "DnsRecordCollection":
        if not path.exists(): return cls()
        raw = json.loads(path.read_text(encoding="utf-8")); return cls(DnsRecord.from_dict(item) for item in raw)

    @classmethod
    def load_jsonl(cls, path: Path) -> "DnsRecordCollection":
        if not path.exists(): return cls()
        values = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip(): values.append(DnsRecord.from_dict(json.loads(line)))
        return cls(values)

    def merge(self, other: "DnsRecordCollection") -> "DnsRecordCollection":
        result = DnsRecordCollection(self._values); result.extend(other); return result

    def summarize(self) -> dict[str, Any]:
        complete = sum(item.is_complete() for item in self._values)
        return {"count": len(self), "complete": complete, "incomplete": len(self) - complete}

class DnsRecordParser:
    """Conservative parser accepting mappings or delimited text."""
    def parse_mapping(self, value: Mapping[str, Any]) -> DnsRecord:
        return DnsRecord.from_dict(value)

    def parse_many(self, values: Iterable[Mapping[str, Any]]) -> DnsRecordCollection:
        return DnsRecordCollection(self.parse_mapping(value) for value in values)

    def parse_lines(self, text: str, delimiter: str = "|") -> DnsRecordCollection:
        rows = []
        names = list(DnsRecord.__dataclass_fields__.keys())
        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith("#"): continue
            pieces = [piece.strip() for piece in line.split(delimiter)]
            row = {name: pieces[index] for index, name in enumerate(names[:len(pieces)])}
            rows.append(DnsRecord.from_dict(row))
        return DnsRecordCollection(rows)

    def normalize(self, value: DnsRecord) -> DnsRecord:
        data = value.to_dict()
        for key, item in list(data.items()):
            if isinstance(item, str): data[key] = item.strip()
        return DnsRecord.from_dict(data)

class DnsRecordValidator:
    """Validation rules shared by adapters and report generators."""
    def validate(self, value: DnsRecord) -> list[str]:
        errors = []
        if not value.is_complete(): errors.append("required fields are incomplete")
        for key, item in value.to_dict().items():
            if isinstance(item, str) and ("\x00" in item or "\n" in item): errors.append(f"invalid characters in {key}")
        return errors

    def require_valid(self, value: DnsRecord) -> DnsRecord:
        errors = self.validate(value)
        if errors: raise ValueError("; ".join(errors))
        return value

    def validate_collection(self, values: DnsRecordCollection) -> dict[str, list[str]]:
        return {value.identity(): self.validate(value) for value in values if self.validate(value)}

class DnsRecordIndex:
    """Small query index for deterministic local analysis."""
    def __init__(self, values: DnsRecordCollection) -> None:
        self.values = values
        self.by_identity = {value.identity(): value for value in values}

    def search(self, query: str) -> list[DnsRecord]:
        needle = query.casefold(); return [value for value in self.values if needle in json.dumps(value.to_dict()).casefold()]

    def group(self, field_name: str) -> dict[str, list[DnsRecord]]:
        groups: dict[str, list[DnsRecord]] = {}
        for value in self.values:
            key = str(getattr(value, field_name, "")); groups.setdefault(key, []).append(value)
        return groups

    def export_summary(self) -> dict[str, Any]:
        return {"records": len(self.values), "identities": len(self.by_identity), "fields": list(DnsRecord.__dataclass_fields__)}


def load_dns_records(path: str | Path) -> DnsRecordCollection:
    return DnsRecordCollection.load_json(Path(path))


def save_dns_records(values: DnsRecordCollection, path: str | Path) -> Path:
    return values.save_json(Path(path))


def build_dns_records(**values: Any) -> DnsRecord:
    return DnsRecord.from_dict(values)

