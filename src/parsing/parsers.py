import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from storage.mongo import save_to_mongo


def parse_json_files():
    folder = Path("data/raw/api")
    json_files = list(folder.glob("*.json"))

    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        features = data.get("features", [])
        print(f"{file_path.name}: {len(features)} places")

        for feature in features:
            save_to_mongo(feature, "geoapify_json")

        if features:
            props = features[0].get("properties", {})
            print("First place name:", props.get("name", "No name"))


def parse_csv_file(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print("CSV rows:", len(rows))
    if rows:
        print("First CSV row:", rows[0])

    for row in rows:
        save_to_mongo(row, "sample_csv")


def parse_xml_file(path):
    tree = ET.parse(path)
    root = tree.getroot()

    print("XML root:", root.tag)

    for destination in root.findall("destination"):
        data = {
            "id": destination.findtext("id"),
            "name": destination.findtext("name"),
            "country": destination.findtext("country")
        }
        save_to_mongo(data, "sample_xml")

    first_destination = root.find("destination")
    if first_destination is not None:
        name = first_destination.find("name")
        if name is not None:
            print("First XML destination:", name.text)


if __name__ == "__main__":
    parse_json_files()
    parse_csv_file("data/raw/csv/sample.csv")
    parse_xml_file("data/raw/xml/sample.xml")