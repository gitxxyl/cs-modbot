"""Main.py - runs bot."""
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pretty_help import PrettyHelp

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX")

# create bot object
intents = discord.Intents.default()
intents.members = True  # to access members
bot = commands.Bot(command_prefix=f"{PREFIX}",
                   help_command=PrettyHelp(color=discord.colour.Colour.blurple(),
                                           show_index=False,
                                           no_category="Commands"),
                   intents=intents,
                   case_insensitive=True)
# add cogs here
bot.run(TOKEN)
