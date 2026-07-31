import csv
import json
import pyarrow.parquet as pq
from pathlib import Path
from collections import defaultdict
import sys

from config import BATCH_DIRS


def load_articles(mfile):
    """Load the article metadata file and return a generator of dicts"""
    with open(mfile, "r") as cfh:
        reader = csv.reader(cfh, dialect="excel")
        for row in reader:
            yield {
                "aid": row[0],
                "title": row[1],
                "date": row[2],
                "publication": row[6],
                "include": True,
            }


def summarise_batch(d):
    pqf = Path(d) / "articles_nre_export.parquet"
    nre_pq = pq.read_table(pqf)
    articles = {}
    for row in load_articles(Path(d) / "article_metadata.csv"):
        articles[row["aid"]] = row
    counts = defaultdict(int)
    for nre_article in nre_pq.to_pylist():
        aid = nre_article["aid"]
        if aid in articles:
            md = articles[aid]
            date = md["date"]
            year = date[:4]
            counts[year] += 1
        else:
            print(f"Article {aid} not in article_metadata.csv", file=sys.stderr)
    return counts


if __name__ == "__main__":
    counts = []
    for d in BATCH_DIRS:
        for date, total in summarise_batch(d).items():
            counts.append({"date": date, "count": total, "batch": d})

    counts.sort(key=lambda d: d["date"])

    print(json.dumps(counts, indent=2))
