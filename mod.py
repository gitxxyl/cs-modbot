"""
**mod.py**\n

Cog for moderation related commands and listeners - such as warn, kick and purge.\n
|
"""
import io
from typing import Union
import json
from collections import defaultdict
import secrets
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = config.prefix

MOD_CHANNEL = config.debug_channel_id

WARNS_PATH = 'warns.json'
with open(WARNS_PATH) as j:
    warns = defaultdict(lambda: defaultdict(lambda: []), json.load(j))
    # print(type(warns))

class Mod(commands.Cog):
    """
    Cog that deals with the main mod commands, like
    purge, mute, ban, warn, kick, and etc.\n
    |
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_message(self, ctx) -> None:
    #     if not ctx.author.guild_permissions.administrator:
    #         await ctx.send("Sorry, you don't have the permissions to do this!")
    #         return
    #     await self.bot.process_commands(ctx)

    @commands.has_permissions(administrator=True)
    @commands.command(name='purge')
    async def purge(self, ctx, amount: int, mode: str = None,
                    param: Union[discord.Member, str] = None) -> None:
        """
        Deletes messages from the channel that this command is run in.
        <amount>: number of messages to delete
        === MODES ===
        all: no check is applied
        from: deletes messages from a user only
        with: deletes messages containing a phrase
        === OPTIONAL ===
        [mode]: mode of purging messages. must be one of all, from, with
        [param]: if mode is from, param should be id/username/mention of a user.
                 if mode is with, param should be a string in quotes containing the phrase.\n
        |
        """
        if not param and mode:
            await ctx.send("You must specify a user or message to purge!")
            return
        def purge_check(msg):
            """
            Checks if a message is under the purge request.
            Called on discord.Channel.purge.\n
            |
            """
            if mode[0] == "f":
                return msg.author == param
            if mode[0] == "w":
                return param in msg.content
            return True

        if mode not in [None, "all", "from", "with", "a", "f", "w"]:  # validate mode input
            await ctx.send(f"Mode {mode} does not exist!")
            return
        if mode is None:  # set default
            mode = "d"
        mode = mode[0]
        if amount <= 0:  # negative no. of msgs
            await ctx.send("You can't delete a negative number of messages!")
            return
        try:
            await ctx.message.delete()
            msg_list = []
            async for msg in ctx.channel.history():
                if len(msg_list) == amount: # we have enough messages alr
                    break
                if purge_check(msg): # if message fits requirement
                    msg_list.append(msg) # add message to list
            await ctx.channel.delete_messages(msg_list) # delete all messages in list
            # purge amt+1 msgs with purge_check
            # await ctx.channel.purge(limit=amount, check=purge_check)
            await ctx.send(f"Purged {amount} messages.", delete_after=2)
            await self.bot.get_channel(MOD_CHANNEL).send(
                f"User {ctx.author.name} has deleted {amount} messages"
                f"in channel {ctx.channel.name}."
            )

        except discord.Forbidden:  # bot doesn't have deleting permissions
            # debug.log(e)
            await ctx.send("ERROR: permissions missing.", delete_after=2)
            await ctx.send(f"Purged {amount} messages.", delete_after=2)
            await self.bot.get_channel(MOD_CHANNEL).send(
                f"User {ctx.author.nickname} attempted to delete "
                f"{amount} messages in channel {ctx.channel.name}. "
                f"Action failed because of missing permissions."
            )
        except discord.HTTPException:  # misc discord exception
            # debug.log(e)
            await ctx.send("ERROR: messages could not be purged.", delete_after=2)
            await self.bot.get_channel(MOD_CHANNEL).send(
                f"User {ctx.author.nickname} attempted to delete "
                f"{amount} messages in channel {ctx.channel.name}. "
                f"Action failed because of HTTPException."
            )

    @purge.error
    async def purge_error(self, ctx, err):
        """
        :param ctx:
        :param err:
        :return:

        Deals with errors where user does not have admin permissions.\n
        |
        """
        if isinstance(err, commands.MissingPermissions):
            print("missing admin perms")
            await ctx.send("You don't have the permission to do this!")

    @commands.has_permissions(administrator=True)
    @commands.command(name='warn')
    async def warn(self, ctx, user: discord.Member, *reason) -> None:
        """
        Warns a user with an optional reason.
        <user>: id/username of user to warn
        === OPTIONAL ===
        [reason]: reason for warn\n
        |
        """
        # await ctx.send(user.display_name)
        # await ctx.send(' '.join(reason) if len(reason) else 'none given')
        try:
            warn_id = secrets.token_hex(4)
            warns[user.id][warn_id].append(reason)
            with open(WARNS_PATH, 'w',
                      encoding='utf-8') as file:
                json.dump(warns, file, ensure_ascii=False, indent=4)
            embed = discord.Embed(title=f":white_check_mark: {user.name} has been warned.")
            embed.add_field(name="Reason:", value=f"{' '.join(reason)}", inline=False)
            embed.add_field(name="ID:", value=f"{warn_id}")
            await ctx.send(embed=embed)
            await self.bot.get_channel(MOD_CHANNEL).send(
                f"User {user.display_name} was warned because of reason:\n```{' '.join(reason)}```"
            )
        except io.UnsupportedOperation:
            await ctx.send('ERROR: warns.json is not writable')

    @warn.error
    async def warn_error(self, ctx, err):
        """
        :param ctx:
        :param err:
        :return:

        Deals with errors where user does not have admin permissions\n
        |
        """
        if isinstance(err, commands.MissingPermissions):
            print("missing admin perms")
            await ctx.send("You don't have the permission to do this!")
    # optional function to check if message author has admin perms
    # @staticmethod
    # async def is_mod(ctx):
    #     return bool(ctx.author.server_permissions.administrator)
