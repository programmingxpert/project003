import discord
from discord.ext import commands
import time
from discord.ui import Select, View, Button

class AntinukeSettingsSelect(Select):
    def __init__(self, bot, cog, admin_id):
        self.bot = bot
        self.cog = cog
        self.admin_id = admin_id
        options = [
            discord.SelectOption(label="Set Log Channel", description="Choose a channel for AntiNuke alerts"),
            discord.SelectOption(label="Toggle Auto-Mute", description="Enable or disable auto-muting spammers"),
            discord.SelectOption(label="Set Mute Duration", description="Adjust the auto-mute time"),
            discord.SelectOption(label="Whitelist Role", description="Add a role to ignore"),
            discord.SelectOption(label="Remove Whitelist Role", description="Remove a role from ignore list"),
            discord.SelectOption(label="Toggle Mass Ban Protection", description="Enable/disable mass ban detection"),
            discord.SelectOption(label="Toggle Mass Kick Protection", description="Enable/disable mass kick detection"),
            discord.SelectOption(label="Toggle Mass Ping Protection", description="Enable/disable mass ping detection"),
            discord.SelectOption(label="Toggle Spam Protection", description="Enable/disable spam detection"),
            discord.SelectOption(label="Mass Ban", description="Ban multiple users"),
            discord.SelectOption(label="Mass Kick", description="Kick multiple users"),
            discord.SelectOption(label="View Status", description="Check current settings"),
        ]
        super().__init__(placeholder="Select an action...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.admin_id:
            await interaction.response.send_message("You are not authorized to use this panel!", ephemeral=True)
            return
        guild_id = interaction.guild.id
        selection = self.values[0]
        if selection == "Set Log Channel":
            await interaction.response.send_message("Please mention a channel (e.g., #logs) to set as the log channel.", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            try:
                message = await self.bot.wait_for("message", check=check, timeout=30.0)
                channel = message.channel_mentions[0] if message.channel_mentions else None
                if channel and channel.permissions_for(interaction.guild.me).send_messages:
                    self.cog.log_channel[guild_id] = channel.id
                    await interaction.followup.send(f"Log channel set to {channel.mention}.", ephemeral=True)
                    await channel.send("AntiNuke is now active! Alerts will appear here.")
                else:
                    await interaction.followup.send("Invalid channel or I lack permissions!", ephemeral=True)
            except:
                await interaction.followup.send("Timeout! Please try again.", ephemeral=True)

        elif selection == "Toggle Auto-Mute":
            self.cog.auto_mute_enabled[guild_id] = not self.cog.auto_mute_enabled.get(guild_id, False)
            status = "enabled" if self.cog.auto_mute_enabled[guild_id] else "disabled"
            await interaction.response.send_message(f"Auto-mute is now {status}.", ephemeral=True)

        elif selection == "Set Mute Duration":
            await interaction.response.send_message("Enter duration in seconds (e.g., 300 for 5 mins).", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            try:
                message = await self.bot.wait_for("message", check=check, timeout=30.0)
                duration = int(message.content)
                if duration > 0:
                    self.cog.mute_duration = duration
                    await interaction.followup.send(f"Mute duration set to {duration} seconds.", ephemeral=True)
                else:
                    await interaction.followup.send("Duration must be positive!", ephemeral=True)
            except:
                await interaction.followup.send("Invalid input or timeout!", ephemeral=True)

        elif selection == "Whitelist Role":
            await interaction.response.send_message("Mention a role to whitelist (e.g., @Role).", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            try:
                message = await self.bot.wait_for("message", check=check, timeout=30.0)
                role = message.role_mentions[0] if message.role_mentions else None
                if role:
                    if guild_id not in self.cog.whitelisted_roles:
                        self.cog.whitelisted_roles[guild_id] = set()
                    self.cog.whitelisted_roles[guild_id].add(role.id)
                    await interaction.followup.send(f"{role.mention} whitelisted from AntiNuke.", ephemeral=True)
                else:
                    await interaction.followup.send("Invalid role!", ephemeral=True)
            except:
                await interaction.followup.send("Timeout or error! Try again.", ephemeral=True)

        elif selection == "Remove Whitelist Role":
            await interaction.response.send_message("Mention a role to remove from whitelist (e.g., @Role).", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            try:
                message = await self.bot.wait_for("message", check=check, timeout=30.0)
                role = message.role_mentions[0] if message.role_mentions else None
                if role and guild_id in self.cog.whitelisted_roles and role.id in self.cog.whitelisted_roles[guild_id]:
                    self.cog.whitelisted_roles[guild_id].remove(role.id)
                    await interaction.followup.send(f"{role.mention} removed from whitelist.", ephemeral=True)
                else:
                    await interaction.followup.send("Role not whitelisted or invalid!", ephemeral=True)
            except:
                await interaction.followup.send("Timeout or error! Try again.", ephemeral=True)

        elif selection == "Toggle Mass Ban Protection":
            self.cog.protections[guild_id] = self.cog.protections.get(guild_id, {})
            self.cog.protections[guild_id]["mass_ban"] = not self.cog.protections.get(guild_id, {}).get("mass_ban", True)
            status = "enabled" if self.cog.protections[guild_id]["mass_ban"] else "disabled"
            await interaction.response.send_message(f"Mass ban protection is now {status}.", ephemeral=True)

        elif selection == "Toggle Mass Kick Protection":
            self.cog.protections[guild_id] = self.cog.protections.get(guild_id, {})
            self.cog.protections[guild_id]["mass_kick"] = not self.cog.protections.get(guild_id, {}).get("mass_kick", True)
            status = "enabled" if self.cog.protections[guild_id]["mass_kick"] else "disabled"
            await interaction.response.send_message(f"Mass kick protection is now {status}.", ephemeral=True)

        elif selection == "Toggle Mass Ping Protection":
            self.cog.protections[guild_id] = self.cog.protections.get(guild_id, {})
            self.cog.protections[guild_id]["mass_ping"] = not self.cog.protections.get(guild_id, {}).get("mass_ping", True)
            status = "enabled" if self.cog.protections[guild_id]["mass_ping"] else "disabled"
            await interaction.response.send_message(f"Mass ping protection is now {status}.", ephemeral=True)

        elif selection == "Toggle Spam Protection":
            self.cog.protections[guild_id] = self.cog.protections.get(guild_id, {})
            self.cog.protections[guild_id]["spam"] = not self.cog.protections.get(guild_id, {}).get("spam", True)
            status = "enabled" if self.cog.protections[guild_id]["spam"] else "disabled"
            await interaction.response.send_message(f"Spam protection is now {status}.", ephemeral=True)

        elif selection == "Mass Ban":
            await interaction.response.send_message("Mention users to ban (e.g., @user1 @user2) and provide a reason.", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            try:
                message = await self.bot.wait_for("message", check=check, timeout=60.0)
                users = message.mentions
                split_content = message.content.split()
                reason = " ".join(split_content[len(users):]) or "Mass ban by admin"

                if users:
                    for user in users:
                        if not any(role.id in self.cog.whitelisted_roles.get(guild_id, set()) for role in user.roles):
                            await interaction.guild.ban(user, reason=reason)
                    log_channel_id = self.cog.log_channel.get(guild_id)
                    if log_channel_id:
                        log_channel = self.bot.get_channel(log_channel_id)
                        await log_channel.send(f"🚫 Mass banned {len(users)} users: {', '.join(u.mention for u in users)} | Reason: {reason}")
                    await interaction.followup.send(f"Mass banned {len(users)} users.", ephemeral=True)
                else:
                    await interaction.followup.send("No users mentioned!", ephemeral=True)
            except:
                await interaction.followup.send("Timeout or error! Try again.", ephemeral=True)

        elif selection == "Mass Kick":
            await interaction.response.send_message("Mention users to kick (e.g., @user1 @user2) and provide a reason.", ephemeral=True)
            def check(m):
                return m.author == interaction.user and m.channel == interaction.channel
            try:
                message = await self.bot.wait_for("message", check=check, timeout=60.0)
                users = message.mentions
                split_content = message.content.split()
                reason = " ".join(split_content[len(users):]) or "Mass kick by admin"

                if users:
                    for user in users:
                        if not any(role.id in self.cog.whitelisted_roles.get(guild_id, set()) for role in user.roles):
                            await interaction.guild.kick(user, reason=reason)
                    log_channel_id = self.cog.log_channel.get(guild_id)
                    if log_channel_id:
                        log_channel = self.bot.get_channel(log_channel_id)
                        await log_channel.send(f"👢 Mass kicked {len(users)} users: {', '.join(u.mention for u in users)} | Reason: {reason}")
                    await interaction.followup.send(f"Mass kicked {len(users)} users.", ephemeral=True)
                else:
                    await interaction.followup.send("No users mentioned!", ephemeral=True)
            except:
                await interaction.followup.send("Timeout or error! Try again.", ephemeral=True)

        elif selection == "View Status":
            log_channel = self.cog.log_channel.get(guild_id)
            auto_mute = self.cog.auto_mute_enabled.get(guild_id, False)
            locked = self.cog.locked_status.get(guild_id, False)
            protections = self.cog.protections.get(guild_id, {})
            embed = discord.Embed(
                title="AntiNuke Status",
                color=discord.Color.blue()
            )
            embed.add_field(name="Log Channel", value=f"{self.bot.get_channel(log_channel).mention if log_channel else 'Not set'}", inline=True)
            embed.add_field(name="Auto-Mute", value=f"{'Enabled' if auto_mute else 'Disabled'} (Duration: {self.cog.mute_duration // 60} mins)", inline=True)
            embed.add_field(name="Server Locked", value=f"{'Yes' if locked else 'No'}", inline=True)
            embed.add_field(name="Protections", value="\n".join([
                f"Spam: {'Enabled' if protections.get('spam', True) else 'Disabled'}",
                f"Mass Ban: {'Enabled' if protections.get('mass_ban', True) else 'Disabled'}",
                f"Mass Kick: {'Enabled' if protections.get('mass_kick', True) else 'Disabled'}",
                f"Mass Ping: {'Enabled' if protections.get('mass_ping', True) else 'Disabled'}"
            ]), inline=False)
            embed.add_field(name="Thresholds", value="\n".join([f"{k.replace('_', ' ').title()}: {v}" for k, v in self.cog.thresholds.items()]), inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

class AntinukeMenu(View):
    def __init__(self, bot, cog, admin_id):
        super().__init__(timeout=None)
        self.add_item(AntinukeSettingsSelect(bot, cog, admin_id))

class AntiNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.whitelisted_roles = {}  # Store whitelisted roles per guild
        self.log_channel = {}        # Store antinuke log channel per guild
        self.locked_status = {}      # Track if server is locked per guild
        self.mute_duration = 600     # Default automute duration (10 minutes) in seconds
        self.auto_mute_enabled = {}  # Track if automute is enabled per guild
        self.protections = {}        # Track enabled protections per guild

        # Customizable thresholds for mass actions (default values)
        self.thresholds = {
            "channel_create": 5,
            "channel_delete": 5,
            "role_create": 3,
            "role_delete": 3,
            "ban": 3,
            "kick": 5,
            "spam": 10,
            "ping": 10
        }

        # Time window for mass action detection (in seconds)
        self.time_window = 10

        # Caching recent actions for rate limiting
        self.recent_actions = {
            "channel_create": {},
            "channel_delete": {},
            "role_create": {},
            "role_delete": {},
            "ban": {},
            "kick": {},
            "spam": {},
            "ping": {}
        }

    @commands.command(name="antinuke", aliases=["an"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def antinuke(self, ctx):
        """Open the AntiNuke control menu to protect your server!"""
        guild_id = ctx.guild.id
        auto_mute = self.auto_mute_enabled.get(guild_id, False)
        protections = self.protections.get(guild_id, {})
        enabled_features = (
            f"Auto-Mute: {u'✅' if auto_mute else u'❌'}\n"
            f"Spam Protection: {u'✅' if protections.get('spam', True) else u'❌'}\n"
            f"Mass Ban Protection: {u'✅' if protections.get('mass_ban', True) else u'❌'}\n"
            f"Mass Kick Protection: {u'✅' if protections.get('mass_kick', True) else u'❌'}\n"
            f"Mass Ping Protection: {u'✅' if protections.get('mass_ping', True) else u'❌'}"
        )
        embed = discord.Embed(
            title="AntiNuke Control Panel",
            description=f"Welcome to AntiNuke! Use the dropdown below to configure protection, ban/kick users, or check status.\n\n**Enabled Features:**\n{enabled_features}",
            color=discord.Color.dark_purple()
        )
        embed.add_field(
            name="Features",
            value="Raid detection, mass ban/kick, auto-mute, mass ping protection, and more!",
            inline=False
        )
        await ctx.send(embed=embed, view=AntinukeMenu(self.bot, self, ctx.author.id))

    @commands.command(name="setlogchannel")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setlogchannel(self, ctx, channel: discord.TextChannel = None):
        """Sets or disables the channel for AntiNuke alerts."""
        guild_id = ctx.guild.id
        if channel is None:
            self.log_channel[guild_id] = None
            await ctx.send("AntiNuke alerts disabled. Use `.setlogchannel #channel` to re-enable.")
        else:
            if not channel.permissions_for(ctx.guild.me).send_messages:
                await ctx.send(f"I can’t send messages in {channel.mention}. Please check permissions!")
                return
            self.log_channel[guild_id] = channel.id
            await ctx.send(f"Log channel set to {channel.mention}.")
            await channel.send("AntiNuke is now active! Alerts will appear here.")

    @commands.command(name="toggleautomute")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def toggleautomute(self, ctx):
        """Toggles auto-mute for spammers."""
        guild_id = ctx.guild.id
        self.auto_mute_enabled[guild_id] = not self.auto_mute_enabled.get(guild_id, False)
        status = "enabled" if self.auto_mute_enabled[guild_id] else "disabled"
        await ctx.send(f"Auto-mute is now {status}.")

    @commands.command(name="setmuteduration")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setmuteduration(self, ctx, duration: int):
        """Sets the duration for auto-mute in seconds."""
        if duration > 0:
            self.mute_duration = duration
            await ctx.send(f"Mute duration set to {duration} seconds.")
        else:
            await ctx.send("Duration must be positive!")

    @commands.command(name="whitelistrole")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def whitelistrole(self, ctx, role: discord.Role):
        """Adds a role to be ignored by AntiNuke."""
        guild_id = ctx.guild.id
        if guild_id not in self.whitelisted_roles:
            self.whitelisted_roles[guild_id] = set()
        self.whitelisted_roles[guild_id].add(role.id)
        await ctx.send(f"{role.mention} whitelisted from AntiNuke.")

    @commands.command(name="removewhitelistrole")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def removewhitelistrole(self, ctx, role: discord.Role):
        """Removes a role from the AntiNuke whitelist."""
        guild_id = ctx.guild.id
        if guild_id in self.whitelisted_roles and role.id in self.whitelisted_roles[guild_id]:
            self.whitelisted_roles[guild_id].remove(role.id)
            await ctx.send(f"{role.mention} removed from whitelist.")
        else:
            await ctx.send("Role not whitelisted or invalid!")

    @commands.command(name="togglemassbanprotection")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def togglemassbanprotection(self, ctx):
        """Toggles mass ban protection."""
        guild_id = ctx.guild.id
        self.protections[guild_id] = self.protections.get(guild_id, {})
        self.protections[guild_id]["mass_ban"] = not self.protections.get(guild_id, {}).get("mass_ban", True)
        status = "enabled" if self.protections[guild_id]["mass_ban"] else "disabled"
        await ctx.send(f"Mass ban protection is now {status}.")

    @commands.command(name="togglemasskickprotection")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def togglemasskickprotection(self, ctx):
        """Toggles mass kick protection."""
        guild_id = ctx.guild.id
        self.protections[guild_id] = self.protections.get(guild_id, {})
        self.protections[guild_id]["mass_kick"] = not self.protections.get(guild_id, {}).get("mass_kick", True)
        status = "enabled" if self.protections[guild_id]["mass_kick"] else "disabled"
        await ctx.send(f"Mass kick protection is now {status}.")

    @commands.command(name="togglemasspingprotection")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def togglemasspingprotection(self, ctx):
        """Toggles mass ping protection."""
        guild_id = ctx.guild.id
        self.protections[guild_id] = self.protections.get(guild_id, {})
        self.protections[guild_id]["mass_ping"] = not self.protections.get(guild_id, {}).get("mass_ping", True)
        status = "enabled" if self.protections[guild_id]["mass_ping"] else "disabled"
        await ctx.send(f"Mass ping protection is now {status}.")

    @commands.command(name="togglespamprotection")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def togglespamprotection(self, ctx):
        """Toggles spam protection."""
        guild_id = ctx.guild.id
        self.protections[guild_id] = self.protections.get(guild_id, {})
        self.protections[guild_id]["spam"] = not self.protections.get(guild_id, {}).get("spam", True)
        status = "enabled" if self.protections[guild_id]["spam"] else "disabled"
        await ctx.send(f"Spam protection is now {status}.")

    @commands.command(name="massban")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def massban(self, ctx, *, args):
        """Bans multiple users. Usage: .massban @user1 @user2 reason"""
        guild_id = ctx.guild.id
        users = ctx.message.mentions
        reason = args.split(maxsplit=len(users))[len(users):].strip() or "Mass ban by admin"
        if users:
            for user in users:
                if not any(role.id in self.whitelisted_roles.get(guild_id, set()) for role in user.roles):
                    await ctx.guild.ban(user, reason=reason)
            log_channel_id = self.log_channel.get(guild_id)
            if log_channel_id:
                log_channel = self.bot.get_channel(log_channel_id)
                await log_channel.send(f"🚫 Mass banned {len(users)} users: {', '.join(u.mention for u in users)} | Reason: {reason}")
            await ctx.send(f"Mass banned {len(users)} users.")
        else:
            await ctx.send("No users mentioned!")

    @commands.command(name="masskick")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def masskick(self, ctx, *, args):
        """Kicks multiple users. Usage: .masskick @user1 @user2 reason"""
        guild_id = ctx.guild.id
        users = ctx.message.mentions
        reason = args.split(maxsplit=len(users))[len(users):].strip() or "Mass kick by admin"
        if users:
            for user in users:
                if not any(role.id in self.whitelisted_roles.get(guild_id, set()) for role in user.roles):
                    await ctx.guild.kick(user, reason=reason)
            log_channel_id = self.log_channel.get(guild_id)
            if log_channel_id:
                log_channel = self.bot.get_channel(log_channel_id)
                await log_channel.send(f"👢 Mass kicked {len(users)} users: {', '.join(u.mention for u in users)} | Reason: {reason}")
            await ctx.send(f"Mass kicked {len(users)} users.")
        else:
            await ctx.send("No users mentioned!")

    @commands.command(name="lock")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx):
        """Locks the server to prevent @everyone from sending messages."""
        guild_id = ctx.guild.id
        self.locked_status[guild_id] = True
        for channel in ctx.guild.channels:
            overwrites = channel.overwrites_for(ctx.guild.default_role)
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites, reason="Server locked by admin")
        log_channel_id = self.log_channel.get(guild_id)
        if log_channel_id:
            log_channel = self.bot.get_channel(log_channel_id)
            await log_channel.send("🔒 Server locked by an admin!")
        embed = discord.Embed(
            title="Server Locked",
            description="@everyone can no longer send messages. Use `.unlock` to reopen.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @commands.command(name="unlock")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx):
        """Unlocks the server to allow @everyone to send messages again."""
        guild_id = ctx.guild.id
        self.locked_status[guild_id] = False
        for channel in ctx.guild.channels:
            overwrites = channel.overwrites_for(ctx.guild.default_role)
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites, reason="Server unlocked by admin")
        log_channel_id = self.log_channel.get(guild_id)
        if log_channel_id:
            log_channel = self.bot.get_channel(log_channel_id)
            await log_channel.send("🔓 Server unlocked by an admin!")
        embed = discord.Embed(
            title="Server Unlocked",
            description="@everyone can now send messages again.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild_id = channel.guild.id
        if self.protections.get(guild_id, {}).get("spam", True) and guild_id not in self.recent_actions["channel_create"]:
            self.recent_actions["channel_create"][guild_id] = []
        self.recent_actions["channel_create"][guild_id].append(time.time())
        self.recent_actions["channel_create"][guild_id] = [t for t in self.recent_actions["channel_create"][guild_id] if t > self.time_window]
        if len(self.recent_actions["channel_create"][guild_id]) > self.thresholds["channel_create"]:
            audit_logs = await channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create).flatten()
            if audit_logs:
                user = audit_logs[0].user
                if not any(role.id in self.whitelisted_roles.get(guild_id, set()) for role in user.roles):
                    await channel.guild.ban(user, reason="Mass channel creation detected")
                    log_channel_id = self.log_channel.get(guild_id)
                    if log_channel_id:
                        log_channel = self.bot.get_channel(log_channel_id)
                        await log_channel.send(f"🚫 Banned {user} for creating {len(self.recent_actions['channel_create'][guild_id])} channels in {self.time_window}s!")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild_id = channel.guild.id
        if self.protections.get(guild_id, {}).get("spam", True) and guild_id not in self.recent_actions["channel_delete"]:
            self.recent_actions["channel_delete"][guild_id] = []
        self.recent_actions["channel_delete"][guild_id].append(time.time())
        self.recent_actions["channel_delete"][guild_id] = [t for t in self.recent_actions["channel_delete"][guild_id] if t > self.time_window]
        if len(self.recent_actions["channel_delete"][guild_id]) > self.thresholds["channel_delete"]:
            audit_logs = await channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete).flatten()
            if audit_logs:
                user = audit_logs[0].user
                if not any(role.id in self.whitelisted_roles.get(guild_id, set()) for role in user.roles):
                    await channel.guild.ban(user, reason="Mass channel deletion detected")
                    log_channel_id = self.log_channel.get(guild_id)
                    if log_channel_id:
                        log_channel = self.bot.get_channel(log_channel_id)
                        await log_channel.send(f"🚫 Banned {user} for deleting {len(self.recent_actions['channel_delete'][guild_id])} channels in {self.time_window}s!")

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild_id = role.guild.id
        if self.protections.get(guild_id, {}).get("spam", True) and guild_id not in self.recent_actions["role_create"]:
            self.recent_actions["role_create"][guild_id] = []
        self.recent_actions["role_create"][guild_id].append(time.time())
        self.recent_actions["role_create"][guild_id] = [t for t in self.recent_actions["role_create"][guild_id] if t > self.time_window]
        if len(self.recent_actions["role_create"][guild_id]) > self.thresholds["role_create"]:
            audit_logs = await role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create).flatten()
            if audit_logs:
                user = audit_logs[0].user
                if not any(role.id in self.whitelisted_roles.get(guild_id, set()) for role in user.roles):
                    await role.guild.ban(user, reason="Mass role creation detected")
                    log_channel_id = self.log_channel.get(guild_id)
                    if log_channel_id:
                        log_channel = self.bot.get_channel(log_channel_id)
                        await log_channel.send(f"🚫 Banned {user} for creating {len(self.recent_actions['role_create'][guild_id])} roles in {self.time_window}s!")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild_id = role.guild.id
        if self.protections.get(guild_id, {}).get("spam", True) and guild_id not in self.recent_actions["role_delete"]:
            self.recent_actions["role_delete"][guild_id] = []
        self.recent_actions["role_delete"][guild_id].append(time.time())
        self.recent_actions["role_delete"][guild_id] = [t for t in self.recent_actions["role_delete"][guild_id] if t > self.time_window]
        if len(self.recent_actions["role_delete"][guild_id]) > self.thresholds["role_delete"]:
            audit_logs = await role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete).flatten()
            if audit_logs:
                user = audit_logs[0].user
                if not any(role.id in self.whitelisted_roles.get(guild_id, set()) for role in user.roles):
                    await role.guild.ban(user, reason="Mass role deletion detected")
                    log_channel_id = self.log_channel.get(guild_id)
                    if log_channel_id:
                        log_channel = self.bot.get_channel(log_channel_id)
                        await log_channel.send(f"🚫 Banned {user} for deleting {len(self.recent_actions['role_delete'][guild_id])} roles in {self.time_window}s!")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        guild_id = guild.id
        if self.protections.get(guild_id, {}).get("mass_ban", True) and guild_id not in self.recent_actions["ban"]:
            self.recent_actions["ban"][guild_id] = []
        self.recent_actions["ban"][guild_id].append(time.time())
        self.recent_actions["ban"][guild_id] = [t for t in self.recent_actions["ban"][guild_id] if t > self.time_window]
        if len(self.recent_actions["ban"][guild_id]) > self.thresholds["ban"]:
            audit_logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
            if audit_logs:
                admin = audit_logs[0].user
                if not any(role.id in self.whitelisted_roles.get(guild_id, set()) for role in admin.roles):
                    await guild.ban(admin, reason="Mass ban detected")
                    log_channel_id = self.log_channel.get(guild_id)
                    if log_channel_id:
                        log_channel = self.bot.get_channel(log_channel_id)
                        await log_channel.send(f"🚫 Banned {admin} for mass banning {len(self.recent_actions['ban'][guild_id])} users in {self.time_window}s!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = member.guild.id
        if self.protections.get(guild_id, {}).get("mass_kick", True) and guild_id not in self.recent_actions["kick"]:
            self.recent_actions["kick"][guild_id] = []
        self.recent_actions["kick"][guild_id].append(time.time())
        self.recent_actions["kick"][guild_id] = [t for t in self.recent_actions["kick"][guild_id] if t > self.time_window]
        if len(self.recent_actions["kick"][guild_id]) > self.thresholds["kick"]:
            audit_logs = await member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick).flatten()
            if audit_logs:
                user = audit_logs[0].user
                if not any(role.id in self.whitelisted_roles.get(guild_id, set()) for role in user.roles):
                    await member.guild.ban(user, reason="Mass kick detected")
                    log_channel_id = self.log_channel.get(guild_id)
                    if log_channel_id:
                        log_channel = self.bot.get_channel(log_channel_id)
                        await log_channel.send(f"🚫 Banned {user} for mass kicking {len(self.recent_actions['kick'][guild_id])} users in {self.time_window}s!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        guild_id = message.guild.id
        user_id = message.author.id
        if guild_id not in self.recent_actions["spam"]:
            self.recent_actions["spam"][guild_id] = {}
        if user_id not in self.recent_actions["spam"][guild_id]:
            self.recent_actions["spam"][guild_id][user_id] = []
        self.recent_actions["spam"][guild_id][user_id].append(time.time())
        self.recent_actions["spam"][guild_id][user_id] = [t for t in self.recent_actions["spam"][guild_id][user_id] if t > self.time_window]
        if len(self.recent_actions["spam"][guild_id][user_id]) > self.thresholds["spam"] and self.protections.get(guild_id, {}).get("spam", True) and self.auto_mute_enabled.get(guild_id, False):
            if not any(role.id in self.whitelisted_roles.get(guild_id, set()) for role in message.author.roles):
                mute_role = discord.utils.get(message.guild.roles, name="Muted")
                if not mute_role:
                    mute_role = await message.guild.create_role(name="Muted", reason="Auto-created for AntiNuke")
                    for channel in message.guild.channels:
                        await channel.set_permissions(mute_role, send_messages=False)
                await message.author.add_roles(mute_role, reason="Mass spam detected")
                await message.channel.send(f"🔇 {message.author.mention} muted for {self.mute_duration // 60} mins due to {len(self.recent_actions['spam'][guild_id][user_id])} messages in {self.time_window}s.")
                log_channel_id = self.log_channel.get(guild_id)
                if log_channel_id:
                    log_channel = self.bot.get_channel(log_channel_id)
                    await log_channel.send(f"🔇 Muted {message.author} for {self.mute_duration // 60} mins due to spam.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        guild_id = message.guild.id
        user_id = message.author.id
        if guild_id not in self.recent_actions["ping"]:
            self.recent_actions["ping"][guild_id] = {}
        if user_id not in self.recent_actions["ping"][guild_id]:
            self.recent_actions["ping"][guild_id][user_id] = []
        ping_count = len([m for m in message.mentions if not m.bot])
        if ping_count > 5:  # Threshold for mass ping
            self.recent_actions["ping"][guild_id][user_id].append(time.time())
            self.recent_actions["ping"][guild_id][user_id] = [t for t in self.recent_actions["ping"][guild_id][user_id] if t > self.time_window]
            if len(self.recent_actions["ping"][guild_id][user_id]) > self.thresholds["ping"] and self.protections.get(guild_id, {}).get("mass_ping", True) and self.auto_mute_enabled.get(guild_id, False):
                if not any(role.id in self.whitelisted_roles.get(guild_id, set()) for role in message.author.roles):
                    mute_role = discord.utils.get(message.guild.roles, name="Muted")
                    if not mute_role:
                        mute_role = await message.guild.create_role(name="Muted", reason="Auto-created for AntiNuke")
                        for channel in message.guild.channels:
                            await channel.set_permissions(mute_role, send_messages=False)
                    await message.author.add_roles(mute_role, reason="Mass ping detected")
                    await message.channel.send(f"🔇 {message.author.mention} muted for {self.mute_duration // 60} mins due to mass pinging.")
                    log_channel_id = self.log_channel.get(guild_id)
                    if log_channel_id:
                        log_channel = self.bot.get_channel(log_channel_id)
                        await log_channel.send(f"🔇 Muted {message.author} for {self.mute_duration // 60} mins due to mass pinging {ping_count} users.")

async def setup(bot):
    await bot.add_cog(AntiNuke(bot))