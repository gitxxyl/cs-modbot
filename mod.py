"""mod.py - file dealing with most of the moderator commands, such as kick, ban, etc."""
import discord
from discord.ext import commands
from dotenv import dotenv_values
import json

config = dotenv_values(".env")
TOKEN = config["DISCORD_TOKEN"]
PREFIX = config["PREFIX"]

MOD_CHANNEL = int(config["MOD_CHANNEL"])
WARNS_PATH = 'warns.json'


class Mod(commands.Cog):
    """
    Cog that deals with the main mod commands, like
    purge, mute, ban, warn, kick, and etc.
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='purge')
    async def purge(self, ctx, amount: int) -> None:
        """
        Deletes messages from the channel that this command is run in.
        <amount>: number of messages to delete
        """
        if amount <= 0:
            await ctx.send("You can't delete a negative number of messages!")
            return
        try:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"Purged {amount} messages.", delete_after=2)
            await self.bot.get_channel(MOD_CHANNEL).send(
                f"User {ctx.author.name} has deleted {amount} messages in channel {ctx.channel.name}."
            )
        except discord.Forbidden:
            await ctx.send("ERROR: permissions missing.", delete_after=2)
            await ctx.send(f"Purged {amount} messages.", delete_after=2)
            await self.bot.get_channel(MOD_CHANNEL).send(
                f"User {ctx.author.nickname} attempted to delete {amount} messages in channel {ctx.channel.name}. "
                f"Action failed because of missing permissions."
            )
        except discord.HTTPException:
            await ctx.send("ERROR: messages could not be purged.", delete_after=2)
            await self.bot.get_channel(MOD_CHANNEL).send(
                f"User {ctx.author.nickname} attempted to delete {amount} messages in channel {ctx.channel.name}. "
                f"Action failed because of HTTPException."
            )

    @commands.command(name='warn')
    async def warn(self, ctx):
        pass
