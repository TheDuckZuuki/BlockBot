import nextcord
from nextcord.ext import commands

guild = 1046096307439284224

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        entries = await ctx.guild.audit_logs(limit=1, action=nextcord.AuditLogAction.channel_create).flatten()
        print(entries)
        

def setup(bot):
    bot.add_cog(Moderation(bot))
