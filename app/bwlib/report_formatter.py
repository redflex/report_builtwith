"""Format output for reporting."""
import base64
import csv
import cStringIO
import datetime
from string import Template


class ReportFormatter(object):
    """Initialize with the desired output format.

    Args:
        report_format(str): MD for markdown, CSV for comma-separated values.

    Attributes:
        report_format(str): Output format, taken from init arg.
    """

    def __init__(self, report_format):
        self.report_format = report_format
        return

    def format_report(self, report_structure):
        """Wrap reporting action."""
        if self.report_format == "MD":
            formatter = self.md_wrapper
        elif self.report_format == "CSV":
            formatter = self.csv_wrapper
        formatted = formatter(report_structure)
        encoded = base64.b64encode(formatted)
        return encoded

    @classmethod
    def md_wrapper(cls, result_structure):
        """Wrap all markdown formatting."""
        retval = ""
        main = cls.md_format_main(
                   cls.enrich_dates(
                       cls.collapse_lists(result_structure)))
        meta = cls.md_format_meta(
                   cls.enrich_dates(
                       cls.collapse_lists(result_structure["Meta"])))
        paths = "\n---\n".join([cls.md_format_path(
                                    cls.collapse_lists(
                                        cls.enrich_dates(x)))
                                for x in
                                result_structure["Result"]["Paths"]])
        retval += "\n\n".join([main, meta, paths])
        retval += "\n"
        return retval.encode('utf-8', errors='replace')

    @classmethod
    def csv_wrapper(cls, result):
        """Return a string containing a CSV."""
        rows = cls.build_rows(result)
        out = cStringIO.StringIO()
        cols = rows[0].keys()
        rows = cls.encode_rows(rows)
        csv_obj = csv.DictWriter(out, fieldnames=cols)
        csv_obj.writeheader()
        csv_obj.writerows(rows)
        return out.getvalue()

    @classmethod
    def encode_rows(cls, rows):
        """Make sure each value is UTF-8."""
        out = []
        keys = rows[0].keys()
        for row in rows:
            row_out = {}
            for key in keys:
                row_out[key] = row[key].encode('utf-8')
            out.append(row_out.copy())
        return out

    @classmethod
    def build_rows(cls, result):
        """Build rows for CSV output."""
        rows = []
        meta = {"Lookup": result["Lookup"],
                "City": result["Meta"]["City"],
                "CompanyName": result["Meta"]["CompanyName"],
                "State": result["Meta"]["State"],
                "Country": result["Meta"]["Country"],
                "Postcode": result["Meta"]["Postcode"],
                "Telephones": " | ".join(result["Meta"]["Telephones"]),
                "Social": " | ".join(result["Meta"]["Social"]),
                "Emails": " | ".join(result["Meta"]["Emails"])
                }
        for path in result["Result"]["Paths"]:
            for technology in path["Technologies"]:
                tech = meta.copy()
                tech["Domain"] = path["Domain"]
                tech["Url"] = path["Url"]
                tech["IsPremium"] = technology["IsPremium"]
                tech["TechName"] = technology["Name"]
                tech["FirstDetected"] = cls.epoch_to_iso(
                    technology["FirstDetected"])
                tech["LastDetected"] = cls.epoch_to_iso(
                    technology["LastDetected"])
                tech["TechLink"] = technology["Link"]
                tech["TechTag"] = technology["Tag"]
                if technology["Categories"] is None:
                    tech["TechCategories"] = ""
                else:
                    tech["TechCategories"] = " | ".join(technology["Categories"])  # NOQA
                tech["TechDescription"] = technology["Description"]
                rows.append(tech.copy())
        return rows

    @classmethod
    def enrich_dates(cls, results):
        """Substitute epoch dates for ISO ones in specific fields."""
        for sub in ["LastIndexed", "FirstIndexed",
                    "LastDetected", "FirstDetected"]:
            if sub in results:
                results[sub] = cls.epoch_to_iso(results[sub])
        return results

    @classmethod
    def collapse_lists(cls, results):
        """Collapse fields we know are lists for clean markdown."""
        for sub in ["Emails", "Social", "Telephones"]:
            if sub in results:
                results[sub] = "  |  ".join(results[sub])
        return results

    @classmethod
    def md_format_main(cls, result_structure):
        """Format top-level info in builtwith report."""
        tmpl = {"Lookup": "# Lookup: $Lookup",
                "FirstIndexed": "First indexed: $FirstIndexed",
                "LastIndexed": "Last indexed: $LastIndexed"}
        fields = ["Lookup", "FirstIndexed", "LastIndexed"]
        return "\n\n".join([Template(tmpl[x]).safe_substitute(result_structure)
                           for x in fields])

    @classmethod
    def md_format_meta(cls, meta):
        """Format top-level info in builtwith report."""
        tmpl = {"CompanyName": "Company: $CompanyName",
                "City": "City: $City",
                "State": "State: $State",
                "Postcode": "Postcode: $Postcode",
                "Country": "Country: $Country",
                "Vertical": "Vertical: $Vertical",
                "Telephones": "Tel:\n  $Telephones",
                "Emails": "Emails:\n  $Emails",
                "Social": "Social:\n  $Social"}
        fields = ["CompanyName", "City", "State", "Postcode", "Country",
                  "Vertical", "Telephones", "Emails", "Social"]
        return "\n\n".join([Template(tmpl[x]).safe_substitute(meta)
                           for x in fields])

    @classmethod
    def md_format_path(cls, path):
        """Return path formatted in markdown.

        Expected input example:
            {"Domain": "builtwith.com",
             "Url": "",
             "LastIndexed": 1525302000000,
             "Technologies": []
             "SubDomain": "",
             "FirstIndexed": 1294059600000
             }

        Args:
            path(dict):Path subsection of builtwith report.

        """
        tmpl = {"Domain": "## Domain: $Domain",
                "Url": "### URL: $Url",
                "LastIndexed": "Last indexed: $LastIndexed",
                "FirstIndexed": "First indexed: $FirstIndexed",
                "Subdomain": "### Subdomain: $Subdomain"}
        tech = "Technologies:\n"
        tech += "\n---\n".join([cls.md_format_technology(cls.enrich_dates(x))
                                for x in path["Technologies"]])
        fields = ["Domain", "Subdomain", "Url", "FirstIndexed", "LastIndexed"]
        body = "\n\n".join([Template(tmpl[x]).safe_substitute(path)
                            for x in fields
                            if x in tech])
        return "\n\n".join([body, tech])

    @classmethod
    def md_format_technology(cls, tech):
        """Return technology formatted in markdown.

        Expected input example:
            {"IsPremium": "yes",
             "Name": "Amazon CloudFront",
             "FirstDetected": 1386284400000,
             "Tag": "cdns",
             "Link": "http://aws.amazon.com/cloudfront/",
             "LastDetected": 1525129200000,
             "Categories": [
                 "Edge Delivery Network"
              ],
             "Description": "Amazon CloudFront delivers your..."
             }

        Args:
            tech(dict): Expected keys: "IsPremium" (str), "Name" (str),
                "FirstDetected" (int, unix date), "Tag" (str), "Link" (str),
                "LastDetected" (int, unix date), "Categories" (list),
                "Description" (str).
        """
        tmpl = {"Name": "####  Name: $Name",
                "Premium": "    Premium: $IsPremium",
                "FirstDetected": "    First detected: $FirstDetected",
                "LastDetected": "    Last detected: $LastDetected",
                "Description": "    Description: $Description"}
        if "Categories" in tech and tech["Categories"] is not None:
            cats = "\n\n    Categories: %s" % ", ".join(tech["Categories"])
        else:
            cats = ""
        fields = ["Name", "Premium", "FirstDetected", "LastDetected",
                  "Description"]
        body = "\n\n".join([Template(tmpl[x]).safe_substitute(tech)
                           for x in fields])
        body += cats
        return body

    @classmethod
    def epoch_to_iso(cls, epoch_date):
        """Return ISO 8601 date for epoch_date."""
        e_date = float(epoch_date/1000)
        stamp = datetime.datetime.utcfromtimestamp(e_date).isoformat()
        return stamp
