import discord
from discord.ext import commands

class AntinukeThreshold(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="threshold")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def antinuke_threshold(self, ctx, action: str, number: int = None):
      """Sets the threshold for mass actions"""
      #Correct names in this
      if action == "channel_create":
        self.mass_channel_create_threshold = number
      elif action == "channel_delete":
        self.mass_channel_delete_threshold = number
      elif action == "role_create":
        self.mass_role_create_threshold = number
      elif action == "role_delete":
        self.mass_ban_threshold = number
      elif action == "kick":
        self.mass_kick_threshold = number
      elif action == "spam":
        self.mass_spam_threshold = number
      elif action == "ping":
        self.mass_ping_threshold = number
      else:
        await ctx.send("Invalid action type.")
        return
      await ctx.send(f"Setting for {action} is {number}")

async def setup(bot):
    await bot.add_cog(AntinukeThreshold(bot))