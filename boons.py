import argparse
import requests
import bs4
import json
from pprint import pprint as pp
import re

with open("config.json", "r") as f:
    config = json.load(f)

def get_boons_by_level(level, purview):
    with open("boons.json") as f:
        data = json.load(f)

    boon_result = []
    for boon_attr in data:
        if "animal" in purview.lower():
            purview = purview.split(" (")[0]
        if purview.lower() in boon_attr.lower():
            for idx, boon in enumerate(data[boon_attr]):
                if idx+1 <= level:
                    boon_result.append([boon["title"] ,boon["description"]])

    return boon_result

def search_boons(term):
    with open("boons.json") as f:
        data = json.load(f)

    boon_result = []
    for boon_attr in data:
        for boon_list in data[boon_attr]:
            try:
                filter_list = []
                if boon_list["title"] != None and boon_list["description"] != None and boon_list["title"] not in filter_list:
                    if term.lower() in boon_list["title"].lower():
                        boon_result.append(((boon_list["title"]), boon_list["description"]))
            except TypeError as te:
                raise te

    return boon_result                        

def get_boons(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    table = soup.find("div", {"id": "page-content"})
    rows = table.find_all("h3")
    boons_html = []
    boons = []
    
    for row in rows:
        desc_list = [d.string for d in row.next_sibling.next_sibling.contents if d.string]
        if row.contents and desc_list:
            title = row.contents[0].string
            description = " ".join(desc_list)
        
            k = {
                "title": title,
                "description": description,
            }
            boons.append(k)
    return boons
    

def main(crawl, test):
    if crawl:
        boon_urls = {
            "animal" : "http://scion-mmp.wikidot.com/animal-boons",
            "chaos" : "http://scion-mmp.wikidot.com/chaos-boons",
            "darkness" : "http://scion-mmp.wikidot.com/darkness-boons",
            "death" : "http://scion-mmp.wikidot.com/death-boons",
            "earth" : "http://scion-mmp.wikidot.com/earth-boons",
            "fertility" : "http://scion-mmp.wikidot.com/fertility-boons",
            "fire" : "http://scion-mmp.wikidot.com/fire-boons",
            "frost" : "http://scion-mmp.wikidot.com/frost-boons",
            "guardian" : "http://scion-mmp.wikidot.com/guardian-boons",
            "health" : "http://scion-mmp.wikidot.com/health-boons",
            "illusion" : "http://scion-mmp.wikidot.com/illusion-boons",
            "justice" : "http://scion-mmp.wikidot.com/justice-boons",
            "moon" : "http://scion-mmp.wikidot.com/moon-boons",
            "psychopomp" : "http://scion-mmp.wikidot.com/psychopomp-boons",
            "sky" : "http://scion-mmp.wikidot.com/sky-boons",
            "star" : "http://scion-mmp.wikidot.com/star-boons",
            "sun" : "http://scion-mmp.wikidot.com/sun-boons",
            "war" : "http://scion-mmp.wikidot.com/war-boons",
            "water" : "http://scion-mmp.wikidot.com/water-boons",
            "asha" : "http://scion-mmp.wikidot.com/asha-purview",
            "arete" : "http://scion-mmp.wikidot.com/arete-purview",
            "cheval" : "http://scion-mmp.wikidot.com/cheval-boons",
            "civitas" : "http://scion-mmp.wikidot.com/civitas-boons",
            "enech" : "http://scion-mmp.wikidot.com/enech-boons",
            "heku" : "http://scion-mmp.wikidot.com/heku-boons",
            "industry" : "http://scion-mmp.wikidot.com/industry-boons",
            "itzli" : "http://scion-mmp.wikidot.com/itzli-boons",
            "jotunblut" : "http://scion-mmp.wikidot.com/jotunblut-boons",
            "samsura" : "http://scion-mmp.wikidot.com/samsura-boons",
            "mana" : "http://scion-mmp.wikidot.com/mana-boons",
            "scire" : "http://scion-mmp.wikidot.com/scire-boons",
            "taiyi" : "http://scion-mmp.wikidot.com/taiyi-boons",
            "tsukumo-gami" : "http://scion-mmp.wikidot.com/tsukumo-gami-boons",
            "mystery" : "http://scion-mmp.wikidot.com/mystery-purview",
            "prophecy" : "http://scion-mmp.wikidot.com/prophecy-purview",
            "magic" : "http://scion-mmp.wikidot.com/magic-boons-purview",
            }

        boons = {}

        for boon_attr, url in enumerate(boon_urls):
             boons[url] = get_boons(boon_urls[url])
        
        with open("boons.json", "w") as f:
             json.dump(boons, f, indent=4)

    if test:
        print("Boon Debugger")
        print("=============")
        print(search_boons("avatar"))
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Boon scanner for Scion 1e.")
    parser.add_argument('--crawl','-c', action='store_true')
    parser.add_argument('--test','-t', action='store_true')
    
    args = parser.parse_args()

    main(args.crawl, args.test)
    