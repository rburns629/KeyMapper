# KeyMapper

A `dict` whose keys can also be paths into nested data. Read, write, and
delete deep values with one key, such as `km["servers.0.ip"]`, instead of
`km["servers"][0]["ip"]`.

- It is a real `dict`: `isinstance(km, dict)`, `json.dumps(km)`, and every dict
  method work as usual.
- A path walks mappings by key and lists or tuples by index, negative indexes
  included.
- A missing path raises `KeyError` naming it, as a dict does; `get` returns a
  default instead.
- Writing to a path creates the mappings it needs.
- A key that exists exactly as written always wins, so keys that contain the
  delimiter still work.

## Installation

    pip install keymapper

Python 3.11 or newer.

## Examples

**Paths:**

```python
from keymapper import KeyMapper

km = KeyMapper({"servers": [{"ip": "10.0.0.1"}, {"ip": "10.0.0.2"}]})

km["servers.1.ip"]       # '10.0.0.2'
km["servers.-1.ip"]      # '10.0.0.2', the last server
km["servers", 0, "ip"]   # '10.0.0.1', a tuple path
km.get("servers.5.ip")   # None
"servers.0.ip" in km     # True
```

**Writing and deleting:**

```python
km = KeyMapper()
km["user.name"] = "Ada"          # creates km["user"]
km["user.email"] = "ada@example.com"
del km["user.email"]
print(km)                        # KeyMapper({'user': {'name': 'Ada'}})
```

**Another delimiter, or keys that contain one:**

```python
km = KeyMapper({"a": {"b": 1}}, delimiter="/")
km["a/b"]                        # 1

km = KeyMapper({"version.major": 2, "build": {"tag.name": "v2"}})
km["version.major"]              # 2, the key exists as written
km["build", "tag.name"]          # 'v2', a tuple keeps each part whole
```

**Keys that look like numbers:** a part such as `"0"` matches the key `"0"`
first, then the key `0`, so both kinds of dictionary work. Sets have no order,
so a path cannot index into one.

## Upgrading from 1.x

Version 2.0 makes KeyMapper behave like a dict, which changes four things:

- A missing key raises `KeyError`; use `get` for a default.
- Attribute access (`km.name`) is gone; use `km["name"]`.
- The `schema` option is gone; validate data with a library made for it, such
  as pydantic.
- Writing a path creates missing mappings instead of raising `KeyError`.

See [CHANGES.md](CHANGES.md).

## Development

    python -m venv .venv && .venv/bin/pip install -e . pytest
    .venv/bin/python -m pytest
