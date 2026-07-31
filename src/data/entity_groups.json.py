# data loader which builds preset lists of entities as JSON

import json
from collections import defaultdict

from config import ENTITIES_CSV_FILES
from entities import load_mapped_entities, EntityGroups


def match_entity_names(eg, entity_type):
    ecsv = ENTITIES_CSV_FILES[entity_type]
    entity_map = load_mapped_entities(ecsv)
    groupsets = defaultdict(set)
    for eid, emap in entity_map.items():
        g = eg.group(entity_type, emap["clean_name"])
        if g:
            groupsets[g].add(emap["ceid"])
            print(g + "," + emap["ceid"])
    groups = {group: list(groupsets[group]) for group in groupsets}
    return groups


def main():
    eg = EntityGroups()
    entity_groups = match_entity_names(eg, "org")
    print(json.dumps(entity_groups, indent=2))


if __name__ == "__main__":
    main()
