


# Standard Modules
import time
import threading
import logging.config

# 3rd Party Modules


# Initialize Logging
logging.config.fileConfig('resources/logging.cfg')

from resources.discordClient import discord_client, get_token


def main():

    discord_client.run(get_token("resources/token.txt"))

if __name__ == '__main__':
    main()
