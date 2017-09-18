from collections import namedtuple
import asyncio
import logging
import json

# 3rd Party Modules
import discord
import resources.stat as stat


# Bot Prefix
prefix = "!!"

logger = logging.getLogger(__name__)

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
        userIn = message.content.split(" ")
        tmp = await discord_client.send_message(message.channel, "Getting stats")
        await discord_client.send_typing(message.channel)
        name = userIn[1]
        try:
            sampleSizeStart = message.content.split(" ")[3]
            sampleSize = message.content.split(" ")[2]
        except IndexError:
            try:
                sampleSize = message.content.split(" ")[2]
                sampleSizeStart = '0'
            except IndexError:
                sampleSize = '1000'
                sampleSizeStart = '0'
        try:
            response = stat.stats(discord_client, name, sampleSizeStart, sampleSize)
            await discord_client.edit_message(tmp, response)

        except:
            await discord_client.edit_message(tmp, "Error getting stats")
            raise

    if message.content.startswith(prefix + 'statm'):
        userIn = message.content.split(" ")
        tmp = await discord_client.send_message(message.channel, "Getting stats")
        await discord_client.send_typing(message.channel)
        name = userIn[1]
        try:
            sampleSizeStart = message.content.split(" ")[3]
            sampleSize = message.content.split(" ")[2]
        except IndexError:
            try:
                sampleSize = message.content.split(" ")[2]
                sampleSizeStart = '0'
            except IndexError:
                sampleSize = '1000'
                sampleSizeStart = '0'
        try:
            response = stat.statm(discord_client, name, sampleSizeStart, sampleSize)
            print(response)
            await discord_client.edit_message(tmp, response)

        except:
            await discord_client.edit_message(tmp, "Error getting stats")
            raise





    elif message.content.startswith('!help'):
        await discord_client.send_message(message.channel,
                                          "<@" + message.author.id + "> I have sent my commands in a PM")
        response = help_response('resources/commands.json')

        await discord_client.send_message(message.author, response)