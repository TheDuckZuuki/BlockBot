import nextcord
from nextcord.ext import commands
from datetime import datetime

import sys
import os
path = os.getcwd()
sys.path.append('../bot')

from util.loaders.yml import read_yml

config = read_yml('config/config')

class Logs(commands.Cog):
    def __init__(self, bot):    
        self.bot = bot

# Channel
    def channel_edit():
        @commands.Cog.listener()
        async def on_guild_channel_update(self, before, after):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            log = await before.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.channel_update).flatten()
            embed = nextcord.Embed(
                title="✏️ Channel Updated", description=f"Channel {before.mention} renamed")
            embed.add_field(name="User:", value = log[0].user, inline=False)
            embed.add_field(name="Old: ", value=before)
            embed.add_field(name="New: ", value=after)
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)

    def channel_create():
        @commands.Cog.listener()
        async def on_guild_channel_create(self, channel):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            log = await channel.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.channel_create).flatten()
            embed = nextcord.Embed(
                title="🛠️ Channel Created")
            embed.add_field(name="User:", value = log[0].user, inline=False)
            embed.add_field(name="Channel: ", value=channel.mention)
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)

    def channel_delete():
        @commands.Cog.listener()
        async def on_guild_channel_delete(self, channel):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            log = await channel.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.channel_delete).flatten()
            embed = nextcord.Embed(
                title="🗑️ Channel Deleted")
            embed.add_field(name="User:", value = log[0].user.mention, inline=False)
            embed.add_field(name="Channel: ", value=channel.id)
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)



    if config["Logs"]["Enabled"]["Channel-Edit"] == True:
        channel_edit()
    if config["Logs"]["Enabled"]["Channel-Create"] == True:
        channel_create()
    if config["Logs"]["Enabled"]["Channel-Delete"] == True:
        channel_delete()

# Message
    def message_edit():
        @commands.Cog.listener()
        async def on_message_edit(self, before, after):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            embed = nextcord.Embed(
                title="📝 Message Updated", description=f"[Message]({after.jump_url}) by {before.author.mention} edited")
            embed.add_field(name="Old message: ", value=before.content)
            embed.add_field(name="New message: ", value=after.content)
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)

    def message_delete():
        @commands.Cog.listener()
        async def on_message_delete(self, message):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            embed = nextcord.Embed(title="🗑️ Message Deleted", description=f"Message by {message.author.mention} deleted in {message.channel.mention}")
            if message.content == "":
                messagecontent = "Embed"
            else:
                messagecontent = message.content
            embed.add_field(name="Message content:", value=messagecontent)
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)

    if config["Logs"]["Enabled"]["Message-Edit"] == True:
        message_edit()
    if config["Logs"]["Enabled"]["Message-Delete"] == True:
        message_delete()

# Role
    def role_edit():
        @commands.Cog.listener()
        async def on_guild_role_update(self, before, after):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            log = await before.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.role_update).flatten()
            embed = nextcord.Embed(
                title="✏️ Role Updated!", description=f"Role {before.mention} was updated by {log[0].user.mention}")
            embed.add_field(name="Old: ", value=before)
            embed.add_field(name="New: ", value=after)
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)

    def role_create():
        @commands.Cog.listener()
        async def on_guild_role_create(self, role):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            log = await role.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.role_create).flatten()
            embed = nextcord.Embed(
                title="🛠️ Role Created", description=f"Created by {log[0].user.mention}")
            embed.add_field(name="Role: ", value=role.mention)
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)

    def role_delete():
        @commands.Cog.listener()
        async def on_guild_role_delete(self, role):
            logs = self.bot.get_channel(config["Logs"]["Logs-Channel-Name"])
            log = await role.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.role_delete).flatten()
            embed = nextcord.Embed(
                title="🗑️ Role Deleted", description=f"Role {role} deleted by {log[0].user.mention}")
            embed.add_field(name="Role: ", value=role)
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)

    if config["Logs"]["Enabled"]["Role-Edit"] == True:
        role_edit()
    if config["Logs"]["Enabled"]["Role-Create"] == True:
        role_create()
    if config["Logs"]["Enabled"]["Role-Delete"] == True:
        role_delete()

def setup(bot):
    bot.add_cog(Logs(bot))
