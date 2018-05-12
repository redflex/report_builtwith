"""Get and expand document from env."""
import base64
import json
import os


class Document(object):
    """Get doc from env var ``SCAN``, unpack, and set as ``Document.scan``."""
    def __init__(self):
        self.scan_raw = os.getenv("SCAN")
        self.scan = self.unpack_raw_scan(self.scan_raw)

    @classmethod
    def unpack_raw_scan(cls, scan_raw):
        """Return unpacked scan as a Python ``dict``."""
        return json.loads(base64.b64decode(scan_raw))
