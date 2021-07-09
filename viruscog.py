from discord.ext import commands
import discord

import config
import debug
from virusscanner import scanf


class Virus(commands.Cog):
    """
    Cog for antivirus features.
    Contains a message listener to scan attachments automatically.
    Instance of commands.Cog.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message) -> None:
        """
        Checks for attachments on every message to scan appropriate files.
        :param msg: Message to be checked and scanned.
        :type msg: discord.Message
        :return: None
        :rtype: None
        """
        if not msg.attachments:
            return
        for attachment in msg.attachments:
            if attachment.filename.split('.', 1)[1] in config.file_extensions_to_scan:
                await debug.log(f"Scanning file {attachment.filename} from {msg.author}")
                await msg.add_reaction("⌛")
                if await scanf(file=await attachment.to_file(), msg=msg):
                    await msg.channel.send(f"I smell malicious code... {msg.author.mention} is that you?")
