import datetime

import config


async def start(bot):
    """Initialise debugging features; run at start of script."""
    global file, channel
    dt = datetime.datetime.today()
    channel = await bot.get_channel(config.debug_channel_id)
    file = open(f"CS-MODBOT Logog-{dt.day}-{dt.month}-{dt.year}.log", "a")  # load log file on import into main


async def log(log):
    """Log a message to log file, console and log channel."""
    global file
    file.write(str(log))
    print(log)
    await channel.send(str(log))
