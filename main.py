import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

BOT_PREFIX = "."
bot = commands.Bot(command_prefix=commands.when_mentioned_or(BOT_PREFIX), intents=intents)

# Custom Help Command
class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        # Remove 'autoresponder' category from the mapping
        if "Autoresponder" in mapping:
            del mapping["Autoresponder"]
        
        # Proceed with default help command functionality
        await super().send_bot_help(mapping)

bot.help_command = CustomHelpCommand()

async def load_commands():
    for category in os.listdir('./commands'):
        init_path = f'./commands/{category}/__init__.py'
        
        if os.path.isdir(f'./commands/{category}') and os.path.exists(init_path):
            try:
                await bot.load_extension(f'commands.{category}')
                print(f'Loaded category {category}')
            except Exception as e:
                print(f'Failed to load category {category}')
                import traceback
                traceback.print_exc()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    bot.remove_command("help")
    await load_commands()

async def main():
    async with bot:
        await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
