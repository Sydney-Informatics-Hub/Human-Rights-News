# Takes an updated entity JSON from TDM Studio and compares it to the
# existing OpenRefine clean map and report on what's mising


import logging
import csv
import json
from pathlib import Path
from argparse import ArgumentParser


# loglevel is set in __main__

logger = logging.getLogger(__name__)

# quick fix - get all the unmatched ones and append them to the clean maps


def main(prefix, jsonin, csvin, csvout):
    with open(jsonin, "r") as jfh:
        entities_json = json.load(jfh)
    raw_eids = {}
    for name, eid in entities_json.items():
        raw_eids[f"{prefix}_{eid}"] = {"name": name}
    with open(csvin, "r") as cfh:
        reader = csv.reader(cfh, dialect="excel")
        for row in reader:
            raw_eid = row[1]
            clean_eid = row[3]
            if raw_eid in raw_eids:
                raw_eids[raw_eid]["map_to"] = clean_eid
    unmatched = [eid for eid in raw_eids.keys() if "map_to" not in raw_eids[eid]]
    with open(csvout, "w") as cfh:
        writer = csv.writer(cfh, dialect="excel")
        for eid in unmatched:
            name = raw_eids[eid]["name"]
            writer.writerow([name, eid, name, eid])


if __name__ == "__main__":
    ap = ArgumentParser("Check updated entity JSON against clean maps")
    ap.add_argument(
        "-p",
        "--prefix",
        type=str,
        help="id prefix (geo or org)",
    )
    ap.add_argument(
        "-j",
        "--json",
        type=Path,
        help="Entity JSON file",
    )
    ap.add_argument(
        "-c",
        "--csv",
        type=Path,
        help="Existing clean map",
    )
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output clean map",
    )
    args = ap.parse_args()

    loglevel = logging.INFO

    logger.setLevel(loglevel)
    logch = logging.StreamHandler()
    logch.setLevel(loglevel)
    logger.addHandler(logch)

    main(args.prefix, args.json, args.csv, args.output)
