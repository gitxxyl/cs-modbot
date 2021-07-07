from discord.ext import commands
from virusscanner import scanf


class Virus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg) -> None:
        if not msg.attachments:
            print("no attachments")
            return
        await msg.add_reaction("⌛")
        for attachment in msg.attachments:
            await scanf(file=await attachment.to_file(), msg=msg)


    @commands.command()
    async def scan(self, ctx, url):
        pass

