from discord.ext import commands

async def setup(bot):
    await bot.load_extension('commands.autoresponder.autoresponder')