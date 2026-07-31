import csv
import re

# these are regular expressions to be matched against entity names

GROUP_LABELS = {
    "grp_1": "GROUP 1: European Human Rights System",
    "grp_2": "GROUP 2: United Nations System",
    "grp_3": "GROUP 3: Major Transnational NGOs",
    "grp_4": "GROUP 4: Russia, Soviet Union, USSR (combined)",
    "grp_5": "GROUP 5: Germany (combined)",
    "grp_6": "GROUP 6: Former Yugoslavia (combined)",
    "grp_7": "GROUP 7: United Kingdom (combined)",
    "grp_8": "GROUP 8: United States of America (combined)",
}

GROUP_TYPES = {
    "grp_1": "org",
    "grp_2": "org",
    "grp_3": "org",
    "grp_4": "geo",
    "grp_5": "geo",
    "grp_6": "geo",
    "grp_7": "geo",
    "grp_8": "geo",
}

GROUPS = {
    "grp_1": [
        "european convention",
        "^european human rights convention$",
        "^convention on human rights$",
        "^convention of human rights$",
        "^european convention for the protection of human rights$",
        "^ECHR$",
        "^european court of human rights$",
        "^european commission of human rights$",
        "^european commission on human rights$",
        "^council of Europe$",
        "^Strasbourg court$",
    ],
    "grp_2": [
        # negative lookahead, match all ^un except 'un watch'
        "^un (?!watch)",
        "^united nations",
        "^security council$",
        "^general assembly$",
        "^human rights council$",
        "^convention on the rights of the child$",
        "^convention against torture$",
        "^genocide convention$",
        "^UNHCR$",
        "^UNCRC$",
        "^UNICEF$",
    ],
    "grp_3": [
        "amnesty international",
        "red cross",
        "international red cross",
        "Oxfam",
        "medecins",
        "save the children",
        "human rights watch",
        "helsinki watch",
        "americas watch",
        "africa watch",
        "asia watch",
    ],
    "grp_4": [
        "russia",
        "soviet union",
        "ussr",
        "russian federation",
    ],
    "grp_5": [
        "germany",
        "east germany",
        "west germany",
        "federal republic",
        "federal republic of germany",
        "german democratic republic",
        "GDR",
        "Berlin",
    ],
    "grp_6": [
        "yugoslavia",
        "bosnia",
        "bosnia and herzogovina",
        "serbia",
        "croatia",
        "kosovo",
        "slovenia",
        "macedonia",
        "montenegro",
    ],
    "grp_7": [
        "united kingdom",
        "uk",
        "britain",
        "great britain",
        "england",
        "scotland",
        "wales",
        "northern ireland",
    ],
    "grp_8": [
        "united states",
        "usa",
        "america",
        "united states of america",
    ],
}


class EntityGroups:
    def __init__(self):
        self.groups = {}
        for group, res in GROUPS.items():
            self.groups[group] = [re.compile(r) for r in res]
        self._cache = {}

    def group(self, etype, entity_name):
        """Try to match an entity name against all the group res and
        return the first one it matches. Caches results in _cache"""
        if entity_name in self._cache:
            return self._cache[entity_name]
        for group, res in self.groups.items():
            if GROUP_TYPES[group] == etype:
                for pattern in res:
                    if pattern.search(entity_name):
                        self._cache[entity_name] = group
                        return group
        return None


def load_mapped_entities(fn):
    with open(fn, "r") as cfh:
        reader = csv.reader(cfh, dialect="excel")
        ents = {}
        for row in reader:
            raw_name = row[0]
            eid = row[1]
            clean_name = row[2]
            ceid = row[3]
            ents[eid] = {"raw_name": raw_name, "clean_name": clean_name, "ceid": ceid}
    return ents


def make_clean_map(entity_map):
    return {
        entity_map[eid]["ceid"]: entity_map[eid]["clean_name"]
        for eid in entity_map.keys()
    }
