import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite", help="Sends an invite link for the bot.")
    async def invite(self, ctx):
        embed = discord.Embed(title="Invite <BOT NAME>", description="Click the link below to invite <BOT NAME> to your server!", color=discord.Color.green())
        embed.add_field(name="Invite Link", value="[Click Here](https://your-invite-link-here)", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Invite(bot))