import json

with open("data/catalog.json", encoding="utf8") as f:
    catalog = json.load(f, strict=False)


def get_by_name(name):
    for item in catalog:
        if item["name"].lower() == name.lower():
            return item
    return None


def get_by_url(url):
    for item in catalog:
        if item.get("url", "").lower().rstrip("/") == url.lower().rstrip("/"):
            return item
    return None