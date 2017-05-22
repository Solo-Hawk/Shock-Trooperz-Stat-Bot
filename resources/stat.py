import json
import requests

import asyncio
import resources.censusapi
import discord
def get_apikey(self, file):
    with open(file, 'r') as f:
        password = f.read()

    return password

apikey = get_apikey("resources/apikey.txt")


def stats(self, discord_client, playername, samplesize):
    playerid, playername, battlerank, nextbattlerank, faction, lastlogin, certs = censusapi.get_meta(apikey, playername)
    response =  "```" + '\n' \
               + "Character Name : " + playername + '\n' \
               + "Faction : " + faction + '\n' \
               + "Battle Rank : " + battlerank + '\n' \
               + "Battle Rank Completion %" + str((float(nextbattlerank) * 100)) + '\n' \
               + "You have " + certs + " certs available" + '\n' \
               + "Last Logged In :  " + lastlogin+ '\n' \
               + "```"
    return response
def statm(self, discord_client, playername, samplesize):
    playerid, playername, battlerank, nextbattlerank, faction, lastlogin, certs = censusapi.get_meta(apikey, playername)

def statl(self, discord_client, playername, samplesize):
    playerid, playername, battlerank, nextbattlerank, faction, lastlogin, certs = censusapi.get_meta(apikey, playername)

