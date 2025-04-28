import discord
from discord.ext import commands

class OnRoleDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """Detects role deletion and takes action."""
        if role.guild is None:
          return

        guild = role.guild

        return await self.check_mass_action(guild.id, "recent_role_deletes", guild.owner, self.mass_role_delete_threshold, "role deletion")

async def setup(bot):
    await bot.add_cog(OnRoleDelete(bot))