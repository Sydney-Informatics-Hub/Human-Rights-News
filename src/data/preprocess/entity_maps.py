# Builds a complete deduplication map from the CSV from OpenRefine, and
# does additional data cleaning like folding "blah" and "the blah" to the
# same ID.

# OpenRefine (input CSV):
#
# name,clean_name,eid
# united states,united states,geo_1
# unified stations,united states,geo_2
# the united states,the uniteed states,geo_3
# congoo,congo,geo_4

# This script (output CSV):
#
# name,eid,clean_name,clean_eid
# united states,geo_1,united states,geo_1
# unified stations,geo_2,united states,geo_1
# the united states,geo_3,united states,geo_1
# congoo,geo_4,congo,geo_5

# Note that some cleaned entities will not have ids: new ones are created
# following in sequence where this is required (for eg congo/geo_5 in the
# example above)

import logging
import csv
from pathlib import Path
from argparse import ArgumentParser

# loglevel is set in __main__

logger = logging.getLogger(__name__)


# input is the OpenRefine spreadsheet with:
# orig_name,clean_name,eid


def load_entities_csv(fn):
    """From a filename, load the OpenRefine CSV and return a dict of original
    names to objects with eid and clean_name, and the max id so the following
    code can add new ones
    """
    entities = {}
    max_id = 0
    prefix = None
    i = 0
    with open(fn, "r") as cfh:
        reader = csv.reader(cfh, dialect="excel")
        for row in reader:
            i += 1
            if row[2] != "eid":
                name = row[0]
                clean_name = row[1]
                if not clean_name:
                    clean_name = row[0]
                eid = row[2]
                if name in entities:
                    logger.warning(f"[{i}] Duplicate original name {name} in CSV")
                entities[name] = {"eid": eid, "clean_name": clean_name}
                n_id = int(eid[4:])
                if n_id > max_id:
                    max_id = n_id
                if not prefix:
                    prefix = eid[:3]
                else:
                    if not prefix == eid[:3]:
                        logger.error(
                            f"[{i}] mismatched prefix{eid[:]} (expected {prefix})"
                        )
    return n_id, prefix, entities


def dedupe_the(entities):
    """
    Deduplicate for eg "the united states" -> "united states"
    Only deduplicates if "united states" already exists
    """

    for name, mapping in entities.items():
        if name[:4] == "the ":
            if name[4:] in entities:
                eid = mapping["eid"]
                mapped = entities[name[4:]]
                c_name = mapped["clean_name"]
                c_eid = mapped["eid"]
                logger.debug(f"{name} {eid} -> {c_name} {c_eid}")
                entities[name] = {"eid": eid, "clean_name": c_name}
            else:
                logger.warning(f"the-name '{name}' with no the-less match")
    return entities


def clean_map(max_id, prefix, entities):
    """Generator which yields rows mapping original name/id to clean versions"""
    next_id = max_id + 1
    new_entities = {}
    for name, mapping in entities.items():
        clean_name = mapping["clean_name"]
        eid = mapping["eid"]
        if name == clean_name:
            yield [name, eid, name, eid]
        else:
            if clean_name in entities:
                clean = entities[clean_name]
                yield [name, eid, clean_name, clean["eid"]]
            else:
                if clean_name in new_entities:
                    clean = new_entities[clean_name]
                    yield [name, eid, clean_name, clean["eid"]]
                else:
                    ceid = f"{prefix}_{next_id}"
                    logger.info(f"Minting new id {ceid} for '{clean_name}'")
                    next_id += 1
                    new_entities[clean_name] = {
                        "eid": ceid,
                        "clean_name": clean_name,
                    }
                    yield [name, eid, clean_name, ceid]


def main(csvin, csvout):
    max_id, prefix, entities = load_entities_csv(csvin)
    logger.info(f"Max id: {max_id}")
    logger.info(f"ID prefix: {prefix}")
    entities = dedupe_the(entities)
    old_ids = set()
    new_ids = set()
    with open(csvout, "w") as ofh:
        writer = csv.writer(ofh, dialect="excel")
        for row in clean_map(max_id, prefix, entities):
            writer.writerow(row)
            old_ids.add(row[1])
            new_ids.add(row[3])
    logger.info(f"old ids: {len(old_ids)}")
    logger.info(f"new ids: {len(new_ids)}")


if __name__ == "__main__":
    ap = ArgumentParser("Map entities to cleaned values")
    ap.add_argument(
        "-i",
        "--input",
        type=Path,
        help="CSV file to convert",
    )
    ap.add_argument(
        "-o",
        "--output",
        default="results.csv",
        type=Path,
        help="Output csv",
    )
    ap.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Set log level to debug",
    )
    args = ap.parse_args()

    loglevel = logging.INFO
    if args.verbose:
        loglevel = logging.DEBUG

    logger.setLevel(loglevel)
    logch = logging.StreamHandler()
    logch.setLevel(loglevel)
    logger.addHandler(logch)

    main(args.input, args.output)
