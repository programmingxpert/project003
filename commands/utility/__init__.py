from discord.ext import commands

async def setup(bot):
    await bot.load_extension('commands.utility.invite')
    await bot.load_extension('commands.utility.ping')
    await bot.load_extension('commands.utility.uptime')