import discord
from discord.ext import commands

class Setmuteduration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setmuteduration")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setmuteduration(self, ctx, duration: int):
        """Sets the mute duration for spam."""
        if duration > 0:
            self.bot.spam_mute_duration = duration
            await ctx.send(f"Mute duration set to {duration} seconds.")
        else:
            await ctx.send("Duration must be positive.")

async def setup(bot):
    await bot.add_cog(Setmuteduration(bot))