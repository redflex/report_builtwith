import base64
import imp
import json
import os

modulename = "bwlib"
modulepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
file, pathname, description = imp.find_module(modulename, [modulepath])
bwlib = imp.load_module(modulename, file, pathname, description)

herepath = os.path.dirname(os.path.abspath(__file__))
fixture_path = os.path.join(herepath, "../fixture")
json_file = os.path.join(fixture_path, "builtwith_output.json")

with open(json_file, 'r') as j_file:
    full_report = json.load(j_file)


class TestDocument:
    def instantiate_document(self, monkeypatch):
        target_report = full_report["Results"][0]
        monkeypatch.setenv("SCAN", base64.b64encode(json.dumps(target_report)))
        return bwlib.Document()

    def test_instantiate_document(self, monkeypatch):
        assert self.instantiate_document(monkeypatch)

    def test_document_is_dict(self, monkeypatch):
        doc = self.instantiate_document(monkeypatch)
        assert isinstance(doc.scan, dict)
