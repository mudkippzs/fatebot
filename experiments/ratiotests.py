from difflib import SequenceMatcher
from pprint import pprint

def similar(a, b):
            return SequenceMatcher(None, a, b).ratio()

test_list = [
        "a",
        "b",
        "c",
        "ab",
        "ac",
        "ba",
        "bc",
        "ca",
        "cb",
        "abc",
        "cba",
        "bac",
        "acb",
        "cab",
        "bca",
        "d",
        "e",
        "f",
        "def",
        "efd",
        "fde",
        "dfe",
        "fed",
        "edf",
        "da",
        "dab",
        "dea",
        "daf"
]

attributes = [
        "stre",
        "dex",
        "sta",
        "cha",
        "man",
        "app",
        "per",
        "inte",
        "wits",
]

abilities = [
        "academics",
        "animal_ken",
        "art",
        "athletics",
        "awareness",
        "brawl",
        "command",
        "control",
        "craft",
        "empathy",
        "fortitude",
        "integrity",
        "investigation",
        "larceny",
        "marksmanship",
        "medicine",
        "melee",
        "occult",
        "presence",
        "politics",
        "science",
        "stealth",
        "survival",
        "thrown",
    ]

attrib_ratios = []
for attrib_1 in attributes:
        for attrib_2 in attributes:
                if attrib_1 != attrib_2:
                        ratio = similar(attrib_1, attrib_2)
                        attrib_ratios.append((attrib_1, attrib_2, ratio))

ability_ratios = []
for ability_1 in abilities:
        for ability_2 in abilities:
                if ability_1 != ability_2:
                        ratio = similar(ability_1, ability_2)
                        ability_ratios.append((ability_1, ability_2, ratio))


test_ratios = []
for test_1 in test_list:
        for test_2 in test_list:
                if test_1 != test_2:
                        ratio = similar(test_1, test_2)
                        test_ratios.append((test_1, test_2, ratio))

pprint(sorted(attrib_ratios, key=lambda x: x[2])[-1:-5])
pprint(sorted(ability_ratios, key=lambda x: x[2])[-1:-5])
pprint(sorted(test_ratios, key=lambda x: x[2]))