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



    response = response + "```"
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
