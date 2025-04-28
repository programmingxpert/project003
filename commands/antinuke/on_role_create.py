import discord
from discord.ext import commands

class OnRoleCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Detects role creation and takes action."""
        if role.guild is None:
          return

        guild = role.guild
        return await self.check_mass_action(guild.id, "recent_role_creates", guild.owner, self.mass_role_create_threshold, "role creation")

async def setup(bot):
    await bot.add_cog(OnRoleCreate(bot))