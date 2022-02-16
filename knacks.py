"""
1. Create a web crawler to extract the content at http://scion-mmp.wikidot.com/dex-knacks
2. Store the content in a JSON object and print it out.
"""

import requests
import bs4
import json
from pprint import pprint as pp
import re
import random

from tableparser import parse_table

KNACKS_WITH_TABLES = ["Rumor Mill", "Trendsetter", "Scent The Divine", "Concept To Execution"]

def get_all_knacks_by_attr(attr, character_data, god_data):
    with open("knacks.json") as f:
        data = json.load(f)

    knack_list = []
    favoured_epic_attributes = [ea.replace("Epic ", "").lower() for ea in god_data["favoured"]["epic_attributes"]]
    random.shuffle(favoured_epic_attributes)
    try:
        fav_attr = favoured_epic_attributes[0]
    except IndexError:
        fav_attr = []

    for knack in data:
        if knack in attr:
            if knack in fav_attr:
                #print(f"Choosing {knack} knack...")
                chosen_knack = None
                #print(f"Searching for a new {knack}...")
                random.shuffle(data[knack])
                chosen_knack = data[knack][0]
                chosen_knack_title = chosen_knack["title"]
                #print(f"Checking if we have {chosen_knack_title}...")
                #print([k["title"] for k in character_data["knacks"]])
                if chosen_knack_title not in [k["title"] for k in character_data["knacks"]]:
                    #print(f"Added to list...")
                    character_data["knacks"].append(chosen_knack)
                    break
            else:
                #print(f"Choosing {knack} knack...")
                chosen_knack = None
                #print(f"Searching for a new {knack}...")
                random.shuffle(data[knack])
                chosen_knack = data[knack][0]
                chosen_knack_title = chosen_knack["title"]
                #print(f"Checking if we have {chosen_knack_title}...")
                #print([k["title"] for k in character_data["knacks"]])
                if random.randint(-1,1) is True and chosen_knack_title not in [k["title"] for k in character_data["knacks"]]:
                    #print(f"Added to list...")
                    character_data["knacks"].append(chosen_knack)
                    break


    return character_data


def get_random_knacks(attr, character_data, god_data, quantity = 1):
    with open("knacks.json") as f:
        data = json.load(f)

    knack_list = []
    favoured_epic_attributes = [ea.replace("epic_", "") for ea in god_data["favoured"]["epic_attributes"]]
    for knack in data:
        for ea in favoured_epic_attributes:
            if knack.lower() in ea.lower():
                character_data["knacks"].append(random.sample(data[knack], quantity))

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
                        knack_result = ((knack_list["title"]), knack_list["description"], tables)
                        return knack_result
            except TypeError as te:
                raise te

    return(None,None)


def get_knacks(url):
    knacks = []

    # Get the html from the page and parse it with BeautifulSoup
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    # Find all of the divs that contain a knack, then loop through them to extract the data we need into our dictionary
    knack_divs = soup.find('div', attrs={'id': 'page-content'})
    knacks_split = str(knack_divs).split("<strong>")
    for ks in knacks_split:
        knack = ks.split("<p>")
        title = knack[0].replace("</strong></p>","")
        description = []

        table_list = []
        for d in knack[1:]:            
            if "Scent The Divine" in title:
                d = d.replace('<table class=\"wiki-content-table\">\n<tr>\n<td>',"")
                tables = bs4.BeautifulSoup(" ".join(knacks_split), "html.parser").find_all("table", {"class": "wiki-content-table"})
            else:
                tables = bs4.BeautifulSoup(d, "html.parser").find_all("table")

            if tables:
                for table in tables:
                    table_list.append(parse_table(table))
            
            d = d.replace("Caveat:","<Caveat>")
            d = d.replace("Prerequisite Knacks:","<Prerequisites>")
            d = d.replace("  .","")
            d = d.replace('</p>\n','')
            d = d.replace('</div>','')
            d = d.replace('<ul>',"\n")
            d = d.replace('<li>',"\n* ")
            d = d.replace('</li>',"\n")
            d = d.replace('</ul>',"\n")
            description.append(d)

        k = {
            "title": title,
            "description": description,
            "tables": table_list
        }

        knacks.append(k)

    return knacks

def main():
    knack_urls = {
        "str" : "http://scion-mmp.wikidot.com/str-knacks",
        "dex" : "http://scion-mmp.wikidot.com/dex-knacks",
        "sta" : "http://scion-mmp.wikidot.com/sta-knacks",
        "cha" : "http://scion-mmp.wikidot.com/cha-knacks",
        "app" : "http://scion-mmp.wikidot.com/app-knacks",
        "man" : "http://scion-mmp.wikidot.com/man-knacks",
        "per" : "http://scion-mmp.wikidot.com/per-knacks",
        "int" : "http://scion-mmp.wikidot.com/int-knacks",
        "wit" : "http://scion-mmp.wikidot.com/wit-knacks",
    }

    knacks = {}

    for knack_attr, url in enumerate(knack_urls):
        knacks[url] = get_knacks(knack_urls[url])
    
    with open("knacks.json", "w") as f:
        json.dump(knacks, f, indent=4)

    
if __name__ == "__main__":
    #main()
    pass