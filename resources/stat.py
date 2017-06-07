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

    response = "```"
    character_result = censusapi.get_character(apikey, playername)
    event_result = censusapi.get_events(apikey, character_result[0],samplesizestart,samplesize)
    accuracy_result = censusapi.get_accuracy(apikey, character_result[0], event_result[4])
    print(character_result)
    print(event_result)
    print(character_result)
    print(event_result)
    print(character_result)
    print(event_result)
    response =  response +  "```"
    return response


def statm(discord_client, playername, samplesizestart, samplesize):
    response = "```"

    # code here

    response = response + "```"
    return response


def statl(discord_client, playername, samplesizestart, samplesize):
    response = "```"

    # code here

    response = response + "```"
    return response
