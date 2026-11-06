import json
from pathlib import Path

from keymapper import KeyMapper


def test_paths_into_a_json_document():
    data = json.loads((Path(__file__).parent / "etc" / "test_json.json").read_text())
    km = KeyMapper(data)
    assert km["web-app.servlet.0.init-param"] == data["web-app"]["servlet"][0]["init-param"]
    assert km["web-app.servlet.0.init-param.maxUrlLength"] == data["web-app"]["servlet"][0]["init-param"]["maxUrlLength"]
    assert json.loads(km.pprint()) == data
