import os
import sys
from collections import defaultdict
import pyarrow as pa
import pyarrow.parquet as pq

from config import NRE_FILE, ENTITIES_CSV_FILES
from entities import (
    GROUP_LABELS,
    GROUP_TYPES,
    load_mapped_entities,
    make_clean_map,
    EntityGroups,
)


def clean_eids(entity_map, etype, raw_ids):
    """For a set of raw article ids, return a deduplicated list of qualified
    clean ids"""
    qeids = [f"{etype}_{eid}" for eid in raw_ids]
    idset = set([entity_map[eid]["ceid"] for eid in qeids])
    return list(idset)


def write_entities(articles):
    pdict = {"eid": [], "type": [], "name": [], "freq": []}
    group_freqs = defaultdict(int)
    grouper = EntityGroups()
    for etype, ecsv in ENTITIES_CSV_FILES.items():
        entity_map = load_mapped_entities(ecsv)
        clean_map = make_clean_map(entity_map)
        freqs = defaultdict(int)
        for article in articles.to_pylist():
            for eid in clean_eids(entity_map, etype, article[etype]):
                freqs[eid] += 1
                gid = grouper.group(etype, clean_map[eid])
                if gid:
                    group_freqs[gid] += 1

        clean_entities = set()
        for eid, emap in entity_map.items():
            ceid = emap["ceid"]
            if ceid not in clean_entities:
                pdict["eid"].append(ceid)
                pdict["type"].append(etype)
                pdict["name"].append(emap["clean_name"])
                pdict["freq"].append(freqs[ceid])
                clean_entities.add(ceid)

    for group, name in GROUP_LABELS.items():
        pdict["eid"].append(group)
        pdict["type"].append(GROUP_TYPES[group])
        pdict["name"].append(name)
        pdict["freq"].append(group_freqs[group])

    arrow = pa.table(pdict)
    with os.fdopen(sys.stdout.fileno(), "wb") as stdout:
        pq.write_table(arrow, stdout)
        stdout.flush()


def main():
    articles = pq.read_table(NRE_FILE)
    write_entities(articles)


if __name__ == "__main__":
    main()
