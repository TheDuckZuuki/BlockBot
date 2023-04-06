import nextcord

import sys
import os
path = os.getcwd()
sys.path.append('../bot')

from util.loaders.yml import read_yml

config = read_yml('config/config')

class Tickets_Panel(nextcord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Create Ticket",
        style=nextcord.ButtonStyle.green,
        custom_id="create_ticket:green"
    )
    async def create_ticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        msg = await interaction.response.send_message("A ticket is being created!!", ephemeral=True)
        overwrites = {
            interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
            interaction.user: nextcord.PermissionOverwrite(read_messages=True),
            interaction.guild.get_role(config['Tickets']['Support-Role-Id']): nextcord.PermissionOverwrite(read_messages=True)
        }
        guild = self.bot.get_guild(config["Guild-Id"])
        cat = nextcord.utils.get(guild.categories, id=config["Tickets"]["Category-Id"])
        channel = await interaction.guild.create_text_channel(f"{interaction.user.name}-ticket", overwrites=overwrites, category=cat)
        user = interaction.user.name
        await msg.edit(f"Channel Created! " + channel.mention)
        embed = nextcord.Embed(
            title=f"Ticket for " + interaction.user.name,
            description=f"Click a button below to change settings"
        )
        await channel.send(embed=embed, view=Ticket_Buttons())

class Ticket_Buttons(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(
        label="Close Ticket", style=nextcord.ButtonStyle.red, custom_id="ticket_close:red"
    )
    async def close_ticket(self, button: nextcord.ui.Button, interaction: nextcord. Interaction):
        await interaction.response.send_message("Ticket is being closed.", ephemeral=True)
        await interaction.channel.delete()
        embed = nextcord.Embed(title="Ticket deleted!", description="The ticket has been closed!", color=nextcord.Color.red)
        await interaction.user.send(embed=embed)