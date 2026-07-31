import pyarrow as pa
import pyarrow.parquet as pq
import json
import spacy
import csv
from tqdm import tqdm

nlp = spacy.load("en_core_web_sm")

# size comparison between JSON and parquet for NER


# doing NER on article titles just to have something to play with

from config import SPREADSHEET_COLS, SPREADSHEET_FILE

COERCE_STR = [ "Title", "Authors" ]
DATE = [ "Date" ]

dumb_json = {}

entities = {}
e_id = 0

rows = []

print("Loading CSV")
with open(SPREADSHEET_FILE, "r") as cfh:
    creader = csv.reader(cfh, dialect="excel")
    rows = list(creader)

print("Doing NER")
for row in tqdm(rows):
    if row[0] != "GOID":
        doc_id = int(row[0])
        doc = nlp(row[SPREADSHEET_COLS["Title"]])
        dumb_json[doc_id] = []
        for e_name in [ e.text for e in doc.ents ]:
            if e_name not in entities:
                entities[e_name] = { "eid": e_id, "count": 0 }
                e_id += 1
            entities[e_name]["count"] += 1
            dumb_json[doc_id].append(entities[e_name]["eid"])

print("writing to dumb2.json")
with open("dumb2.json", "w") as jfh:
    json.dump(dumb_json, jfh)

print("writing entities.json")
with open("entities.json", "w") as jfh:
    json.dump(entities, jfh)

print("rearranging as parquet")

pdict = { "doc_id":[], "entities": [] }

for doc_id, ents in dumb_json.items():
    pdict["doc_id"].append(doc_id)
    pdict["entities"].append(ents)

print("writing to test2.parquet")
try:
    arrow = pa.table(pdict)
    pq.write_table(arrow, 'test2.parquet')
except Exception as e:
    print(f"PyArrow error: {e}")
    print(data_types)
