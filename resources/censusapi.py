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

def get_character(apikey, name): # return list object formated in (character_id, name, faction, battle_rank, next_battle_rank)
    result = None
    try:
        data = get_json("http://census.daybreakgames.com/s:" + apikey + "/json/get/ps2:v2/character/?name.first_lower=" + name.lower)
        character_id = str(data['character_list'][0]['character_id'])
        name = str(data['character_list'][0]['name']['first'])
        faction = str(get_faction(data['character_list'][0]['faction_id']))
        battle_rank = str(data['character_list'][0]['battle_rank']['value'])
        next_battle_rank = str(data['character_list'][0]['battle_rank']['percent_to_next'])
        result = [character_id,name,faction,battle_rank,next_battle_rank]
    except Exception as e:
        raise e

    return result


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

def validate_bushido(ID):
    text_file = open("filter.txt", "r")
    data = text_file.read()

    for weapon in str(data).split('\n'):
        if int(ID) == int(weapon):
            return False
    return True

def get_events(apikey, character_id, samplestart, samplesize):
    weapons = []
    kills = 0
    deaths = 0
    events = 0
    headshots = 0
    sampleSearch = samplestart + samplesize
    data = get_json("https://census.daybreakgames.com/s:"+apikey+"/get/ps2:v2/characters_event/?character_id="+character_id+"type=KILL,DEATH&c:limit=" + sampleSearch)
    for i in range(int(samplestart), int(samplesize)):
        try:
            if data['characters_event_list'][i]['table_type'] == 'kills' and \
            not validate_bushido(data['characters_event_list'][i]['attacker_weapon_id'] and
            data['characters_event_list'][i]['attacker_vehicle_id'] == '0'):
                headshots += int(data['characters_event_list'][i]['is_headshot'])
                kills += 1
                weapons.append(data['characters_event_list'][i]['attacker_weapon_id'])
            else:
                deaths += 1
            events += 1
        except IndexError:
            break
        result = [kills, deaths, headshots, events, weapons]
    return result

def get_accuracy(weapons, profiles):
    data = get_json(
        "https://census.daybreakgames.com/s:558296/get/ps2:v2/characters_stat?character_id=5428257774265773585&stat_name=fire_count,hit_count&profile_id="+profiles+"&c:limit=50")

if __name__ == "__main__":
    print("Commands involving getting the JSON files from Census and Fisu APIs, also make for styling the text for the"
          "Emerald stream extension.")

