"""Main.py - runs bot."""

# import external libraries
import discord
from discord.ext import commands
from dotenv import dotenv_values
from pretty_help import PrettyHelp

# import other classes
import debug
from viruscog import Virus
from mod import Mod

secrets = dotenv_values(".env")
TOKEN = secrets["DISCORD_TOKEN"]
PREFIX = secrets["PREFIX"]

# create bot object
intents = discord.Intents.default()
intents.members = True  # to access members
bot = commands.Bot(command_prefix=f"{PREFIX}",
                   help_command=PrettyHelp(color=discord.colour.Colour.blurple(),
                                           show_index=False,
                                           no_category="Commands"),
                   intents=intents,
                   case_insensitive=True)

debug.start(bot)
# add cogs here
bot.add_cog(Virus(bot))
bot.add_cog(Mod(bot))
bot.run(TOKEN)
