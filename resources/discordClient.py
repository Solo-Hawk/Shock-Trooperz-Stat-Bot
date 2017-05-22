

from collections import namedtuple
import asyncio
import logging
import json
prefix = "!!"
logger = logging.getLogger(__name__)

# 3rd Party Modules
import discord
from stat import stat

discord_client = discord.Client()

def get_token(file):

    with open(file, 'r') as f:
        password = f.read()

    return password


def help_response(file):
    response = "```"
    with open(file) as json_data:
        cjson = json.load(json_data)

    # todo improve / reduce code
    for x in range(len(cjson['commands'])):
        response = response + "Command : " + cjson['commands'][x]['command'] + '\n' + \
                   "Argument : " + cjson['commands'][x]['arguments'] + '\n' + \
                   "Description : " + cjson['commands'][x]['description'] + '\n \n'

    return response + "```"


@discord_client.event
async def on_ready():
    logger.debug(discord_client.user.name)
    logger.debug(discord_client.user.id)
    logger.debug('------')



@discord_client.event
async def on_member_join(member):

    logger.info("Member Joined", member)
    server = member.server

    msg = 'Welcome {0.mention} to Shock Trooperszzzzzzzzzzz MLG Discord, we do stuff and stuff and stuff, ' \
          'If you are cancer we have a channel for that, ' \
          'if you want a GIT GUD we have a channel for that, ' \
          'if you want to be extemely tactical we also have a channel for that, ' \
          'HAVE FUN AND WELCOME TO SHOCK TROOPERZ'
    await discord_client.send_message(server, msg.format(member, server))

@discord_client.event
async def on_message(message):
    if message.content.startswith(prefix + 'stats'):
        userSend = message.content.split(" ")
        name = userSend[1]
        try:
            sample = userSend[2]
        except IndexError:
            sample = 1000
        try:
            response = stat.stats(discord_client, name, sample)
            await discord_client.send_message(message.channel, response)

        except:
            await discord_client.send_message(message.channel, "Error getting stats")
            raise

    elif message.content.startswith('!help'):
        await discord_client.send_message(message.channel,
                                          "<@" + message.author.id + "> I have sent my commands in a PM")
        response = help_response('resources/commands.json')

        await discord_client.send_message(message.author, response)