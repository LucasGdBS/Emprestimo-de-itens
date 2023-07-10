import requests
from os import linesep
from discord.ext import commands

class Stock(commands.Cog):
    """ Return stock's informations"""

    def __init__(self, bot):
        self.bot = bot
        self.api = 'http://127.0.0.1:8000/estoque'
    
    @commands.command(name='estoque')
    async def get_item(self, ctx, *nome_item):
        '''
        Exibe informações do item escolhido- !estoque <item>
        '''

        item = ' '.join(nome_item)

        response = requests.get(url=f'{self.api}/get-item?nome_item={item}').json()
        string = f'{item} no GARAGino'


        for k,v in response.items():
            if not k == 'qnt_quebrados':
                string += f'{linesep}{k}: {v}'
        await ctx.send(string)

async def setup(bot):
    await bot.add_cog(Stock(bot))
