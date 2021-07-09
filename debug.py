import datetime
from discord.ext import commands

import config


def start(client: commands.Bot) -> None:
    """
    Initialise debugging features; run at start of script.

    :param client: Discord bot to send log messages from.
    :type client: commands.Bot

    :return: None
    :rtype: None

    |
    """
    global file, bot
    bot = client
    dt = datetime.datetime.today()
    # load log_message file on start
    file = open(f"CS-MODBOT Log-{dt.day}-{dt.month}-{dt.year}.log_message", "a")


async def log(log_message: str) -> None:
    """
    Log a message to log_message file, console and log_message channel.

    :param log_message: Message to be logged.
    :type log_message: str

    :return: None
    :rtype: None \n
    |
    """
    global file
    channel = bot.get_channel(config.debug_channel_id)
    file.write(log_message)
    print(log_message)
    await channel.send(log_message)
