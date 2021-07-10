"""
==============
**CS Mod Bot**
==============

This is a discord moderation bot made specifically for Coding Server in response to attacks by the British Empire.
It currently has the following features:
\t* Automatic virus scanning
\t* Message purging
\t* Warns and kicks

-------------------------------------------------------------------------------------------------------------------

Source code is privately available at `its GitHub repository <https://github.com/gitxxyl/cs-modbot>`_.
For support and questions, contact xxyl#9999 on discord.

Currently developed by:
    UnimpressedFish#2806\n
    xxyl#9999\n
    azazo#2752\n
    PythonRocks1234#5259\n
-------------------------------------------------------------------------------------------------------------------
\n\n\n
"""

# import external libraries
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pretty_help import PrettyHelp

# import other classes
import debug
from viruscog import Virus
from mod import Mod
import config

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = config.prefix


# create bot object
intents = discord.Intents.default()
# intents.members = True  # to access members
bot = commands.Bot(command_prefix=f"{PREFIX}",
                   help_command=PrettyHelp(color=discord.colour.Colour.blurple(),
                                           show_index=False,
                                           no_category="Commands"),
                   intents=intents,
                   case_insensitive=True)

if __name__ == '__main__':
    debug.start(bot)
    # add cogs here
    bot.add_cog(Virus(bot))
    bot.add_cog(Mod(bot))
    bot.run(TOKEN)
