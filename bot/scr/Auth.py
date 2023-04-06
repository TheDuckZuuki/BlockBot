import nextcord
from nextcord.ext import commands

import sys
import os
path = os.getcwd()
sys.path.append('../bot')

from util.loaders.yml import read_yml

config = read_yml('config/config')


class Auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

def setup(bot):
    bot.add_cog(Auth(bot))
