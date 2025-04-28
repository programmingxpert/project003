import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason="No reason provided"):
        """Kicks a member (kick members required)."""
        if not member:
            await ctx.send("Please mention a member to kick.")
            return
        
        if member == ctx.author:
            await ctx.send("You cannot kick yourself!")
            return

        if not ctx.author.top_role > member.top_role:
            await ctx.send("You cannot kick someone with a higher or equal role than you!")
            return
        
        try:
            await member.kick(reason=f"Kicked by {ctx.author} | Reason: {reason}")
            embed = discord.Embed(
                title="Member Kicked",
                description=f"{member.mention} has been kicked. Reason: {reason}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I don't have permission to kick this member!")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while kicking the member: {e}")

    @kick.error
    async def kick_error(self, ctx, error):
        """Handles any errors that occur during the command execution."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to kick members!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to mention a member to kick!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("I couldn't find the member you mentioned.")
        else:
            await ctx.send(f"An unexpected error occurred: {error}")

async def setup(bot):
    await bot.add_cog(Kick(bot))
