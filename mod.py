"""mod.py - file dealing with most of the moderator commands, such as kick, ban, etc."""
import io

import discord
from discord.ext import commands
from dotenv import dotenv_values
import json
import secrets
from collections import defaultdict

config = dotenv_values(".env")
TOKEN = config["DISCORD_TOKEN"]
PREFIX = config["PREFIX"]

MOD_CHANNEL = int(config["MOD_CHANNEL"])

WARNS_PATH = 'warns.json'
with open(WARNS_PATH) as j:
    warns = defaultdict(lambda: {}, json.load(j))


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
    async def warn(self, ctx, user: discord.Member, *reason) -> None:
        """
        Warns a user with an optional reason.
        <user>: id/username of user to warn
        <reason>: optional reason for warn
        """
        # await ctx.send(user.display_name)
        # await ctx.send(' '.join(reason) if len(reason) else 'none given')
        try:
            warn_id = secrets.token_hex(4)
            warns[user.id][warn_id] = reason
            with open(WARNS_PATH, 'w', encoding='utf-8') as f:
                json.dump(warns, f, ensure_ascii=False, indent=4)
            embed = discord.Embed(title=f":white_check_mark: {user.name} has been warned. (TESTING)")
            embed.add_field(name="Reason:", value=f"{' '.join(reason)}", inline=False)
            embed.add_field(name="ID:", value=f"{warn_id}")
            await ctx.send(embed=embed)
            await self.bot.get_channel(MOD_CHANNEL).send(
                f"User {user.display_name} was warned because of reason:\n```{' '.join(reason)}```"
            )
        except io.UnsupportedOperation:
            await ctx.send('ERROR: warns.json is not writable')
