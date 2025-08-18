from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List


def sanitize(name: str) -> str:
    """Convert any string into a valid Python identifier."""
    if not isinstance(name, str):
        name = str(name)
    name = re.sub(r"[^a-zA-Z0-9\s]", "_", name)
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"_+", "_", name)
    name = name.strip("_")
    if not name or not name[0].isalpha():
        name = "X" + name
    return name


@dataclass
class DimensionEnv:
    """
    Simple dot-accessible container for code lists.
    """
    _attrs: Dict[str, str] = field(default_factory=dict)

    def __getattr__(self, item: str) -> str:
        try:
            return self._attrs[item]
        except KeyError as e:
            raise AttributeError(item) from e

    def __dir__(self) -> List[str]:
        return sorted(list(self._attrs.keys()))

    def __repr__(self) -> str:
        pairs = ", ".join(f"{k}={v!r}" for k, v in self._attrs.items())
        return f"DimensionEnv({pairs})"


def make_env_from_pairs(pairs: Iterable[tuple[str, str]]) -> DimensionEnv:
    attrs: Dict[str, str] = {}
    for label, code in pairs:
        key = sanitize(label)
        if key not in attrs:
            attrs[key] = code
        # silently skip duplicates
    return DimensionEnv(attrs)


def old_make_key_str(key: List[List[str]]) -> str:
    """
    Convert list-of-lists to SDMX key string.
    Example: [["USA","CAN"], ["LUR"], ["A"]] -> "USA+CAN.LUR.A"
    """
    return ".".join("+".join(inner) if inner else "" for inner in key)


def make_key_str(key) -> str:
    parts = []
    for group in key:
        if group is None or (isinstance(group, list) and len(group) == 0):
            part = ""
        elif isinstance(group, str):
            part = str(group)  # single string
        else:
            # Assume it's an iterable (list, tuple, R vector, etc.)
            items = [str(x) for x in group if x is not None and x != "" and not str(x).lower() == "null"]
            part = "+".join(items) if items else ""
        parts.append(part)
    return ".".join(parts)

