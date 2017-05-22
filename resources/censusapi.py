import json
import requests

def grab_json(html):
    page = requests.get(html)
    print(html)
    text = page.text
    data = json.loads(text)
    return data

def grab_faction(id):
    if id == "1":
       faction = 'VS'
    elif id == "2":
       faction = 'NC'
    elif id == "3":
        faction = 'TR'
    else:
        faction = 'unknown'
    return faction

def get_meta(apikey, playername):
    playername = playername.lower()
    html = "https://census.daybreakgames.com/s:" \
           + apikey + "/get/ps2:v2/character/?name.first_lower=" \
           + playername
    data = grab_json(html)
    playerid = data['character_list'][0]['character_id']
    playername = data['character_list'][0]['name']['first']
    battlerank = data['character_list'][0]['battle_rank']['value']
    nextbattlerank = data['character_list'][0]['battle_rank']['percentage_to_next']
    faction = grab_faction(playername = data['character_list'][0]['faction_id'])
    lastlogin = data['character_list'][0]['times']['last_login_date']
    certs = data['character_list'][0]['certs']['available_points']

    return playerid, playername, battlerank, nextbattlerank, faction, lastlogin, certs