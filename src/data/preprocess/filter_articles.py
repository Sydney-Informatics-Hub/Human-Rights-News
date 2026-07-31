import csv
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
import re
from collections import defaultdict
from tqdm import tqdm
from fuzzywuzzy import fuzz

from config import (
    BATCH_DIRS,
    MERGED_DIR,
    METADATA_FILE,
    RAW_METADATA_FILE,
    REMOVED_FILE,
    SKIP_TITLES,
    DUPLICATE_THRESHOLD,
)


skip_pattern_re = {r: re.compile(r, re.IGNORECASE) for r in SKIP_TITLES}


def unwanted_article(article):
    """Return True if the article's title matches a pattern from SKIP_TITLES"""
    for label, pattern in skip_pattern_re.items():
        if pattern.search(article["title"]):
            return True
    return False


def load_articles(mfile):
    """Load the article metadata file and return a generator of dicts."""
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


def filter_articles(mfile):
    """Load the metadata file and return a list of dicts with the article
    data, a flag indicating inclusion and a reason for excluding"""
    articles = []
    by_date = defaultdict(list)
    by_aid = {}

    for article in load_articles(mfile):
        if unwanted_article(article):
            article["include"] = False
            article["reason"] = "Bad title"
            articles.append(article)
        else:
            articles.append(article)
            by_aid[article["aid"]] = article
            by_date[article["date"]].append(article["aid"])

    already_deduped = set()

    for article in tqdm(articles):
        if article["aid"] not in already_deduped:
            same_day = [by_aid[aid] for aid in by_date[article["date"]]]
            title = article["title"]
            matches = [
                (a["aid"], fuzz.ratio(title, a["title"]), a)
                for a in same_day
                if a["aid"] not in already_deduped
            ]
            threshold = [
                m
                for m in matches
                if m[1] > DUPLICATE_THRESHOLD and m[0] != article["aid"]
            ]
            if threshold:
                threshold.sort(key=lambda m: m[1], reverse=True)
                pubs = set()
                for match in threshold:
                    pubs.add(match[2]["publication"])
                publist = ",".join(pubs)
                row = [publist]
                for match in threshold:
                    row += [match[0], match[1], match[2]["title"]]
                    already_deduped.add(match[0])
                article["include"] = False
                article["reason"] = "Duplicate title: " + str(row)
    return articles


def write_removed(articles, filename):
    """Write a CSV of articles which have been filtered and the reasons why"""
    COLS = ["aid", "publication", "date", "title", "reason"]
    with open(filename, "w") as fh:
        writer = csv.writer(fh)
        for article in articles:
            if not article["include"]:
                writer.writerow([article[f] for f in COLS])


def write_filtered_metadata(articles_by_id, raw_metadata, filtered_metadata):
    """Go back to the raw metadata and filter it by article inclusion"""
    with open(raw_metadata, "r") as cfh:
        with open(filtered_metadata, "w") as wfh:
            reader = csv.reader(cfh, dialect="excel")
            writer = csv.writer(wfh)
            for row in reader:
                if articles_by_id[row[0]]["include"]:
                    writer.writerow(row)


if __name__ == "__main__":
    print("Merging NRE parquet files")

    batch_nre = [Path(d) / "articles_nre_export.parquet" for d in BATCH_DIRS]
    nre_pq = [pq.read_table(pqf) for pqf in batch_nre]
    merged = pa.concat_tables(nre_pq)

    # uncomment to skip filtering
    # pq.write_table(merged, Path(MERGED_DIR) / "articles_nre_export.parquet")

    print("Removing unwanted articles and duplicates")

    articles = filter_articles(RAW_METADATA_FILE)

    # build a list of booleans flagging which articles are to be included,
    # in the order defined by the ids in merged, and apply that to the
    # pyarrow using the filter() method

    by_id = {article["aid"]: article for article in articles}
    include = [by_id[aid]["include"] for aid in merged["aid"].to_pylist()]

    filtered = merged.filter(include)

    pq.write_table(filtered, Path(MERGED_DIR) / "articles_nre_export.parquet")

    INCLUDE_COLS = ["aid", "publication", "date", "title"]

    print(f"Writing removed articles to {REMOVED_FILE}")

    write_removed(articles, REMOVED_FILE)

    print(f"Writing filtered article metadata file to {METADATA_FILE}")

    write_filtered_metadata(by_id, RAW_METADATA_FILE, METADATA_FILE)
