# Generates the article-entities junction table, and also
# adds extra meta-entities for groups

import os
import sys
import pyarrow as pa
import pyarrow.parquet as pq

from config import NRE_FILE, ENTITIES_CSV_FILES
from entities import load_mapped_entities, EntityGroups


def write_junction(articles, entity_maps):
    """Junction table for articles to entities. This uses the entity map files
    from OpenRefine to map 'dirty' IDs to 'clean' IDs in the parquet."""
    grouper = EntityGroups()
    aes = {}
    for article in articles.to_pylist():
        aid = article["aid"]
        if aid not in articles:
            aes[aid] = {"geo": set(), "org": set()}
        for etype, emap in entity_maps.items():
            for eid in article[etype]:
                qeid = f"{etype}_{eid}"
                if qeid in emap:
                    ceid = emap[qeid]["ceid"]
                    aes[aid][etype].add(ceid)
                    cname = emap[qeid]["clean_name"]
                    g = grouper.group(etype, cname)
                    if g:
                        aes[aid][etype].add(g)
                else:
                    print(f"Could not find eid {qeid} in entity csv")
                    sys.exit(-1)

    pdict = {"aid": [], "eid": []}
    for aid, entities in aes.items():
        for etype in entities:
            for eid in entities[etype]:
                pdict["aid"].append(aid)
                pdict["eid"].append(eid)

    arrow = pa.table(pdict)
    with os.fdopen(sys.stdout.fileno(), "wb") as stdout:
        pq.write_table(arrow, stdout)
        stdout.flush()


if __name__ == "__main__":
    articles = pq.read_table(NRE_FILE)
    entity_maps = {}
    for etype in ENTITIES_CSV_FILES.keys():
        entity_maps[etype] = load_mapped_entities(ENTITIES_CSV_FILES[etype])
    write_junction(articles, entity_maps)
