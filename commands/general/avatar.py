import discord
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="avatar")
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = None):
        """Shows a user's avatar (defaults to sender)."""
        member = member or ctx.author
        embed = discord.Embed(
            title=f"{member.name}#{member.discriminator}'s Avatar",
            color=discord.Color.green()
        )
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Avatar(bot))