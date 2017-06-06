from bot import *
import requests
import json
import threading

def get_json(html):
    page = requests.get(html)
    print(html)
    text = page.text
    data = json.loads(text)
    return data

def get_character(apikey, name):
    data = get_json("http://census.daybreakgames.com/s:" + apikey + "/json/get/ps2:v2/character/?name.first_lower=" + name.lower)
    character_id = data['character_list'][0]['character_id']
    name = data['character_list'][0]['name']['first']
    faction = get_faction(data['character_list'][0]['faction_id'])
    battle_rank = data['character_list'][0]['battle_rank']['value']
    next_battle_rank = data['character_list'][0]['battle_rank']['percent_to_next']
    return


def get_faction(faction_id):
    if faction_id == '1':
        faction = 'TR'
    elif faction_id == '2':
        faction = 'NC'
    elif faction_id == '3':
        faction = 'VS'
    else:
        faction = 'none'
    return faction


if __name__ == "__main__":
    print("Commands involving getting the JSON files from Census and Fisu APIs, also make for styling the text for the"
          "Emerald stream extension.")

