import nextcord
from nextcord.ext import commands
from datetime import datetime


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        logs = self.bot.get_channel(1047195462639288320)
        log = await channel.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.channel_create).flatten()
        embed = nextcord.Embed(
            title="Channel created!", description=f"A channel was created", color=nextcord.Color.blurple())
        embed.add_field(name="Channel: ", value=channel.mention)
        embed.add_field(name="User:", value=log[0].user, inline=False)
        embed.timestamp = datetime.now()
        await logs.send(embed=embed)
    
    def message():
        @commands.Cog.listener()
        async def on_message_edit(self, before, after):
            logs = self.bot.get_channel(1039848665562501190)
            embed = nextcord.Embed(
                title="📝 Message Updated", description=f"[Message]({after.jump_url}) by {before.author.mention} edited")
            embed.add_field(name="Old message: ", value=before.content)
            embed.add_field(name="New message: ", value=after.content)
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)
        
        @commands.Cog.listener()
        async def on_message_delete(self, message):
            logs = self.bot.get_channel(1039848665562501190)
            embed = nextcord.Embed(title="🗑️ Message Deleted", description=f"Message by {message.author.mention} deleted in {message.channel.mention}")
            if message.content == "":
                messagecontent = "Embed"
            else:
                messagecontent = message.content
            embed.add_field(name="Message content:", value=messagecontent)
            embed.timestamp = datetime.now()
            await logs.send(embed=embed)
    message()

def setup(bot):
    bot.add_cog(Logs(bot))
