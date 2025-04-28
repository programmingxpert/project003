import discord
from discord.ext import commands
import time

class OnChannelCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild_id = channel.guild.id
        if guild_id not in self.bot.recent_channel_creates:
            self.bot.recent_channel_creates[guild_id] = []
        self.bot.recent_channel_creates[guild_id].append(time.time())
        self.bot.recent_channel_creates[guild_id] = [t for t in self.bot.recent_channel_creates[guild_id] if t > time.time() - self.bot.time_window]
        if len(self.bot.recent_channel_creates[guild_id]) > self.bot.mass_channel_create_threshold:
            audit_logs = await channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create).flatten()
            if audit_logs:
                user = audit_logs[0].user
                await channel.guild.ban(user, reason="Mass channel creation detected")
                log_channel_id = self.bot.log_channel.get(guild_id)
                if log_channel_id:
                    log_channel = self.bot.get_channel(log_channel_id)
                    await log_channel.send(f"Banned {user} for mass channel creation.")

async def setup(bot):
    await bot.add_cog(OnChannelCreate(bot))