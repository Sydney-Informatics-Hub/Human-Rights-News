# Python script to turn the metadata spreadsheet into a Parquet file

import csv
import pyarrow as pa
import pyarrow.parquet as pq
import datetime
import sys
import os

from config import (
    METADATA_COLS,
    METADATA_FILE,
    NRE_FILE,
    DATE_CUTOFF,
    PUBLICATIONS,
)

# Loads the metadata CSV file and joins it to the parquet file exported
# from TDM studio, leaving the NREs as we got them

DATE = ["Date"]

earliest = datetime.datetime.fromisoformat(DATE_CUTOFF)

data_dict = {}
data_types = {}

for field in METADATA_COLS.keys():
    data_dict[field] = []
    data_types[field] = set()

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
                    data_dict["aid"].append(aid)
                    data_dict["date"].append(article_date)
                    data_dict["publication"].append(pubname)
                    for field in METADATA_COLS.keys():
                        if field not in ["aid", "date", "publication"]:
                            v = row[METADATA_COLS[field]]
                            data_dict[field].append(v)
                            data_types[field].add(str(type(v)))

nre_table = pq.read_table(NRE_FILE)

try:
    table = pa.table(data_dict)
    with os.fdopen(sys.stdout.fileno(), "wb") as stdout:
        pq.write_table(table, stdout)
        stdout.flush()
except Exception as e:
    print(f"PyArrow error: {e}", file=sys.stderr)
    print(data_types, file=sys.stderr)
    sys.exit(-1)
