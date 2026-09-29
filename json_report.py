import json
from crawl import PageData


def write_json_report(page_data: dict[str, PageData], filename: str = "report.json") -> None:
    pages = sorted(page_data.values(), key=lambda page: page["url"])
    file = open(filename, 'w', encoding="utf-8")
    json.dump(pages, file, indent=2)
    print(f"wrote report to {filename}")
