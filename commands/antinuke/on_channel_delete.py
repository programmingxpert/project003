import discord
from discord.ext import commands

class OnChannelDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Detects channel deletion and takes action."""
        if channel.guild is None:
          return

        guild = channel.guild
        return await self.check_mass_action(guild.id, "recent_channel_deletes", channel.guild.owner, self.mass_channel_delete_threshold, "channel deletion")

async def setup(bot):
    await bot.add_cog(OnChannelDelete(bot))