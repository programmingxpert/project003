import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import inspect
import random  # For selecting an aesthetic footer

load_dotenv()

prefix = os.getenv("BOT_PREFIX", ".")
invite_link = os.getenv("INVITE_LINK", "#")
support_server_link = os.getenv("SUPPORT_SERVER_LINK", "#")
terms_of_service_link = os.getenv("TERMS_OF_SERVICE_LINK", "#")
privacy_policy_link = os.getenv("PRIVACY_POLICY_LINK", "#")

EXCLUDED_COGS = ["Autoresponder"]  # Cogs to be excluded from help

if not prefix:
    print("⚠️ Warning: Prefix not set in .env file. Using default: '.'")
    prefix = "."

# List of aesthetic status messages (fully original)
aesthetic_status = [
    "✦ Status1",
    "❖ Status2"
]

class HelpDropdown(discord.ui.Select):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        options = []
        self.category_commands = {}
        categories_seen = {}
        
        # Loop through all cogs and exclude those in EXCLUDED_COGS
        for cog_name, cog in bot.cogs.items():
            if cog_name in EXCLUDED_COGS:
                continue
                
            try:
                cog_file_path = inspect.getfile(cog.__class__)
                category = os.path.basename(os.path.dirname(cog_file_path)).title()
                if category not in categories_seen:
                    options.append(discord.SelectOption(
                        label=f"✧ {category}",
                        value=category,
                        description=f"Show {category} commands"
                    ))
                    categories_seen[category] = True
                    self.category_commands[category] = []
                
                # Add non-hidden commands to the corresponding category
                for command in cog.get_commands():
                    if not command.hidden:
                        self.category_commands[category].append(command)
            except Exception as e:
                print(f"❌ Error accessing cog info for {cog_name}: {e}")
        
        if not options:
            options.append(discord.SelectOption(
                label="🚫 No Commands", value="none", description="No commands available."
            ))
        super().__init__(placeholder="Select a category...", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        if category == "none":
            embed = discord.Embed(
                title="🚫 No Commands",
                description="Currently, no commands have been loaded.",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed)
            return
        
        commands_in_category = self.category_commands[category]
        embed = discord.Embed(
            title=f"≋ {category} Commands", 
            color=0x3498db
        )
        if not commands_in_category:
            embed.description = "This category doesn't have any commands."
        else:
            command_desc = [
                f"• `{prefix}{command.name} {command.signature}` — {command.help or 'No details provided.'}"
                for command in commands_in_category
            ]
            embed.description = "\n".join(command_desc)
        # Add a random aesthetic footer message
        embed.set_footer(text=random.choice(aesthetic_status))
        await interaction.response.edit_message(embed=embed)

class InviteButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="➤ Invite Bot",
            style=discord.ButtonStyle.link,
            url=invite_link
        )

class SupportButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="✦ Support Server",
            style=discord.ButtonStyle.link,
            url=support_server_link
        )

class TermsButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="❖ Terms of Service",
            style=discord.ButtonStyle.link,
            url=terms_of_service_link
        )

class PrivacyButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="⊹ Privacy Policy",
            style=discord.ButtonStyle.link,
            url=privacy_policy_link
        )

class HelpView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.add_item(HelpDropdown(bot))
        self.add_item(InviteButton())
        self.add_item(SupportButton())
        self.add_item(TermsButton())
        self.add_item(PrivacyButton())

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", help="Displays this help menu.")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="✧ Command Hub",
            color=discord.Color.blurple()
        )
        embed.description = (
            "Welcome to the help interface!\n\n"
            "Use the dropdown below to browse through command categories.\n"
            "If you need extra support, please use the provided links."
        )
        embed.add_field(name="• Active Prefix", value=f"`{prefix}`", inline=False)
        embed.add_field(name="• Status", value="✅ Fully operational", inline=False)
        # Set a random aesthetic footer message
        embed.set_footer(text=random.choice(aesthetic_status))
        await ctx.send(embed=embed, view=HelpView(self.bot))

async def setup(bot):
    await bot.add_cog(HelpCommands(bot))
