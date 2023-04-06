import nextcord
from nextcord.ext import commands

import sys, os
path = os.getcwd()
sys.path.append('../bot')

from util.loaders.yml import read_yml

config = read_yml('config/config')

# Import views
from util.views.buttons.tickets import Tickets_Panel, Ticket_Buttons


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="setup-tickets")
    async def setup_tickets(self, ctx):
        embed = nextcord.Embed(title="Create a ticket!", description="Press the ``Create Ticket`` buttom below to create a ticket.", color=nextcord.Colour.blurple())
        await ctx.channel.send(embed=embed, view=Tickets_Panel(self.bot))
        embed = nextcord.Embed(title="Sent!", description="Tickets menu sent!", color=nextcord.Colour.blurple())
        await ctx.send(embed=embed, ephemeral=True)


"""
def check(m):
    return m.channel == interaction.channel
answer = await bot.wait_for("message", check = check)
"""

def setup(bot):
    bot.add_cog(Tickets(bot))
