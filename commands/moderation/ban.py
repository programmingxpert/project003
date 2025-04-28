import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason="No reason provided"):
        """Bans a member (ban members required)."""
        if not member:
            await ctx.send("Please mention a member to ban.")
            return
        
        if member == ctx.author:
            await ctx.send("You cannot ban yourself!")
            return

        if not ctx.author.top_role > member.top_role:
            await ctx.send("You cannot ban someone with a higher or equal role than you!")
            return
        
        try:
            await member.ban(reason=f"Banned by {ctx.author} | Reason: {reason}")
            embed = discord.Embed(
                title="Member Banned",
                description=f"{member.mention} has been banned. Reason: {reason}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I don't have permission to ban this member!")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while banning the member: {e}")

    @ban.error
    async def ban_error(self, ctx, error):
        """Handles any errors that occur during the command execution."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to ban members!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to mention a member to ban!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("I couldn't find the member you mentioned.")
        else:
            await ctx.send(f"An unexpected error occurred: {error}")

async def setup(bot):
    await bot.add_cog(Ban(bot))
