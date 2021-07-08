from discord.ext import commands

import config
import debug
from virusscanner import scanf


class Virus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg) -> None:
        if not msg.attachments:
            return
        for attachment in msg.attachments:
            if attachment.filename.split('.', 1)[1] in config.file_extensions_to_scan:
                await debug.log(f"Scanning file {attachment.filename} from {msg.author}")
                await msg.add_reaction("⌛")
                if await scanf(file=await attachment.to_file(), msg=msg):
                    await msg.channel.send(f"I smell malicious code... {msg.author.mention} is that you?")


    @commands.command()
    async def scan(self, ctx, url):
        pass

