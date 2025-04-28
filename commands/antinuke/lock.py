import discord
from discord.ext import commands

class Lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lock", description="Locks the entire server down")
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx):
        """Locks the server down."""
        for channel in ctx.guild.channels:
            try:
                await channel.set_permissions(ctx.guild.default_role, send_messages=False, connect=False)
            except discord.Forbidden:
                continue
        await ctx.send("Locked down the server. :lock:")

async def setup(bot):
    await bot.add_cog(Lock(bot))