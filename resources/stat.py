import json
import requests

import asyncio
import resources.censusapi as censusapi
import discord

def get_apikey( file):
    with open(file, 'r') as f:
        password = f.read()

    return password

apikey = get_apikey("resources/apikey.txt")

def create_stats_response(character_result, event_result, accuracy_result):
    response = "Name : " + character_result[1] + "\nFaction : " \
                         + character_result[2] + "\nBR : "\
                         + character_result[3] \
                         + "\n% to next : " + character_result[4] \
    + "\nKills : " + str(event_result[0]) + " | Deaths : " + str(event_result[1])+ " | Headshots : " + str(event_result[2]) \
    + "\nKDR : " + str(event_result[0] / event_result[1]) \
    + "\nHSR : " + str((event_result[2] / event_result[0]) * 100) \
    + "\nAccuracy from " + str(accuracy_result[0]) + " History : " + str(accuracy_result[1] * 100) + "%" \
    + "\nIvI : " + str((accuracy_result[1] * 100)* (((event_result[2] / event_result[0]) * 100))    )
    return response

def top_weps(weapons, id):
    res = "\n --- Highlighted Weapon --- \n"

    for x in range(len(weapons)):
        print(weapons[x])
        res = res + censusapi.get_wep(apikey, id, weapons[x][1]) + " - " + str(weapons[x][2]) + " Kills \n"
    return res


def stats(discord_client, playername, samplesizestart, samplesize):

    response = "```"
    character_result = censusapi.get_character(apikey, playername)
    event_result = censusapi.get_events(apikey, character_result[0],samplesizestart,samplesize)
    accuracy_result = censusapi.get_accuracy(apikey, character_result[0], event_result[4], samplesize)
    response = response + create_stats_response(character_result, event_result, accuracy_result) +  "```"

    return response


def statm(discord_client, playername, samplesizestart, samplesize):
    response = "```"
    character_result = censusapi.get_character(apikey, playername)
    event_result = censusapi.get_events(apikey, character_result[0], samplesizestart, samplesize)
    accuracy_result = censusapi.get_accuracy(apikey, character_result[0], event_result[4], samplesize)


    response = response + create_stats_response(character_result, event_result, accuracy_result)
    response = response + top_weps(event_result[5], character_result[0])
    response = response + "```"
    return response

def statl(discord_client, playername, samplesizestart, samplesize):
    response = "```"

    # code here

    response = response + "```"
    return response
