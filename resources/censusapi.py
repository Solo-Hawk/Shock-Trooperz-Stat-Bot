import requests
import json
import threading

def get_json(html):
    page = requests.get(html)
    print(html)
    text = page.text
    data = json.loads(text)
    return data


def get_character(apikey, name):  # grabs basic data of the user through their name in lowercase form, returns none if no player info was found/
    result = None
    try:
        data = get_json("http://census.daybreakgames.com/s:" + apikey + "/json/get/ps2:v2/character/?name.first_lower=" + name.lower())
        character_id = str(data['character_list'][0]['character_id'])
        name = str(data['character_list'][0]['name']['first'])
        faction = str(get_faction(data['character_list'][0]['faction_id']))
        battle_rank = str(data['character_list'][0]['battle_rank']['value'])
        next_battle_rank = str(data['character_list'][0]['battle_rank']['percent_to_next'])
        result = [character_id,name,faction,battle_rank,next_battle_rank]
    except Exception as e:
        raise e

    return result  # return list object formatted in (character_id, name, faction, battle_rank, next_battle_rank)


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


def validate_bushido(ID):  # checks weapon against bushido filter list (courtesy of Joke Stat Tracker)
    text_file = open("resources/filter.txt", "r")
    data = text_file.read()

    for weapon in str(data).split('\n'):
        if int(ID) == int(weapon):
            return False
    return True


def get_events(apikey, character_id, samplestart, samplesize):  # gets the KDR and HSR including weapons the target player has used and the kills from the events of that gun
    topweapons = []
    classweapons = []
    kills = 0
    deaths = 0
    events = 0
    headshots = 0
    sampleSearch = samplestart + samplesize
    data = get_json("https://census.daybreakgames.com/s:"+apikey+"/get/ps2:v2/characters_event/?character_id=" + character_id + "&type=KILL,DEATH&c:limit=" + sampleSearch)
    for i in range(int(samplestart), int(samplesize)):
        check = True
        try:
            if data['characters_event_list'][i]['table_type'] == 'kills' and\
            data['characters_event_list'][i]['attacker_character_id'] == character_id and \
            not validate_bushido(data['characters_event_list'][i]['attacker_weapon_id'] and
            data['characters_event_list'][i]['attacker_vehicle_id'] == '0'):

                headshots += int(data['characters_event_list'][i]['is_headshot'])
                kills += 1
                for j in range(len(classweapons)):
                    if data['characters_event_list'][i]['attacker_loadout_id'] == classweapons[j][0]:
                        check = False
                        classweapons[j][2] = classweapons[j][2] + 1
                if check:
                    classweapons.append([data['characters_event_list'][i]['attacker_loadout_id'], data['characters_event_list'][i]['attacker_weapon_id'], 0])

            else:
                deaths += 1
            events += 1
        except IndexError:
            break
    for i in classweapons:
        if i[2] > 100:
            print(i[2])
            topweapons.append(i)


    result = [kills, deaths, headshots, events, classweapons, topweapons]
    return result  # return list object formatted in (kills, deaths, headshots, events, classweapons, topweapons)

def get_accuracy(apikey, character_id, weapons, samplesize):
    profiles = " "
    dailyfire = 0
    dailyhit = 0
    dailyacc = 0
    weeklyfire = 0
    weeklyhit = 0
    weeklyacc = 0
    monthlyfire = 0
    monthlyhit = 0
    monthlyacc = 0
    lifefire = 0
    lifehit = 0
    lifeacc = 0
    for i in range(len(weapons)):
        try:
            if profiles.index(weapons[i][0]) == -1:
                temp = None
        except ValueError:
            profiles = profiles + weapons[i][0] + ","
    data = get_json(
        "https://census.daybreakgames.com/s:"+apikey+"/get/ps2:v2/characters_stat?character_id="+character_id+"&stat_name=fire_count,hit_count&profile_id="+profiles+"&c:limit=50")
    print("https://census.daybreakgames.com/s:"+apikey+"/get/ps2:v2/characters_stat?character_id="+character_id+"&stat_name=fire_count,hit_count&profile_id="+profiles+"&c:limit=50")
    for i in range(len(data['characters_stat_list'])):
        if data['characters_stat_list'][i]['stat_name'] == "fire_count":
            dailyfire = dailyfire + int(data['characters_stat_list'][i]['value_daily'])
            weeklyfire = weeklyfire + int(data['characters_stat_list'][i]['value_weekly'])
            monthlyfire = monthlyfire + int(data['characters_stat_list'][i]['value_monthly'])
            lifefire = lifefire + int(data['characters_stat_list'][i]['value_forever'])
        if data['characters_stat_list'][i]['stat_name'] == "hit_count":
            dailyhit = dailyhit + int(data['characters_stat_list'][i]['value_daily'])
            weeklyhit = weeklyhit + int(data['characters_stat_list'][i]['value_weekly'])
            monthlyhit = monthlyhit + int(data['characters_stat_list'][i]['value_monthly'])
            lifehit = lifehit + int(data['characters_stat_list'][i]['value_forever'])
    dailyacc = dailyhit / dailyfire
    weeklyacc = weeklyhit / weeklyfire
    monthlyacc = monthlyhit / monthlyfire
    lifeacc = lifehit / lifefire
    if dailyfire >= int(samplesize):
        return ['Daily', dailyacc]
    if weeklyfire >= int(samplesize):
        return ['Weekly', weeklyacc]
    if monthlyfire >= int(samplesize):
        return ['Monthly', monthlyacc]
    if lifefire >= int(samplesize):
        return ['Lifetime', lifeacc]
    return None

def get_wep(apikey, id, weapon):
    print(weapon)
    data = get_json("http://census.daybreakgames.com/s:" + apikey + "/get/ps2:v2/characters_weapon_stat?character_id=" + id + "&item_id=" + weapon + "&c:limit=50&c:lang=en&c:resolve=item&c:sort=value:-1")
    return data['characters_weapon_stat_list'][0]['item']['name']['en']


if __name__ == "__main__":
    print("Commands involving getting the JSON files from Census and Fisu APIs, also make for styling the text for the"
          "Emerald stream extension.")

