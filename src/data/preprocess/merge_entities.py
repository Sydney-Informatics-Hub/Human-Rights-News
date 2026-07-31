from pathlib import Path
import json
from tqdm import tqdm

from config import (
    BATCH_DIRS,
)

OUT_DIR = Path("./src/data/test_merge_entities")

# Merge the TYPE_entities.json files from multiple runs of NRE on
# TDM studio


def load_entities(ef):
    """Load JSON entity file"""
    with open(ef, "r") as fh:
        return json.load(fh)


def write_entities(ef, e):
    """Write JSON entity file"""
    with open(ef, "w") as fh:
        json.dump(e, fh)


def merge_entities(ef1, ef2):
    """Load two JSON files which map names to ids, check that the two are
    consistent, and return a single dict with all of the entities."""
    e1 = load_entities(ef1)
    e2 = load_entities(ef2)
    ids1 = {e1[name]: name for name in e1}
    for name, i2 in tqdm(e2.items()):
        if name in e1:
            if e1[name] != i2:
                raise ValueError(f"inconsistent ids for {name}: {e1[name]}, {i2}")
        else:
            if i2 in ids1:
                raise ValueError(f"id collision for {i2}: {ids1[i2]}, {name}")
            else:
                e1[name] = i2
    return e1


def merge_all_entities(entity_jsons, efn):
    """Takes a list of two or more JSON files with entities and tries to
    merge them one by one, writing the results to the file efn as it
    goes. Raises a ValueError if it finds inconsistencies
    or collisions"""

    entities = load_entities(entity_jsons[0])
    write_entities(efn, entities)
    for ejson in entity_jsons[1:]:
        entities = merge_entities(efn, ejson)
        write_entities(efn, entities)


if __name__ == "__main__":
    for enttype in ["geo", "org"]:
        print(f"Merging {enttype} entities")
        entity_file = f"{enttype}_entities.json"
        json_e = [Path(d) / entity_file for d in BATCH_DIRS]
        merged_file = OUT_DIR / entity_file
        sources = ", ".join([str(f) for f in json_e])
        print(f"Merging {sources} to {merged_file}")
        merge_all_entities(json_e, merged_file)
