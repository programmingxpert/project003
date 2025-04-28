import discord
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, message):
        """Makes the bot say something (manage messages required)."""
        await ctx.message.delete()
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Say(bot))