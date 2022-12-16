import nextcord
from nextcord.ext import commands, application_checks
import os

from util.loaders.yml import read_yml
config = read_yml('config\\config')

intents = nextcord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="-", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

#* Load modules
for filename in os.listdir('./scr'):
    if filename.endswith('.py'):
        file = filename.split('.', 1)[0]
        print(f'Loaded the module {file}')
        bot.load_extension(f"scr.{filename[:-3]}")

#* module control
def modules_cmd():
    @bot.slash_command(name='module')
    @application_checks.has_permissions(administrator=True)
    async def module(interaction: nextcord.Interaction): pass
    @module.subcommand(name='load')
    async def load(ctx, extensions):
        bot.load_extension(f'scr.{extensions}')
        embed = nextcord.Embed(
            title="Loaded", description="Module is loaded", color=nextcord.Color.blurple())
        await ctx.send(embed=embed)
    @load.error
    async def on_load_error(interaction: nextcord.Interaction, error):
        if isinstance(error, nextcord.ext.commands.errors.ExtensionNotLoaded):
            embed = nextcord.Embed(
                title="Can't find module", description=f"Could not find the module. Please check the spelling.", color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)
        elif isinstance(error, application_checks.ApplicationMissingPermissions):
            embed = nextcord.Embed(title="Insufficient perms",
                                description=f"You do not have the perms to run this comand!.", color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)
        else:
            raise error
    @module.subcommand(name='unload')
    async def unload(ctx, extensions):
        bot.unload_extension(f'scr.{extensions}')
        embed = nextcord.Embed(
            title="Unloaded", description="Module is unloaded", color=nextcord.Color.blurple())
        await ctx.send(embed=embed)
    @unload.error
    async def on_unload_error(interaction: nextcord.Interaction, error):
        if isinstance(error, nextcord.ext.commands.errors.ExtensionNotLoaded):
            embed = nextcord.Embed(
                title="Can't find module", description=f"Could not find the module. Please check the spelling.", color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)
        elif isinstance(error, application_checks.ApplicationMissingPermissions):
            embed = nextcord.Embed(title="Insufficient perms",
                                description=f"You do not have the perms to run this comand!.", color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)
        else:
            raise error
    @module.subcommand(name='reload')
    async def reload(ctx, extensions):
        bot.unload_extension(f'scr.{extensions}')
        bot.load_extension(f'scr.{extensions}')
        embed = nextcord.Embed(
            title="Reloaded", description="Module is reloaded", color=nextcord.Color.blurple())
        await ctx.send(embed=embed)
    @reload.error
    async def on_reload_error(interaction: nextcord.Interaction, error):
        if isinstance(error, nextcord.ext.commands.errors.ExtensionNotLoaded):
            embed = nextcord.Embed(
                title="Can't find module", description=f"Could not find the module. Please check the spelling.", color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)
        elif isinstance(error, application_checks.ApplicationMissingPermissions):
            embed = nextcord.Embed(title="Insufficient perms",
                                description=f"You do not have the perms to run this comand!.", color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)
        else:
            raise error
    @module.subcommand(name='list')
    async def list(ctx):
        print('modules')
    @list.error
    async def on_list_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            embed = nextcord.Embed(title="Insufficient perms",
                                description=f"You do not have the perms to run this comand!.", color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)
        else:
            raise error
modules_cmd()

#* Run bot
bot.run(config['Token'])