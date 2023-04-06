import nextcord
from nextcord.ext import commands, application_checks
from datetime import datetime

import sys
import os
path = os.getcwd()
sys.path.append('../bot')

from util.loaders.yml import read_yml

config = read_yml('config/config')

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def userinfo_cmd():
        @nextcord.slash_command(description="Show information about the user")
        @application_checks.has_permissions(administrator=True)
        async def userinfo(self, ctx, user: nextcord.Member):
            if user == None:
                user = ctx.user
            author = ctx.user
            date_format = "%a, %d %b %Y %I:%M %p"
            em = nextcord.Embed()
            em.set_author(name=f"User-{user}")
            em.add_field(name="Registered", value=user.created_at.strftime(date_format))
            em.add_field(name="Joined on", value=user.joined_at.strftime(date_format))
            em.add_field(name="ID", value=user.id)
            if len(user.roles) > 1:
                role_string = ' '.join([r.mention for r in user.roles][1:])
                em.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
            perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
            em.add_field(name="Guild permissions", value=perm_string, inline=False)
            await ctx.send(embed=em, ephemeral=True)
            self.bot.dispatch('userinfo', user, author)
            return

        @userinfo.error
        async def on_userinfo_error(self, interaction: nextcord.Interaction, error):
            if isinstance(error, application_checks.ApplicationMissingPermissions):
                embed = nextcord.Embed(title="Insufficient perms", description="You do not have the right permissions to run this comand.") 
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                raise error

    def purge_cmd():
        @nextcord.slash_command(description="Delete a several messages at once")
        @application_checks.has_permissions(manage_messages=True)
        async def purge(self, ctx, ammount: int):
                embed = nextcord.Embed(
                title="Cleared", description=f"You cleared {ammount} messages")
                channel = ctx.channel
                author = ctx.user
                await ctx.channel.purge(limit=ammount)
                await ctx.send(embed=embed, ephemeral=True)
                self.bot.dispatch('purge', ammount, channel, author)

        @purge.error
        async def on_purge_error(self, interaction: nextcord.Interaction, error):
            if isinstance(error, application_checks.ApplicationMissingPermissions):
                embed = nextcord.Embed(title="Insufficient perms", description="You do not have the right permissions to run this comand.") 
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                raise error

    def ban_cmd():
        @nextcord.slash_command(description="Bans a user")
        @application_checks.has_permissions(ban_members=True)
        async def ban(self, ctx, member: nextcord.Member, *, reason=None):
            author=ctx.user
            if reason == None:
                reason = "No reason provided"
            await member.ban(reason=reason)
            embed = nextcord.Embed(
                title="Ban", description=f"Banned {member.mention}.", color=nextcord.Color.from_rgb(3, 200, 255))
            await ctx.send(embed=embed, delete_after=5)
            self.bot.dispatch('ban', member, author, reason, self)


        @ban.error
        async def on_ban_error(self, interaction: nextcord.Interaction, error):
            if isinstance(error, application_checks.ApplicationMissingPermissions):
                embed = nextcord.Embed(title="Insufficient perms", description="You do not have the right permissions to run this comand.") 
                await interaction.response.send_message(embed=embed, ephemeral=True)
                self.bot.dispatch('command', interaction.channel, interaction.author, suck="failed to", name="ban")
            else:
                raise error

        @commands.Cog.listener()
        async def on_ban(member, author, reason, self):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            embed = nextcord.Embed(
                title="Ban command!", description=f"{author} banned {member} reason {reason}", color=nextcord.Color.blue())
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)

    def unban_cmd():
        @nextcord.slash_command(description="Unbans the selected user")
        @application_checks.has_permissions(ban_members=True)
        async def unban(self, ctx, *, member):
            author=ctx.user
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if(user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    embed = nextcord.Embed(
                        title="Unbanned", description=f"Unbanned {user.name}#{user.discriminator}", color=nextcord.Color.from_rgb(0, 255, 0))
                    await ctx.send(embed=embed)
                    return
            self.bot.dispatch('unban', member, author, self)

        @unban.error
        async def on_unban_error(self, interaction: nextcord.Interaction, error):
            if isinstance(error, application_checks.ApplicationMissingPermissions):
                embed = nextcord.Embed(title="Insufficient perms", description="You do not have the right permissions to run this comand.") 
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                raise error


        @commands.Cog.listener()
        async def on_unban(self, member, author):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            embed = nextcord.Embed(
                title="User unbanned!", description=f"{author} unbanned {member}", color=nextcord.Color.blue())
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)

    def kick_cmd():
        @nextcord.slash_command(description="Kick the selcted user")
        @application_checks.has_permissions(kick_members=True)
        async def kick(self, ctx, member: nextcord.Member, *, reason=None):
            if reason == None:
                reason = "No reason provided"
            await ctx.guild.kick(member)
            channel = ctx.channel
            await channel.purge(limit=1)
            embed = nextcord.Embed(title="Kick", description=f"Kicked {member.mention}.", color=nextcord.Color.from_rgb(255, 0, 0))
            embed.add_field(title="Reason:", value=reason)
            await ctx.send(embed=embed, ephemeral=True)

        @kick.error
        async def on_purge_error(self, interaction: nextcord.Interaction, error):
            if isinstance(error, application_checks.ApplicationMissingPermissions):
                embed = nextcord.Embed(title="Insufficient perms", description="You do not have the right permissions to run this comand.") 
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                raise error

        @commands.Cog.listener()
        async def on_purge(self, ammount, channel, author):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            embed = nextcord.Embed(title="Messages cleared", description=f"{author.mention} deleted messages")
            embed.add_field(name="Ammount: ", value=ammount)
            embed.add_field(name="Channel: ", value=channel.mention)
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)

    def mute_cmd():
        @nextcord.slash_command(description="Mutes the selected user")
        @application_checks.has_permissions(manage_messages=True)
        async def mute(self, ctx, member: nextcord.Member, *, reason=None):
            guild = ctx.guild
            mutedRole = nextcord.utils.get(guild.roles, name="Muted")
            if not mutedRole:
                mutedRole = await guild.create_role(name="Muted")
                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
            await member.add_roles(mutedRole, reason=reason)
            await ctx.send(f"Muted {member.mention} for reason {reason}")
            await member.send(f"You were muted in the server {guild.name} for {reason}")

        @mute.error
        async def on_mute_error(self, interaction: nextcord.Interaction, error):
            if isinstance(error, application_checks.ApplicationMissingPermissions):
                embed = nextcord.Embed(title="Insufficient perms", description="You do not have the right permissions to run this comand.") 
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                raise error

        @commands.Cog.listener()
        async def on_purge(self, ammount, channel, author):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            embed = nextcord.Embed(title="Messages cleared", description=f"{author.mention} deleted messages")
            embed.add_field(name="Ammount: ", value=ammount)
            embed.add_field(name="Channel: ", value=channel.mention)
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)

    def unmute_cmd():
        @nextcord.slash_command(description="Unmutes the selected user")
        @application_checks.has_permissions(manage_messages=True)
        async def unmute(self, ctx, member: nextcord.Member):
            author = ctx.author
            mutedRole = nextcord.utils.get(ctx.guild.roles, name="Muted")
            await member.remove_roles(mutedRole)
            await ctx.send(f"Unmuted {member.mention}", ephemeral=True)
            await member.send(f"You have been unmuted in {ctx.guild.name}")
            self.bot.dispatch('unmute', member, author)

        @unmute.error
        async def on_unmute_error(self, interaction: nextcord.Interaction, error):
            if isinstance(error, application_checks.ApplicationMissingPermissions):
                embed = nextcord.Embed(title="Insufficient perms", description="You do not have the right permissions to run this comand.") 
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                raise error

        @commands.Cog.listener()
        async def on_unmute(self, member, author):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            embed = nextcord.Embed(title="Member unmuted", description=f"{author.mention} unmuted {member.mention}")
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
