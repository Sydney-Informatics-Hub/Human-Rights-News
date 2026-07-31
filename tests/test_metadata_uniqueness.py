import csv
import re

from config import RAW_METADATA_FILE


def test_unique_ids():
    articles = {}
    id_re = re.compile(r"^\d+$")
    with open(RAW_METADATA_FILE, "r") as cfh:
        reader = csv.reader(cfh)
        for row in reader:
            aid = row[0]
            if id_re.search(aid):
                assert aid not in articles
                articles[aid] = row
