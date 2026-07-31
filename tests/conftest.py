import pytest
from pathlib import Path


@pytest.fixture
def test_files():
    fixtures_dir = Path("tests") / "fixtures"
    return {
        "deduplicate": {
            "max_id": 7,
            "prefix": "geo",
            "raw": fixtures_dir / "geo_entities.csv",
            "deduped": fixtures_dir / "geo_deduped.csv",
        },
        "entity_merge": {
            "sources": [
                fixtures_dir / "entities/batch1/geo_entities.json",
                fixtures_dir / "entities/batch2/geo_entities.json",
                fixtures_dir / "entities/batch3/geo_entities.json",
            ],
            "merged": fixtures_dir / "entities/geo_entities_merged.json",
            "errors": {
                "inconsistent": {
                    "sources": [
                        fixtures_dir / "entities/batch4/geo_entities.json",
                        fixtures_dir / "entities/batch5/geo_entities.json",
                    ],
                    "error": "inconsistent ids for america: 0, 1",
                },
                "collision": {
                    "sources": [
                        fixtures_dir / "entities/batch6/geo_entities.json",
                        fixtures_dir / "entities/batch7/geo_entities.json",
                    ],
                    "error": "id collision for 0: america, britain",
                },
            },
        },
    }
