import csv
from tqdm import tqdm

from config import RAW_METADATA_FILE, CONCAT_METADATA_FILE


def unique_articles(infile):
    """Load the article metadata file and return a generator of dicts."""
    seen = set()
    with open(infile, "r") as cfh:
        reader = csv.reader(cfh, dialect="excel")
        for row in tqdm(reader):
            aid = row[0]
            if aid not in seen:
                seen.add(aid)
                yield row


with open(RAW_METADATA_FILE, "w") as cfh:
    writer = csv.writer(cfh, dialect="excel")
    for row in unique_articles(CONCAT_METADATA_FILE):
        writer.writerow(row)
