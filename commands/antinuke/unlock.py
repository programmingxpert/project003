import discord
from discord.ext import commands

class Unlock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unlock", description="Unlocks the server")
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx):
        """Unlocks the server."""
        for channel in ctx.guild.channels:
            try:
                await channel.set_permissions(ctx.guild.default_role, send_messages=True, connect=True)
            except discord.Forbidden:
                continue
        await ctx.send("Unlocked the server. :unlock:")

async def setup(bot):
    await bot.add_cog(Unlock(bot))