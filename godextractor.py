"""
1. Create a parser for the following HTML and parse it to a dictionary containing the name, aka, rivals, description and the associated powers, abilities and epic attributes should be in lists.

Example HTML:
<div id="page-content">
    <p><strong>Name</strong>: Anubis<br>
    <strong>AKA</strong>: Yinepu, Anupu</p>
    <p>Anubis, judge of.</p>
    <p>Anubis used to live as an undertaker, a judge, a lawyer, a jeweler and a bodyguard as the mood of the day struck him. None of his clients ever died while under his protection, though few lasted long after his angry departures.</p>
    <p>The Scions of Anubis are similarly dedicated, and similarly fickle. Excellent judges of character like their father, these Scions frequently maintain an intense loyalty to other Scions and Bands they deem worthy.</p>
    <p><strong>Associated Powers</strong>: Epic Perception, Animal (Jackal), Death, Guardian, Heku, Justice<br>
    <strong>Abilities</strong>: Animal Ken, Empathy, Integrity, Medicine, Melee, Occult<br>
    <strong>Rivals</strong>: Set; Baron Samedi, Hermes, Izanami, Tezcatlipoca, Vidar</p>
</div>
"""

from bs4 import BeautifulSoup
from pprint import pprint as pp
import json
import requests



#print(soup.prettify())

#print(soup.find('div', {'id':'page-content'}))
#print(soup.find('div', {'id':'page-content'}).text)


def parse_scion(scion, soup):
    
    scion_dict = {}

    pantheon = soup.find('div', {"id": "breadcrumbs"}).text.split(" » ")[1]
    
    name = scion.find('strong', text='Name').next_sibling.text.strip().replace(": ","")

    aka = scion.find('strong', text='AKA').next_sibling.strip().replace(": ","").split(",")

    description = "\n\n".join([d.text for d in soup.find_all('p') if len(d.text) > 20][1:]).split("Associated")[0].replace(": ","")

    epic_attributes = [p.strip() for p in scion.find('strong', text='Associated Powers').next_sibling.strip().replace(": ","").split(",") if "Epic" in p]
    purviews = [p.strip() for p in scion.find('strong', text='Associated Powers').next_sibling.strip().replace(": ","").split(",") if "Epic" not in p]

    abilities = scion.find('strong', text='Abilities').next_sibling.strip().replace(": ","").split(",")

    rivals = scion.find('strong', text='Rivals').next_sibling.replace(": ","").replace(";",",").strip().split(",")

    scion_dict = {
                "name": name,
                "aka": [],
                "description": None,
                "rivals": [],
                "favoured":{
                    "purviews":[],
                    "epic_attributes":[],
                    "abilities":[],
                }     
    }

    scion_dict['aka'] = aka
    scion_dict['description'] = description
    scion_dict['favoured']['purviews'] = purviews
    scion_dict['favoured']['epic_attributes'] = epic_attributes
    scion_dict['favoured']['abilities'] = abilities
    scion_dict['rivals'] = rivals

    return name, pantheon, scion_dict


def main(url):    
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    content = soup.find('div', {'id': 'page-content'})

    #print(content)

    #print(content.prettify())

    #print(content.find('p').text)

    #print(content.find('p').text)

    #print(content.find('p').text)

    try:
        return parse_scion(content, soup)
    except Exception as e:
        print(url)
        raise e

