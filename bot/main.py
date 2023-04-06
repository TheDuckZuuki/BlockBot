import os, platform, time

from util.loaders.yml import read_yml
from util.loaders.json import read_json, write_json
from util.functions.print import pint

try:
    import nextcord
    import json
    from nextcord.ext import commands, application_checks
except:
    ops = platform.system()
    if ops == "Windows":
        say = ("py -m pip install -r requirements.txt")
    else:
        say = ("pip install requirements.txt")
    pint('Hey! You do not have the requirements installed. Please install the requirements using: the following command: ' + say, 'ERROR')



# Read the config file
config = read_yml('config/config')

# Set intents
intents = nextcord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='-', intents=intents)

# Event that runs when bot is ready
@bot.event
async def on_ready():
    # Set the bot's presence
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name='ur weird cmd'))
    pint(f'Logged in as {bot.user}', 'INFO')

# Create an empty json file
empty = {}
write_json(empty, '/data/modules')

# Inv Tracker

invites = {}
last = ""


@bot.event
async def on_member_join(meme):
    global last
    last = str(meme.id)


async def fetch():
    global invites
    global last
    await bot.wait_until_ready()
    gld = bot.get_guild(int(1046096307439284224))
    logs = bot.get_channel(int(1046097410146975755))
    while True:
        invs = await gld.invites()
        tmp = []
        for i in invs:
            for s in invites:
                if s[0] == i.code:
                    if int(i.uses) > s[1]:
                        usr = gld.get_member(int(last))
                        eme = nextcord.Embed(
                            description="Just joined the server", color=0x03d692, title=" ")
                        eme.add_field(
                            name="Rules:", value="Check out the rules here: <#1046096977030565988>", inline=False)
                        eme.add_field(
                            name="Announcements:", value="Check out all the latest announcements here: \n<#1046097154864853002>", inline=False)
                        eme.add_field(name="Member count:", value="We are currently " + str(
                            usr.guild.member_count) + " members in the server", inline=False)
                        eme.set_thumbnail(url=usr.display_avatar)
                        role = nextcord.utils.get(
                            usr.guild.roles, name='Members')
                        eme.set_author(
                            name=usr.name + "#" + usr.discriminator, icon_url=usr.display_avatar)
                        eme.set_footer(text="Welcome!")
                        eme.timestamp = usr.joined_at
                        eme.add_field(
                            name="Used invite", value="Inviter: " + i.inviter.mention, inline=False)
                        await logs.send(embed=eme)
                        temp = await logs.send(usr.mention)
                        await temp.delete()
            tmp.append(tuple((i.code, i.uses)))
        invites = tmp
        await time.sleep(4)


# * Load modules
for filename in os.listdir('./scr'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'scr.{filename[:-3]}')
            data = read_json('/data/modules')
            file = filename.split('.', 1)[0]
            data[file] = None
            write_json(data, '/data/modules')
            pint('Loaded the module ' + file, 'INFO')
        except:
            pint("Unable to load " + file + ". Reason unknown.", "ERROR")

# Define the module control command


def modules_cmd():
    @bot.slash_command(name='module')
    @application_checks.has_permissions(administrator=True)
    async def module(interaction: nextcord.Interaction): pass

    @module.subcommand(name='load')
    @application_checks.has_permissions(administrator=True)
    async def load(ctx, extensions):
        bot.load_extension(f'scr.{extensions}')
        embed = nextcord.Embed(
            title='Loaded', description='Module is loaded', color=nextcord.Color.blurple())
        await ctx.send(embed=embed)

    @load.error
    async def on_load_error(interaction: nextcord.Interaction, error):
        if isinstance(error, nextcord.ext.commands.errors.ExtensionNotLoaded):
            embed = nextcord.Embed(
                title="Can't find module", description=f'Could not find the module. Please check the spelling.', color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, application_checks.ApplicationMissingPermissions):
            embed = nextcord.Embed(title='Insufficient perms',
                                   description=f'You do not have the perms to run this comand!', color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            raise error

    @module.subcommand(name='unload')
    @application_checks.has_permissions(administrator=True)
    async def unload(ctx, extensions):
        bot.unload_extension(f'scr.{extensions}')
        embed = nextcord.Embed(
            title='Unloaded', description='Module is unloaded', color=nextcord.Color.blurple())
        await ctx.send(embed=embed)

    @unload.error
    async def on_unload_error(interaction: nextcord.Interaction, error):
        if isinstance(error, nextcord.ext.commands.errors.ExtensionNotLoaded):
            embed = nextcord.Embed(
                title="Can't find module", description=f'Could not find the module. Please check the spelling.', color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)
        elif isinstance(error, application_checks.ApplicationMissingPermissions):
            embed = nextcord.Embed(title='Insufficient perms',
                                   description=f'You do not have the perms to run this comand!', color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            raise error

    @module.subcommand(name='reload')
    @application_checks.has_permissions(administrator=True)
    async def reload(ctx, extensions):
        bot.unload_extension(f'scr.{extensions}')
        bot.load_extension(f'scr.{extensions}')
        embed = nextcord.Embed(
            title='Reloaded', description='Module is reloaded', color=nextcord.Color.blurple())
        await ctx.send(embed=embed)

    @reload.error
    async def on_reload_error(interaction: nextcord.Interaction, error):
        if isinstance(error, nextcord.ext.commands.errors.ExtensionNotLoaded):
            embed = nextcord.Embed(
                title="Can't find module", description=f'Could not find the module. Please check the spelling.', color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)
        elif isinstance(error, application_checks.ApplicationMissingPermissions):
            embed = nextcord.Embed(title='Insufficient perms',
                                   description=f'You do not have the perms to run this comand!', color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            raise error

    @module.subcommand(name='list')
    @application_checks.has_permissions(administrator=True)
    async def list(ctx):
        modulest = read_json('/data/modules')
        module = json.dumps(modulest, indent=2)
        modules = module.replace('{', '')
        module = modules.replace('}', '')
        modules = module.replace('"', '')
        module = modules.replace(': null', '')
        embed = nextcord.Embed(
            title='Loaded modules', description=f'Here are the loaded modules', color=nextcord.Color.blurple())
        embed.add_field(name='Modules', value=module)
        await ctx.send(embed=embed)

    @list.error
    async def on_list_error(interaction: nextcord.Interaction, error):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            embed = nextcord.Embed(title='Insufficient perms',
                                   description=f'You do not have the perms to run this comand!', color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            raise error


modules_cmd()

# * Run bot
# bot.loop.create_task(fetch())

bot.run(config['Token'])
