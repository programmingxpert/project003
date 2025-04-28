import discord
from discord.ext import commands

class AntinukeWhitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="whitelist")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def antinuke_whitelist(self, ctx, role: discord.Role):
        """Whitelists a role from Anti-Nuke triggers."""
        guild_id = ctx.guild.id
        if guild_id not in self.whitelisted_roles:
            self.whitelisted_roles[guild_id] = []

        if role.id in self.whitelisted_roles[guild_id]:
            await ctx.send(f"{role.name} is already whitelisted.")
            return

        self.whitelisted_roles[guild_id].append(role.id)
        await ctx.send(f"Whitelisted role {role.name} from Anti-Nuke triggers.")
async def setup(bot):
    await bot.add_cog(AntinukeWhitelist(bot))