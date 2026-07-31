import csv
import pyarrow.parquet as pq
from tqdm import tqdm

MISSING = "./src/data/missing.csv"

METADATA = {
    "nyt_historical": "./src/data/nyt_202507/nyt_historical/extended_hist.csv",
    "nyt": "./src/data/nyt_202507/nyt_main_metadata/extended_main.csv",
}

NRE_FILE = "./src/data/nyt2/articles_nre_export.parquet"


def load_articles(mfile):
    """Load the article metadata file and return a generator of dicts"""
    with open(mfile, "r") as cfh:
        reader = csv.reader(cfh, dialect="excel")
        for row in reader:
            if row[0] != "GOID":
                yield {
                    "aid": row[0],
                    "title": row[1],
                    "date": row[2],
                    "publication": row[6],
                }


if __name__ == "__main__":
    metadata = {}

    for db, mfile in METADATA.items():
        metadata[db] = {}
        for row in load_articles(mfile):
            aid = row["aid"]
            if row["publication"] == "New York Times  (1923-)":
                metadata[db][aid] = row

    missing = 0

    with open(MISSING, "w") as mfh:
        writer = csv.writer(mfh, dialect="excel")
        writer.writerow(["aid", "db", "date", "publication", "title"])
        nre_table = pq.read_table(NRE_FILE)
        nre_aids_list = nre_table.to_pydict()["aid"]
        nre_aids_dict = {aid: 1 for aid in nre_aids_list}
        for db in METADATA:
            for aid in tqdm(metadata[db]):
                m = metadata[db][aid]
                if aid not in nre_aids_dict:
                    title = m["title"]
                    date = m["date"]
                    publication = m["publication"]
                    writer.writerow([aid, db, date, publication, title])
                    missing += 1
    print(f"Wrote {missing} missing records to {MISSING}")
