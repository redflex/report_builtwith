import bwlib


def main():
    # Get config
    config = bwlib.ConfigHelper()
    # Get document
    document = bwlib.Document()
    # Format document
    formatter = bwlib.ReportFormatter(config.output_format)
    result = formatter.format_report(document.scan)
    # print document
    print(result)

if __name__ == "__main__":
    main()
