import discord
from discord.ext import commands

class OnMemberRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
      """Detects a ban and takes action."""
      if member.guild is None:
          return

      guild = member.guild

      return await self.check_mass_action(member.guild.id, "recent_kicks", member.guild.owner, self.mass_kick_threshold, "kick")

async def setup(bot):
    await bot.add_cog(OnMemberRemove(bot))