import discord
from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        """Deletes a specified number of messages (manage messages required)."""
        if not amount:
            await ctx.send("Please specify the number of messages to delete.")
            return

        if amount < 1 or amount > 100:
            await ctx.send("Please enter a number between 1 and 100!")
            return

        try:
            await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
            embed = discord.Embed(
                title="Purge Complete",
                description=f"Deleted {amount} messages.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed, delete_after=5)
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages in this channel.")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while purging messages: {e}")

    @purge.error
    async def purge_error(self, ctx, error):
        """Handles any errors that occur during the command execution."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to manage messages!")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify how many messages to delete!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide a valid number of messages to delete.")
        else:
            await ctx.send(f"An unexpected error occurred: {error}")

async def setup(bot):
    await bot.add_cog(Purge(bot))
