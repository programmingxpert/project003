from discord.ext import commands

async def setup(bot):
    await bot.load_extension('commands.moderation.kick')
    await bot.load_extension('commands.moderation.ban')
    await bot.load_extension('commands.moderation.unban')
    await bot.load_extension('commands.moderation.purge')
    await bot.load_extension('commands.moderation.mute')
    await bot.load_extension('commands.moderation.unmute')
    
