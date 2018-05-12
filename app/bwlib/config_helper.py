"""Manage configs for bwlib."""
import os


class ConfigHelper(object):
    allowed_output_formats = ["MD", "CSV"]

    def __init__(self):
        """Instantiate config helper.

        Attributes:
            output_format(str): Format for report output.  Supports ``CSV``
                and ``MD``.
        """
        self.output_format = os.getenv("OUTPUT_FORMAT")
        self.sanity_check()
        return

    def sanity_check(self):
        """Make sure that all config items are present and sane."""
        err_out = ""
        required = {"OUTPUT_FORMAT": self.output_format}
        for varname, val in required.items():
            if val is None:
                err_out += "Missing environment variable: %s\n" % varname
        if self.output_format not in self.allowed_output_formats:
            err_out += "Invalid output format: %s\n" % self.output_format
            err_out += ("Allowed output formats: %s\n" %
                        ", ".join(self.allowed_output_formats))
        if err_out != "":
            print(err_out)
            raise ValueError(err_out)
        return
