import copy
import json
import pickle

import pytest

from keymapper import KeyMapper


def test_paths_read_like_brackets():
    km = KeyMapper({"servers": [{"ip": "10.0.0.1"}, {"ip": "10.0.0.2"}]})
    assert km["servers.1.ip"] == km["servers"][1]["ip"] == "10.0.0.2"
    assert km["servers", 0, "ip"] == "10.0.0.1"
    assert km["servers.-1.ip"] == "10.0.0.2"


def test_plain_dict_behavior_is_unchanged():
    km = KeyMapper({"a": 1}, b=2)
    assert isinstance(km, dict) and dict(km) == {"a": 1, "b": 2}
    assert json.loads(json.dumps(km)) == {"a": 1, "b": 2}
    with pytest.raises(KeyError):
        km["missing"]
    assert km.get("missing", "default") == "default"
    km[1] = "int keys work"
    assert km[1] == "int keys work"


def test_settings_never_become_data():
    km = KeyMapper({"a": {"b": 1}}, delimiter=",")
    assert dict(km) == {"a": {"b": 1}}
    assert km["a,b"] == 1


def test_missing_paths_raise_key_error_naming_them():
    km = KeyMapper({"a": {"b": [1]}})
    with pytest.raises(KeyError, match="a.c"):
        km["a.c.d"]
    with pytest.raises(KeyError, match="a.b.5"):
        km["a.b.5"]
    assert "a.b.0" in km and "a.b.5" not in km and "x.y" not in km
    assert km.get("a.c", "default") == "default"


def test_falsy_values_are_found():
    km = KeyMapper({"x": [0, ""], "y": {"z": None}})
    assert km["x.0"] == 0 and km["x.1"] == "" and km["y.z"] is None


def test_digit_keys_match_strings_then_integers():
    km = KeyMapper({"a": {"0": "string zero", 1: "int one"}})
    assert km["a.0"] == "string zero"
    assert km["a.1"] == "int one"


def test_keys_containing_the_delimiter_still_work():
    km = KeyMapper({"a.b": "literal", "a": {"b": "nested"}})
    assert km["a.b"] == "literal"
    assert km["a", "b"] == "nested"
    km2 = KeyMapper({"x": {"a.b": 1}})
    assert km2["x", "a.b"] == 1


def test_updates_are_visible_to_paths():
    km = KeyMapper()
    km.update({"a": {"b": 1}})
    assert km["a.b"] == 1
    km.setdefault("c", []).append({"d": 2})
    assert km["c.0.d"] == 2


def test_writing_a_path_creates_mappings():
    km = KeyMapper()
    km["user.name"] = "Ada"
    km["servers"] = [{}]
    km["servers.0.ip"] = "10.0.0.1"
    assert dict(km) == {"user": {"name": "Ada"}, "servers": [{"ip": "10.0.0.1"}]}
    with pytest.raises(KeyError):
        km["servers.3.ip"] = "out of range"
    with pytest.raises(TypeError):
        KeyMapper({"t": (1, 2)})["t.0"] = 3


def test_deleting_a_path():
    km = KeyMapper({"a": {"b": 1, "c": [1, 2]}})
    del km["a.b"]
    del km["a.c.0"]
    assert dict(km) == {"a": {"c": [2]}}
    with pytest.raises(KeyError):
        del km["a.b"]


def test_sets_are_not_indexed():
    km = KeyMapper({"s": {"A", "B"}})
    with pytest.raises(KeyError):
        km["s.0"]


def test_no_attribute_magic():
    km = KeyMapper({"a": 1})
    assert not hasattr(km, "a")
    assert not hasattr(km, "anything")
    with pytest.raises(AttributeError):
        km.anything = 1


def test_copy_and_pickle_keep_the_delimiter():
    km = KeyMapper({"a": {"b": 1}}, delimiter="/")
    for other in (km.copy(), copy.copy(km), copy.deepcopy(km), pickle.loads(pickle.dumps(km))):
        assert isinstance(other, KeyMapper)
        assert other["a/b"] == 1 and other.delimiter == "/"
    assert repr(km) == "KeyMapper({'a': {'b': 1}}, delimiter='/')"


def test_bad_delimiter():
    with pytest.raises(ValueError):
        KeyMapper(delimiter="")
