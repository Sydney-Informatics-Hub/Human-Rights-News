# data loader which builds a JSON with article counts by publication
# and year to normalise the visualisations

import csv
import datetime
import json
from pathlib import Path
from config import (
    COUNTS_DIR,
    METADATA_COLS,
    METADATA_FILE,
    DATE_CUTOFF,
    PUBLICATIONS,
)

from collections import defaultdict
import re

counts = {"total": defaultdict(lambda: defaultdict(int))}

# load the counts of all articles from the CSV files

for csvfile in Path(COUNTS_DIR).glob("*.csv"):
    with open(csvfile, "r") as cfh:
        creader = csv.reader(cfh, dialect="excel")
        for row in creader:
            if re.match(r"\d\d\d\d", row[1]):
                pub = row[0]
                year = row[1]
                article_type = row[2]
                count = int(row[3])
                if pub not in counts:
                    counts[pub] = defaultdict(lambda: defaultdict(int))
                counts[pub][year]["all"] += count
                counts["total"][year]["all"] += count

# load the metadata file of articles mentioning "human rights" and add those
# subtotals

earliest = datetime.datetime.fromisoformat(DATE_CUTOFF)

with open(METADATA_FILE, "r") as cfh:
    creader = csv.reader(cfh, dialect="excel")
    for row in creader:
        if row[0] != "GOID":
            aid = row[0]
            raw_date = row[METADATA_COLS["date"]]
            article_date = datetime.datetime.fromisoformat(raw_date)
            if article_date >= earliest:
                pubid = row[METADATA_COLS["publicationID"]]
                if pubid in PUBLICATIONS:
                    pubname = PUBLICATIONS[pubid]
                    year = str(article_date.year)
                    counts[pubname][year]["human_rights"] += 1
                    counts["total"][year]["human_rights"] += 1

print(json.dumps(counts, indent=2))
