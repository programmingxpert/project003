import discord
from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
      """Check message spam and mention spam"""
      if message.guild is None:
          return

      guild = message.guild

      # await self.check_mass_action(message.guild.id, "recent_messages", message.author, self.mass_spam_threshold, "spam") Remove self
      # Check number of mentions in massping
      #if len(message.mentions) > 5: remove all this functions too
      return #await self.check_mass_action(message.guild.id, "recent_pings", message.author, self.mass_ping_threshold, "mass ping")

async def setup(bot):
    await bot.add_cog(OnMessage(bot))