import discord
from discord.ext import commands
import datetime

class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="uptime")
    @commands.guild_only()
    async def uptime(self, ctx):
        """Shows the bot's uptime."""
        delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{hours}h {minutes}m {seconds}s"
        embed = discord.Embed(
            title="Bot Uptime",
            description=f"Uptime: {uptime_str}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    bot.launch_time = datetime.datetime.utcnow()  # Set bot launch time
    await bot.add_cog(Uptime(bot))