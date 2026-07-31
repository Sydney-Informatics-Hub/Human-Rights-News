from preprocess_entity_maps import load_entities_csv, dedupe_the, clean_map
import csv


def load_expected_map(csvfile):
    mapping = {}
    with open(csvfile, "r") as cfh:
        reader = csv.reader(cfh, dialect="excel")
        for row in reader:
            eid = row[1]
            mapping[eid] = {"eid": row[1], "ceid": row[3], "clean_name": row[2]}
    return mapping


def test_dedupe(test_files):
    raw_csv = test_files["deduplicate"]["raw"]
    max_id, prefix, ents = load_entities_csv(raw_csv)
    assert max_id == test_files["deduplicate"]["max_id"]
    assert prefix == test_files["deduplicate"]["prefix"]
    dd_entities = dedupe_the(ents)
    cleaned_map = {}
    for row in clean_map(max_id, prefix, dd_entities):
        eid = row[1]
        cleaned_map[eid] = {"eid": eid, "ceid": row[3], "clean_name": row[2]}
    expected_map = load_expected_map(test_files["deduplicate"]["deduped"])
    assert cleaned_map == expected_map
