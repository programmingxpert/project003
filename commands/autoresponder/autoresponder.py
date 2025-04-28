import discord
from discord.ext import commands

class Autoresponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = {
            "hello": "Hi there! How can I help you today?",
            "goodbye": "See you later! Take care!",
            "bot": "Yes, I’m a bot! Powered by xAI. 😄",
            "thanks": "You’re welcome! Glad to help!"
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        content = message.content.lower()
        if any(trigger in content for trigger in self.responses):
            response = self.responses.get(content.split()[0], "Sorry, I didn’t get that!")
            await message.channel.send(response)

async def setup(bot):
    await bot.add_cog(Autoresponder(bot))