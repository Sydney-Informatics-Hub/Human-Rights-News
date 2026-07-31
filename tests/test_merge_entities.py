from preprocess import merge_all_entities
from pathlib import Path
import json
import pytest


def test_three_way_merge(tmp_path, test_files):
    ejson = test_files["entity_merge"]["sources"]
    output = Path(tmp_path) / "final.json"
    merge_all_entities(ejson, output)
    with open(output, "r") as fh:
        results = json.load(fh)
    with open(test_files["entity_merge"]["merged"], "r") as efh:
        expected = json.load(efh)
    assert results == expected


@pytest.mark.parametrize("error_case", ["inconsistent", "collision"])
def test_errors(error_case, tmp_path, test_files):
    case = test_files["entity_merge"]["errors"][error_case]
    print(case)
    jsons = case["sources"]
    expect_err = case["error"]
    output = Path(tmp_path) / "final.json"
    with pytest.raises(ValueError) as err:
        merge_all_entities(jsons, output)
    assert expect_err in str(err.value)
