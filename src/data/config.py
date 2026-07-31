METADATA_COLS = {
    "aid": 0,
    "title": 1,
    "date": 2,
    "type": 3,
    "authors": 4,
    "publicationID": 5,
    "publication": 6,
}

BASE_DIR = "./src/data"

# each of these is a directory with the following:
#
# - article_metadata.csv
# - article_nre_export.parquet
# - geo_entities.json
# - org_entities.json
#

BATCH_DIRS = [f"{BASE_DIR}/guardian", f"{BASE_DIR}/nyt1", f"{BASE_DIR}/nyt2"]

MERGED_DIR = f"{BASE_DIR}/merged"

CONCAT_METADATA_FILE = f"{MERGED_DIR}/concat_article_metadata.csv"

RAW_METADATA_FILE = f"{MERGED_DIR}/raw_article_metadata.csv"
REMOVED_FILE = f"{MERGED_DIR}/removed.csv"

METADATA_FILE = f"{MERGED_DIR}/article_metadata.csv"
NRE_FILE = f"{MERGED_DIR}/articles_nre_export.parquet"

DUPLICATE_THRESHOLD = 80

SKIP_TITLES = ["Display Ad", "Classified Ad"]

DATE_CUTOFF = "1900-01-01"

# pubids not in this dict will be skipped by the data loaders

PUBLICATIONS = {
    "45545": "New York Times",
    "35249": "The Guardian",
    "35250": "The Guardian",
    "35251": "The Guardian",
    "44261": "The Guardian",
    "54548": "The Guardian",
    #    "47146": "The Observer",
    #    "55412": "The Observer",
    #    "6350255": "The Observer",
}

# original json from TDM studio

ENTITIES_JSON_FILES = {
    "geo": f"{MERGED_DIR}/geo_entities.json",
    "org": f"{MERGED_DIR}/org_entities.json",
}


ENTITIES_CSV_FILES = {
    "geo": f"{MERGED_DIR}/geo_entities.csv",
    "org": f"{MERGED_DIR}/org_entities.csv",
}

COUNTS_DIR = f"{MERGED_DIR}/article_counts"
