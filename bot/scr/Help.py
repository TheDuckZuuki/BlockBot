import nextcord
from nextcord.ext import commands


class drop(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="1", description="something"),
            nextcord.SelectOption(label="2", description="something"),
            nextcord.SelectOption(label="3", description="somethinge")
        ]
        
        super().__init__(placeholder="Test.lol", options=options, min_values=1, max_values=1)
    
    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"You chose `{self.values[0]}`, was it fun?")

class view(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(drop())

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="TESTING TESTING")
    async def test(self, ctx):
        await ctx.send("YEEHAW", view=view())

def setup(bot):
    bot.add_cog(Help(bot))