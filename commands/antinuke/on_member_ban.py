import discord
from discord.ext import commands

class OnMemberBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Detects a ban and takes action."""
        if guild is None:
          return
        return await self.check_mass_action(guild.id, "recent_bans", guild.owner, self.mass_ban_threshold, "ban")

async def setup(bot):
    await bot.add_cog(OnMemberBan(bot))