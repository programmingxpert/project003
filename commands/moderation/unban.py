import discord
from discord.ext import commands

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: str = None):
        """Unbans a member by username or ID (ban members required)."""

        if member is None:
            await ctx.send("Please specify the member to unban (username or ID).")
            return
        member = member.strip()  # remove leading/trailing whitespace

        try:
            # First, try to interpret the input as an ID.
            try:
                user_id = int(member)
            except ValueError:
                user_id = None  # Not an integer, handle it differently

            if user_id:  # Try unbanning via ID
                try:
                    target = await self.bot.fetch_user(user_id)
                    if target is None:
                        await ctx.send("User not found by ID. Please ensure the ID is correct.")
                        return

                    banned_users = await ctx.guild.bans()
                    target_banned = discord.utils.find(lambda ban_entry: ban_entry.user.id == target.id, banned_users)

                    if target_banned is None:
                        await ctx.send(f"User with ID {user_id} is not banned.")
                        return

                    await ctx.guild.unban(target)
                    embed = discord.Embed(
                        title="Member Unbanned",
                        description=f"{target.name} has been unbanned.", #Removed discriminator since its gone.
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                    return

                except discord.NotFound:
                    await ctx.send("User not found by ID. Please ensure the ID is correct.")
                    return
                except discord.Forbidden:
                    await ctx.send("I do not have permission to unban this user.")
                    return
                except discord.HTTPException as e:  # Catch errors like rate limits, etc.
                    await ctx.send(f"An error occurred while unbanning the user: {e}")
                    return

            else:  # Treat as username

                try:
                    banned_users = await ctx.guild.bans()
                    # Filter the banned_users list to find a match
                    matching_bans = [ban_entry for ban_entry in banned_users if ban_entry.user.name.lower() == member.lower()] #Compare usernames in lowercase

                    if not matching_bans:
                        await ctx.send(f"User {member} not found in the ban list.  Note: Usernames are case-sensitive.")
                        return

                    # If multiple matches, pick the first one (should be rare).
                    target = matching_bans[0].user

                    await ctx.guild.unban(target)
                    embed = discord.Embed(
                        title="Member Unbanned",
                        description=f"{target.name} has been unbanned.", #Removed discriminator since its gone.
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                    return

                except discord.Forbidden:
                    await ctx.send("I do not have permission to unban this user.")
                    return
                except discord.HTTPException as e:  # Catch errors like rate limits, etc.
                    await ctx.send(f"An error occurred while unbanning the user: {e}")
                    return

        except Exception as e:  # Catch any other unexpected errors.
            print(f"An unexpected error occurred: {e}")
            await ctx.send("An unexpected error occurred. Please check the bot's console for details.")


async def setup(bot):
    await bot.add_cog(Unban(bot))