from decouple import config
from discord.ext import commands
from discord import Intents
from os import listdir


intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def setup_hook():
    await bot.load_extension('manage')
    
    for file in listdir(r'DiscordBot/commands'):
        if file.endswith('.py'):
            await bot.load_extension(f'commands.{file[:-3]}')

bot.run(config('TOKEN'))