import base64
import imp
import json
import os

modulename = 'bwlib'
modulepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
file, pathname, description = imp.find_module(modulename, [modulepath])
bwlib = imp.load_module(modulename, file, pathname, description)

herepath = os.path.dirname(os.path.abspath(__file__))
fixture_path = os.path.join(herepath, "../fixture")


class TestReportFormatter:
    def instantiate_report_formatter_md(self):
        return bwlib.ReportFormatter("MD")

    def instantiate_report_formatter_csv(self):
        return bwlib.ReportFormatter("CSV")

    def test_process_markdown(self):
        report_path = os.path.join(fixture_path, "builtwith_output.json")
        with open(report_path, "r") as report_obj:
            report_struct = json.load(report_obj)
        formatter = self.instantiate_report_formatter_md()
        report_formatted = formatter.format_report(report_struct["Results"][0])
        assert isinstance(report_formatted, basestring)

    def test_process_csv(self):
        report_path = os.path.join(fixture_path, "builtwith_output.json")
        with open(report_path, "r") as report_obj:
            report_struct = json.load(report_obj)
        formatter = self.instantiate_report_formatter_csv()
        report_formatted = formatter.format_report(report_struct["Results"][0])
        assert isinstance(report_formatted, basestring)
        assert len(base64.b64decode(report_formatted).split("\n")) == 218
