# Precompute article types, publications and dates

import csv
import json
from config import METADATA_COLS, METADATA_FILE, DATE_CUTOFF, PUBLICATIONS
import datetime

article_types = {}
publications = {}

date_min = datetime.datetime.fromisoformat("2021-01-01")
date_max = datetime.datetime.fromisoformat("1800-01-01")

date_ranges = {}
pub_names = []

for pubid in PUBLICATIONS:
    pub = PUBLICATIONS[pubid]
    if pub not in date_ranges:
        date_ranges[pub] = {"min": date_min, "max": date_max}
        pub_names.append(pub)

earliest = datetime.datetime.fromisoformat(DATE_CUTOFF)

with open(METADATA_FILE, "r") as cfh:
    creader = csv.reader(cfh, dialect="excel")
    for row in creader:
        if row[0] != "GOID":
            article_date = datetime.datetime.fromisoformat(row[METADATA_COLS["date"]])
            if article_date >= earliest:
                if "type" in METADATA_COLS:
                    article_type = row[METADATA_COLS["type"]]
                    if article_type not in article_types:
                        article_types[article_type] = 1
                    else:
                        article_types[article_type] += 1
                pubid = row[METADATA_COLS["publicationID"]]
                if pubid in PUBLICATIONS:
                    pub = PUBLICATIONS[pubid]
                    if pub not in publications:
                        publications[pub] = 1
                    else:
                        publications[pub] += 1
                    if date_ranges[pub]["min"] > article_date:
                        date_ranges[pub]["min"] = article_date
                    if date_ranges[pub]["max"] < article_date:
                        date_ranges[pub]["max"] = article_date

# get the min and max dates for which we have data for all publications

date_min = max([date_ranges[p]["min"] for p in pub_names])
date_max = min([date_ranges[p]["max"] for p in pub_names])


types_json = [{"type": t, "count": c} for t, c in article_types.items()]
types_json.sort(key=lambda x: x["count"], reverse=True)

pubs_json = [{"name": t, "count": c} for t, c in publications.items()]
pubs_json.sort(key=lambda x: x["count"], reverse=True)


print(
    json.dumps(
        {
            "types": types_json,
            "publications": pubs_json,
            "dates": [date_min.year, date_max.year],
        }
    )
)
