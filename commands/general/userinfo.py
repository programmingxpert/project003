import discord
from discord.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo")
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member = None):
        """Displays information about a user (defaults to sender)."""
        member = member or ctx.author
        embed = discord.Embed(
            title=f"{member.name}#{member.discriminator} Info",
            color=discord.Color.purple()
        )
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
        embed.add_field(name="Roles", value=", ".join([role.mention for role in member.roles[1:]]), inline=False)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfo(bot))