import imp
import os
import pytest
modulename = 'bwlib'
modulepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
file, pathname, description = imp.find_module(modulename, [modulepath])
bwlib = imp.load_module(modulename, file, pathname, description)

herepath = os.path.dirname(os.path.abspath(__file__))
fixture_path = os.path.join(herepath, "../fixture")


class TestConfigHelper:
    def test_instantiate_all_vars_good(self, monkeypatch):
        monkeypatch.setenv("OUTPUT_FORMAT", "CSV")
        assert bwlib.ConfigHelper()

    def test_instantiate_bad_format(self, monkeypatch):
        monkeypatch.setenv("OUTPUT_FORMAT", "BADFMT")
        with pytest.raises(ValueError):
            bwlib.ConfigHelper()

    def test_instantiate_no_format(self):
        with pytest.raises(ValueError):
            bwlib.ConfigHelper()
