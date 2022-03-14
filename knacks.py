import requests
import bs4
import json
from pprint import pprint as pp
import re
import random

import argparse

from dprint import Dprint
from tableparser import parse_table

KNACKS_WITH_TABLES = ["Rumor Mill", "Trendsetter",
                      "Scent The Divine", "Concept To Execution"]

# Setup debug logger
dprinter = Dprint()

with open("config.json", "r") as f:
    config = json.load(f)


def choose_random_knacks(character_data, god_data, new_knacks):
    with open("knacks.json") as f:
        data = json.load(f)

    favoured_epic_attributes = [ea.replace("Epic ", "").lower(
    ) for ea in god_data["favoured"]["epic_attributes"]]
    while(sum([v for k, v in new_knacks.items()]) > 0):
        for knack_attr in new_knacks:
            knack_list = character_data["knacks"]
            knack_attr_list = data[knack_attr]
            current_knack_titles = [k["title"] for k in knack_list]
            if any(knack_attr in fea for fea in favoured_epic_attributes) and new_knacks[knack_attr] > 0:
                random_knack = random.choice(data[knack_attr])
                if random_knack["prereqs"] in current_knack_titles:
                    character_data["knacks"].append(random_knack)
                else:
                    if random_knack["prereqs"] is None:
                        character_data["knacks"].append(random_knack)

                new_knacks[knack_attr] -= 1
            else:
                if random.randint(0, 1):
                    random_knack = random.choice(data[knack_attr])
                    if random_knack["prereqs"] in current_knack_titles:
                        character_data["knacks"].append(random_knack)
                    else:
                        if random_knack["prereqs"] is None:
                            character_data["knacks"].append(random_knack)

                    new_knacks[knack_attr] -= 1

    return character_data


def get_random_knacks(attr, character_data, god_data, quantity=1):
    with open("knacks.json") as f:
        data = json.load(f)

    knack_list = []
    favoured_epic_attributes = [ea.replace(
        "epic_", "") for ea in god_data["favoured"]["epic_attributes"]]
    for knack in data:
        for ea in favoured_epic_attributes:
            if knack.lower() in ea.lower():
                character_data["knacks"].append(
                    random.sample(data[knack], quantity))

    return character_data


def search_knacks(term):
    with open("knacks.json") as f:
        data = json.load(f)

    for knack_attr in data:
        for knack_list in data[knack_attr]:
            try:
                if knack_list["title"] != None and knack_list["description"] != None:
                    if term.lower() in knack_list["title"].lower():
                        tables = knack_list["tables"]
                        return knack_list["title"], knack_list["description"], tables
            except TypeError as te:
                raise te

    return(None, None, None)


def get_knacks(url):
    knacks = []
    filterstring = [
        "page-content",
        "EPIC STRENGTH KNACKS",
    ]
    # Get the html from the page and parse it with BeautifulSoup
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    # Find all of the divs that contain a knack, then loop through them to extract the data we need into our dictionary
    knack_divs = soup.find('div', attrs={'id': 'page-content'})
    knacks_split = str(knack_divs).split("<strong>")
    for ks in knacks_split:
        knack = ks.split("<p>")
        title = knack[0].replace("</strong></p>", "").replace("\n", "")
        description = []

        table_list = []
        for d in knack[1:]:
            if "Scent The Divine" in title:
                d = d.replace(
                    '<table class=\"wiki-content-table\">\n<tr>\n<td>', "")
                tables = bs4.BeautifulSoup(" ".join(knacks_split), "html.parser").find_all(
                    "table", {"class": "wiki-content-table"})
            else:
                tables = bs4.BeautifulSoup(d, "html.parser").find_all("table")

            if tables:
                for table in tables:
                    table_list.append(parse_table(table))

            d = d.replace("Caveat:", "<Caveat>")
            d = d.replace("Prerequisite Knacks:", "<Prerequisites>")
            d = d.replace("  .", "")
            d = d.replace('</p>\n', '')
            d = d.replace('</div>', '')
            d = d.replace('<ul>', "\n")
            d = d.replace('<li>', "\n* ")
            d = d.replace('</li>', "\n")
            d = d.replace('</ul>', "\n")
            description.append(d)

        description_split = "\n".join(description)

        prerequisites = description_split.split(" ")
        prereqs = None

        if "Prerequisite" in prerequisites[0] and "(Scion:" in prerequisites[6]:
            prereqs = f"{prerequisites[2]} {prerequisites[3]} {prerequisites[4]} {prerequisites[5]}"

        if "Prerequisite" in prerequisites[0] and "(Scion:" in prerequisites[5]:
            prereqs = f"{prerequisites[2]} {prerequisites[3]} {prerequisites[4]}"

        if "Prerequisite" in prerequisites[0] and "(Scion:" in prerequisites[4]:
            prereqs = f"{prerequisites[2]} {prerequisites[3]}"

        if "Prerequisite" in prerequisites[0] and "(Scion:" in prerequisites[3]:
            prereqs = f"{prerequisites[2]}"

        k = {
            "title": title,
            "description": description,
            "prereqs": prereqs,
            "tables": table_list
        }

        dprinter.dp(k)

        if any(f in title for f in filterstring):
            pass
        else:
            knacks.append(k)

    return knacks


def main(crawl, test):
    knack_urls = {
        "stre": "http://scion-mmp.wikidot.com/str-knacks",
        "dex": "http://scion-mmp.wikidot.com/dex-knacks",
        "sta": "http://scion-mmp.wikidot.com/sta-knacks",
        "cha": "http://scion-mmp.wikidot.com/cha-knacks",
        "app": "http://scion-mmp.wikidot.com/app-knacks",
        "man": "http://scion-mmp.wikidot.com/man-knacks",
        "per": "http://scion-mmp.wikidot.com/per-knacks",
        "inte": "http://scion-mmp.wikidot.com/int-knacks",
        "wits": "http://scion-mmp.wikidot.com/wit-knacks",
    }

    knacks = {}

    if crawl:
        for knack_attr, url in enumerate(knack_urls):
            knacks[url] = get_knacks(knack_urls[url])

        with open("knacks.json", "w") as f:
            json.dump(knacks, f, indent=4)

    if test:
        print("Knack Debugger")
        print("==============")
        pp(search_knacks("cat"))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Knack scanner for Scion 1e.")
    parser.add_argument('--crawl', '-c', action='store_true')
    parser.add_argument('--test', '-t', action='store_true')

    args = parser.parse_args()

    main(args.crawl, args.test)
