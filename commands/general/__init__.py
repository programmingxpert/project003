from discord.ext import commands
from .help import HelpCommands  # Corrected import

async def setup(bot):
    try:
        await bot.add_cog(HelpCommands(bot))
        await bot.load_extension('commands.general.avatar')
        await bot.load_extension('commands.general.userinfo')
        await bot.load_extension('commands.general.say')
        await bot.load_extension('commands.general.serverinfo')
    except Exception as e:
        print(f"Failed to load extension: {e}")
