"""KeyMapper: a dict whose keys can also be paths into nested data.

    km = KeyMapper({"servers": [{"ip": "10.0.0.1"}]})
    km["servers.0.ip"]          # "10.0.0.1"
    km["servers", 0, "ip"]      # the same, as a tuple path
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import Any

__all__ = ["KeyMapper"]
__version__ = "2.0.0"

_INDEX = re.compile(r"-?[0-9]+")
_MISSING = object()


class KeyMapper(dict):
    """A dict that also reads, writes, and deletes values by path.

    A path is a string joined by the delimiter ("." by default), such as
    "servers.0.ip", or a tuple of parts, such as ("servers", 0, "ip"). Each
    part is a key into a mapping (tried as written, then as an integer when it
    looks like one) or an index into a list or tuple, negative indexes
    included. A key that exists exactly as written always wins, so keys that
    contain the delimiter still work. A missing path raises KeyError naming
    it; writing to a path creates missing mappings along the way.
    """

    __slots__ = ("delimiter",)

    def __init__(self, *args: Any, delimiter: str = ".", **kwargs: Any) -> None:
        if not isinstance(delimiter, str) or not delimiter:
            raise ValueError("delimiter must be a non-empty string")
        super().__init__(*args, **kwargs)
        self.delimiter = delimiter

    def _path(self, key: Any) -> tuple | None:
        """Return the parts of the path key names, or None for a plain key."""
        if dict.__contains__(self, key):
            return None
        if isinstance(key, tuple):
            return key or None
        if isinstance(key, str) and self.delimiter in key:
            return tuple(key.split(self.delimiter))
        return None

    def _join(self, parts: tuple) -> str:
        return self.delimiter.join(map(str, parts))

    def _parent(self, parts: tuple, create: bool = False) -> Any:
        """Return the container that holds the last part of the path."""
        node: Any = self
        for i, part in enumerate(parts[:-1]):
            child = _step(node, part)
            if child is _MISSING:
                if not (create and isinstance(node, MutableMapping)):
                    raise KeyError(self._join(parts[: i + 1]))
                child = {}
                _set(node, part, child)
            node = child
        return node

    def __getitem__(self, key: Any) -> Any:
        parts = self._path(key)
        if parts is None:
            return dict.__getitem__(self, key)
        value = _step(self._parent(parts), parts[-1])
        if value is _MISSING:
            raise KeyError(self._join(parts))
        return value

    def __setitem__(self, key: Any, value: Any) -> None:
        parts = self._path(key)
        if parts is None:
            dict.__setitem__(self, key, value)
            return
        parent, last = self._parent(parts, create=True), parts[-1]
        if isinstance(parent, MutableMapping):
            _set(parent, _mapping_key(parent, last), value)
        elif isinstance(parent, MutableSequence) and _is_index(last):
            try:
                parent[int(last)] = value
            except IndexError:
                raise KeyError(self._join(parts)) from None
        else:
            raise TypeError(f"cannot set {self._join(parts)!r} in a {type(parent).__name__}")

    def __delitem__(self, key: Any) -> None:
        parts = self._path(key)
        if parts is None:
            dict.__delitem__(self, key)
            return
        parent, last = self._parent(parts), parts[-1]
        if _step(parent, last) is _MISSING:
            raise KeyError(self._join(parts))
        if isinstance(parent, MutableMapping):
            key = _mapping_key(parent, last)
            if isinstance(parent, dict):
                dict.__delitem__(parent, key)
            else:
                del parent[key]
        elif isinstance(parent, MutableSequence):
            del parent[int(last)]
        else:
            raise TypeError(f"cannot delete {self._join(parts)!r} from a {type(parent).__name__}")

    def __contains__(self, key: object) -> bool:
        try:
            self[key]
        except KeyError:
            return False
        return True

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def copy(self) -> KeyMapper:
        return KeyMapper(self, delimiter=self.delimiter)

    def __reduce__(self):
        return (KeyMapper, (dict(self),), {"delimiter": self.delimiter})

    def __setstate__(self, state: dict) -> None:
        self.delimiter = state["delimiter"]

    def __repr__(self) -> str:
        if self.delimiter == ".":
            return f"KeyMapper({dict.__repr__(self)})"
        return f"KeyMapper({dict.__repr__(self)}, delimiter={self.delimiter!r})"

    def pprint(self, obj: Any = _MISSING) -> str:
        """Return obj, or this mapping, as indented JSON."""
        return json.dumps(self if obj is _MISSING else obj, indent=4, ensure_ascii=False)


def _is_index(part: Any) -> bool:
    return isinstance(part, int) or (isinstance(part, str) and _INDEX.fullmatch(part) is not None)


# Within a path each part is a literal key, so a dict, including a nested
# KeyMapper, is read and written with dict's own methods, which never split a
# part at the delimiter again.


def _has(mapping: Mapping, key: Any) -> bool:
    return dict.__contains__(mapping, key) if isinstance(mapping, dict) else key in mapping


def _set(mapping: MutableMapping, key: Any, value: Any) -> None:
    if isinstance(mapping, dict):
        dict.__setitem__(mapping, key, value)
    else:
        mapping[key] = value


def _mapping_key(mapping: Mapping, part: Any) -> Any:
    """Return the key a part names in mapping: as written, else as an integer."""
    if not _has(mapping, part) and isinstance(part, str) and _is_index(part) and _has(mapping, int(part)):
        return int(part)
    return part


def _step(node: Any, part: Any) -> Any:
    """Return node's child named by part, or _MISSING."""
    if isinstance(node, Mapping):
        key = _mapping_key(node, part)
        if not _has(node, key):
            return _MISSING
        return dict.__getitem__(node, key) if isinstance(node, dict) else node[key]
    if isinstance(node, Sequence) and not isinstance(node, (str, bytes, bytearray)) and _is_index(part):
        try:
            return node[int(part)]
        except IndexError:
            return _MISSING
    return _MISSING
