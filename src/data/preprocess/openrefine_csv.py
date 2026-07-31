# convert entity JSON file to CSV for Openrefine

import json
import csv
from pathlib import Path

from config import MERGED_DIR


def entities_to_csv(datadir, outdir, etype):
    with open(datadir / f"{etype}_entities.json", "r") as jfh:
        entities = json.load(jfh)
    with open(outdir / f"{etype}_entities.csv", "w") as cfh:
        # QUOTE_ALL so that OpenRefine doesn't skip lines starting with #
        writer = csv.writer(cfh, quoting=csv.QUOTE_ALL)
        writer.writerow(["name", "eid"])
        for name, eid in entities.items():
            if name[0] == "#":
                print(f"Hash {name} {etype}_{eid}")
            writer.writerow([name, f"{etype}_{eid}"])


datadir = Path(MERGED_DIR)
outdir = datadir / "open_refine"

entities_to_csv(datadir, outdir, "geo")
entities_to_csv(datadir, outdir, "org")
