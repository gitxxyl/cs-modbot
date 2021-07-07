"""mod.py - file dealing with most of the moderator commands, such as kick, ban, etc."""
import discord
from discord.ext import commands
from dotenv import dotenv_values

config = dotenv_values(".env")
TOKEN = config["DISCORD_TOKEN"]
PREFIX = config["PREFIX"]

class Mod(commands.Cog):
    """
    Cog that deals with the main mod commands, like
    purge, mute, ban, warn, kick, and etc.
    """
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='purge')
    async def purge(self, ctx, number: int) -> None:
        """
        Deletes messages from the channel that this command is run in.
        <number>: number of messages to delete
        """
