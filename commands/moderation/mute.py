import discord
from discord.ext import commands

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute", help="Mutes a member.")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason="No reason provided"):
        """Mutes a member (manage roles permission required)."""
        if not member:
            await ctx.send("Please mention a member to mute.")
            return

        if member == ctx.author:
            await ctx.send("You cannot mute yourself!")
            return

        if not ctx.author.top_role > member.top_role:
            await ctx.send("You cannot mute someone with a higher or equal role than you!")
            return

        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted", reason="Auto-created for mute command")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)
        
        try:
            await member.add_roles(mute_role, reason=reason)
            embed = discord.Embed(
                title="Mute",
                description=f"{member.mention} has been muted. Reason: {reason}",
                color=discord.Color.greyple()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I don't have permission to mute this member!")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while muting the member: {e}")

    @mute.error
    async def mute_error(self, ctx, error):
        """Handles any errors that occur during the command execution."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to manage roles!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to mention a member to mute!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("I couldn't find the member you mentioned.")
        else:
            await ctx.send(f"An unexpected error occurred: {error}")

async def setup(bot):
    await bot.add_cog(Mute(bot))
