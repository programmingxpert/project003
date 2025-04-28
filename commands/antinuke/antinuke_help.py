import discord
from discord.ext import commands

class AntinukeHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="antinuke_help")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def antinuke_help(self, ctx):
        """Shows available AntiNuke commands."""
        embed = discord.Embed(title="AntiNuke Commands", color=discord.Color.blue())
        embed.add_field(name="`.antinuke_help`", value="Shows this help message.", inline=False)
        embed.add_field(name="`.setlogchannel <channel>`", value="Sets the antinuke log channel.", inline=False)
        embed.add_field(name="`.lock`", value="Locks the server down.", inline=False)
        embed.add_field(name="`.unlock`", value="Unlocks the server.", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AntinukeHelp(bot))