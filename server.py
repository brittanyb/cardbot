# Discord server access for Cardbot

import discord

class CardServer():
    def __init__(self):
        intents = discord.Intents.all()
        self.bot = discord.ext.commands.Bot(intents=intents, command_prefix="!")