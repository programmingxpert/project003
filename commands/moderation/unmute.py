import discord
from discord.ext import commands

class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unmute", help="Unmutes a member.")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        """Unmutes a member if they have been muted (manage roles required)."""
        
        # Check if the 'Muted' role exists
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            await ctx.send("The 'Muted' role does not exist in this server.")
            return
        
        # Check if the command issuer is trying to unmute themselves
        if member == ctx.author:
            await ctx.send("You cannot unmute yourself!")
            return
        
        # Check if the command issuer has a higher role than the member to unmute
        if not ctx.author.top_role > member.top_role:
            await ctx.send("You cannot unmute someone with a higher or equal role!")
            return
        
        # Check if the member is already unmuted (doesn't have the 'Muted' role)
        if mute_role not in member.roles:
            await ctx.send(f"{member.mention} is not muted!")
            return
        
        try:
            # Remove the 'Muted' role from the member
            await member.remove_roles(mute_role, reason=reason)
            embed = discord.Embed(
                title="Unmute",
                description=f"Unmuted {member.mention} | Reason: {reason or 'No reason provided'}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I do not have permission to unmute this user.")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while unmuting: {e}")

    @unmute.error
    async def unmute_error(self, ctx, error):
        """Handles errors for the unmute command."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to unmute members.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify the member to unmute.")
        else:
            await ctx.send(f"An unexpected error occurred: {error}")

async def setup(bot):
    await bot.add_cog(Unmute(bot))
