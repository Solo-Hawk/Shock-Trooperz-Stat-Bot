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


def stats(discord_client, playername, samplesizestart, samplesize):
    response = "```" + '\n'
    metaRes, playerID = censusapi.get_meta(apikey, playername)
    response = response + metaRes
    killRes, data, kills, hsr = response + censusapi.get_kills(apikey, playerID, samplesizestart, samplesize, False)
    response = response + killRes
    iviRes = censusapi.grab_weapons_data(apikey, id, data, kills, hsr)



    response = response + '```'

    return response
def statm(discord_client, playername, samplesizestart, samplesize):
    response = "```" + '\n'
    metaRes, playerID = censusapi.get_meta(apikey, playername)
    response = response + metaRes



    response = response + '```'

def statl(discord_client, playername, samplesizestart, samplesize):
    response = "```" + '\n'
    response = response + censusapi.get_meta(apikey, playername)

    response = response + '```'

