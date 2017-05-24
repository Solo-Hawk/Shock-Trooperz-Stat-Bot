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
    nextbattlerank = data['character_list'][0]['battle_rank']['percent_to_next']
    faction = grab_faction(data['character_list'][0]['faction_id'])
    lastlogin = data['character_list'][0]['times']['last_login_date']
    certs = data['character_list'][0]['certs']['available_points']
    response = "Character Name : " + playername + '\n' \
               + "Faction : " + faction + '\n' \
               + "Battle Rank : " + battlerank + '\n' \
               + "Battle Rank Completion %" + str((float(nextbattlerank) * 100)) + '\n' \
               + "You have " + certs + " certs available" + '\n' \
               + "Last Logged In :  " + lastlogin + '\n'
    return response, playerid

def filter_weapon(ID):
    text_file = open("filter.txt", "r")
    data = text_file.read()
    wepIDs = (str(data).split('\n'))
    for weapon in wepIDs:
        #  print("                 ", ID, " - AGAINST - ", weapon)
        if int(ID) == int(weapon):
            return False
    return True



def get_kills(apikey, playerID, sampleSizeStart, sampleSize, bushido):
    html = "https://census.daybreakgames.com/s:" + apikey \
           + "/get/ps2:v2/characters_event/?character_id=" \
           + playerID + "&type=KILL,DEATH&c:limit=" \
           + sampleSize
    hs = 0
    kills = 0
    deaths = 0
    recordedevents = 0
    data = grab_json(html)
    for x in range(int(sampleSizeStart),int(sampleSize)):
        try:
            if data['characters_event_list'][x]['table_type'] == 'kills':
                if bushido:
                    check = filter_weapon(data['characters_event_list'][x]['table_type'])
                    if check:
                        hs += int(data['characters_event_list'][x]['is_headshot'])
                        kills += 1
                else:
                    hs += int(data['characters_event_list'][x]['is_headshot'])
                    kills += 1
            elif data['characters_event_list'][x]['table_type'] == 'kills':
                deaths += 1
            recordedevents += 1
        except IndexError:
            break

    try:
        kdr = kills / deaths
    except ZeroDivisionError:
        kdr = 'infinity'


    try:
        hsr = kills / hs
        hsr = hsr * 100
    except ZeroDivisionError:
        hsr = 'infinity'

    response = "(Last " + str(recordedevents) + " events)" + '\n' \
               + "Kills : " + str(kills) + "| Headshots : " + str(hs) + "| Deaths : " + str(deaths) + '\n' \
               + "KDR : " + str(kdr) + '\n' \
               + "HSR : %" + str(hsr) + '\n'

    return response, data, kills, hsr

def grab_wepsused(sorted_data, killsample):
    weps = []
    count = 1
    for x in range(killsample-1):
        isdouble = False
        for q in weps:
            #print("---------------------- ", q)
            #   print(sorted_data['characters_event_list'][x]['attacker_weapon_id'])
            if q == sorted_data['characters_event_list'][x]['attacker_weapon_id']:
                isdouble = True

                #print("xxxxxxx", q)

            #print(str(isdouble))

            #print(sorted_data['characters_event_list'][x]['attacker_weapon_id'])

        if not isdouble:
            weps.append(sorted_data['characters_event_list'][x]['attacker_weapon_id'])

    return weps

def grab_weapons_data(apikey, id, data, kills, hsr):
    weps = grab_wepsused(data, kills)
    weapons = []
    weapons.append([])
    weapons.append([])
    weapons.append([])
    for x in weps:
        data = grab_json("http://census.daybreakgames.com/s:" + apikey + "/get/ps2:v2/characters_weapon_stat?character_id=" + id + "&item_id=" + x + "&c:limit=50&c:lang=en&c:resolve=item&c:sort=value:-1")
        try:
            weapon = str(data['characters_weapon_stat_list'][0]['item_id'])
            check = filter_weapon(weapon)
            print(str(check))
            if check == True and int(data['characters_weapon_stat_list'][0]['item']['is_vehicle_weapon']) == 0:
                try:
                    print("------Data------")
                    print(data['characters_weapon_stat_list'][0]['item_id'])
                    print(data['characters_weapon_stat_list'][0]['item']['name']['en'])
                    print(data['characters_weapon_stat_list'][2]['value'])
                    print(data['characters_weapon_stat_list'][3]['value'])
                    weapons[0].append(data['characters_weapon_stat_list'][0]['item']['name']['en'])
                    weapons[1].append(data['characters_weapon_stat_list'][2]['value'])
                    weapons[2].append(data['characters_weapon_stat_list'][3]['value'])

                except(KeyError, IndexError):
                    print('')
            else:
                print("--------Empty---------")
        except IndexError:
            print("Error")


    print(weapons[0])
    print(weapons[1])
    print(weapons[2])
    print(len(weapons[0]))
    for x in range(len(weapons[0])):
        print("-------Data-------")
        print(weapons[0][x])
        print(weapons[1][x])
        try:
            print(weapons[2][x])
        except IndexError:
            print("Index Error")


    total = []
    accuracy = 0
    for x in range(len(weapons[0])):
        total.append((100 / float(weapons[1][x])) * float(weapons[2][x]))
    for x in range(len(total)):
        accuracy += total[x]
    try:
        accuracy = accuracy / len(total)
    except:
        accuracy = 0

    ivi = accuracy * hsr

    response = "Infantry Acc : %" + str(accuracy) + '\n' \
               + "IvI Score : " + str(ivi) + '\n'

    return response