if __name__ == '__main__':

    url_list = [
    "http://scion-dayone.wikidot.com/god:anubis",
    "http://scion-dayone.wikidot.com/god:atum-re",
    "http://scion-dayone.wikidot.com/god:bastet",
    "http://scion-dayone.wikidot.com/god:geb",
    "http://scion-dayone.wikidot.com/god:horus",
    "http://scion-dayone.wikidot.com/god:isis",
    "http://scion-dayone.wikidot.com/god:osiris",
    "http://scion-dayone.wikidot.com/god:ptah",
    "http://scion-dayone.wikidot.com/god:set",
    "http://scion-dayone.wikidot.com/god:sobek",
    "http://scion-dayone.wikidot.com/god:aphrodite",
    "http://scion-dayone.wikidot.com/god:apollo",
    "http://scion-dayone.wikidot.com/god:ares",
    "http://scion-dayone.wikidot.com/god:artemis",
    "http://scion-dayone.wikidot.com/god:athena",
    "http://scion-dayone.wikidot.com/god:dionysus",
    "http://scion-dayone.wikidot.com/god:hades",
    "http://scion-dayone.wikidot.com/god:hephaestus",
    "http://scion-dayone.wikidot.com/god:hera",
    "http://scion-dayone.wikidot.com/god:hermes",
    "http://scion-dayone.wikidot.com/god:poseidon",
    "http://scion-dayone.wikidot.com/god:zeus",
    "http://scion-dayone.wikidot.com/god:baldur",
    "http://scion-dayone.wikidot.com/god:freya",
    "http://scion-dayone.wikidot.com/god:freyr",
    "http://scion-dayone.wikidot.com/god:frigg",
    "http://scion-dayone.wikidot.com/god:heimdall",
    "http://scion-dayone.wikidot.com/god:hel",
    "http://scion-dayone.wikidot.com/god:loki",
    "http://scion-dayone.wikidot.com/god:odin",
    "http://scion-dayone.wikidot.com/god:sif",
    "http://scion-dayone.wikidot.com/god:thor",
    "http://scion-dayone.wikidot.com/god:tyr",
    "http://scion-dayone.wikidot.com/god:vidar",
    "http://scion-dayone.wikidot.com/god:huitzilopochtli",
    "http://scion-dayone.wikidot.com/god:miclntecuhtli",
    "http://scion-dayone.wikidot.com/god:quetzalcotl",
    "http://scion-dayone.wikidot.com/god:tezcatlipoca", 
    "http://scion-dayone.wikidot.com/god:tlaloc",
    "http://scion-dayone.wikidot.com/god:tlazoltotl",
    "http://scion-dayone.wikidot.com/god:xipe-totec",
    "http://scion-dayone.wikidot.com/god:amaterasu",
    "http://scion-dayone.wikidot.com/god:hachiman",
    "http://scion-dayone.wikidot.com/god:izanagi",
    "http://scion-dayone.wikidot.com/god:izanami",
    "http://scion-dayone.wikidot.com/god:raiden",
    "http://scion-dayone.wikidot.com/god:susano-o",
    "http://scion-dayone.wikidot.com/god:tsuki-yomi",
    "http://scion-dayone.wikidot.com/god:baron-samedi",
    "http://scion-dayone.wikidot.com/god:damballa",
    "http://scion-dayone.wikidot.com/god:erzulie",
    "http://scion-dayone.wikidot.com/god:kalfu",
    "http://scion-dayone.wikidot.com/god:legba",
    "http://scion-dayone.wikidot.com/god:ogoun",
    "http://scion-dayone.wikidot.com/god:shango",
    "http://scion-dayone.wikidot.com/god:aengus",
    "http://scion-dayone.wikidot.com/god:brigid",
    "http://scion-dayone.wikidot.com/god:dagda",
    "http://scion-dayone.wikidot.com/god:danu",
    "http://scion-dayone.wikidot.com/god:dian-cecht",
    "http://scion-dayone.wikidot.com/god:lugh",
    "http://scion-dayone.wikidot.com/god:manannan-mac-lir",
    "http://scion-dayone.wikidot.com/god:morrigan",
    "http://scion-dayone.wikidot.com/god:nuada",
    "http://scion-dayone.wikidot.com/god:ogma",
    "http://scion-dayone.wikidot.com/god:chang'e",
    "http://scion-dayone.wikidot.com/god:fuxi",
    "http://scion-dayone.wikidot.com/god:guanyin",
    "http://scion-dayone.wikidot.com/god:guan-yu",
    "http://scion-dayone.wikidot.com/god:houyi",
    "http://scion-dayone.wikidot.com/god:huang-di",
    "http://scion-dayone.wikidot.com/god:nezha",
    "http://scion-dayone.wikidot.com/god:nuwa",
    "http://scion-dayone.wikidot.com/god:shennong",
    "http://scion-dayone.wikidot.com/god:sun-wukong",
    "http://scion-dayone.wikidot.com/god:xiwangmu",
    "http://scion-dayone.wikidot.com/god:yanluo",
    "http://scion-dayone.wikidot.com/god:agni",
    "http://scion-dayone.wikidot.com/god:brahma",
    "http://scion-dayone.wikidot.com/god:ganesha",
    "http://scion-dayone.wikidot.com/god:indra",
    "http://scion-dayone.wikidot.com/god:kali",
    "http://scion-dayone.wikidot.com/god:lakshmi",
    "http://scion-dayone.wikidot.com/god:parvati",
    "http://scion-dayone.wikidot.com/god:sarasvati",
    "http://scion-dayone.wikidot.com/god:shiva",
    "http://scion-dayone.wikidot.com/god:surya",
    "http://scion-dayone.wikidot.com/god:vishnu",
    "http://scion-dayone.wikidot.com/god:yama",
    "http://scion-dayone.wikidot.com/god:anahita",
    "http://scion-dayone.wikidot.com/god:ard",
    "http://scion-dayone.wikidot.com/god:haoma",
    "http://scion-dayone.wikidot.com/god:mah",
    "http://scion-dayone.wikidot.com/god:mithra",
    "http://scion-dayone.wikidot.com/god:sraosha",
    "http://scion-dayone.wikidot.com/god:tishtrya",
    "http://scion-dayone.wikidot.com/god:vahram",
    "http://scion-dayone.wikidot.com/god:vayu",
    "http://scion-dayone.wikidot.com/god:zam",
    "http://scion-dayone.wikidot.com/god:amnis",
    "http://scion-dayone.wikidot.com/god:badarus",
    "http://scion-dayone.wikidot.com/god:demosia",
    "http://scion-dayone.wikidot.com/god:heshon",
    "http://scion-dayone.wikidot.com/god:kuros",
    "http://scion-dayone.wikidot.com/god:skaft"
    ]

    gods = {
        "Pesedjet" : {"gods":{}},
        "Dodekatheon" : {"gods":{}},
        "Aesir" : {"gods":{}},
        "Atzlanti" : {"gods":{}},
        "Amatsukami" : {"gods":{}},
        "Loa" : {"gods":{}},
        "Tuatha" : {"gods":{}},
        "Celestial Bureaucracy" : {"gods":{}},
        "Devas" : {"gods":{}},
        "Yazata" : {"gods":{}},
        "Atlantean" : {"gods":{}},
    }

    for url in url_list:
        name, pantheon, god_json = main(url)
        
        gods[pantheon]["gods"][name] = god_json

    with open("gods.json", "w") as f:
        json.dump(gods, f, indent=4)