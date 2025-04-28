import discord
from discord.ext import commands

class Antinuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = {}  # Temporary storage for log channels

    @commands.group(name="antinuke", invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def antinuke(self, ctx):
        """Base antinuke command. Use subcommands like .antinuke setlogchannel."""
        await ctx.send("Available subcommands: setlogchannel, threshold, whitelist, etc.")

    @antinuke.command(name="setlogchannel")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setlogchannel(self, ctx, channel: discord.TextChannel = None):
        """Sets the antinuke log channel."""
        guild_id = ctx.guild.id
        if channel is None:
            self.log_channel[guild_id] = None
            await ctx.send("Antinuke log channel disabled.")
        else:
            # Check if the bot can send messages in the channel
            if not channel.permissions_for(ctx.guild.me).send_messages:
                await ctx.send(f"I don’t have permission to send messages in {channel.mention}.")
                return
            self.log_channel[guild_id] = channel.id
            await ctx.send(f"Antinuke log channel set to: {channel.mention}")

async def setup(bot):
    await bot.add_cog(Antinuke(bot))