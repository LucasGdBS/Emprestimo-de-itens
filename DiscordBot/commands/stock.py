import discord
import requests
from os import linesep
from discord.ext import commands

class Stock(commands.Cog):
    """ Return stock's informations"""

    def __init__(self, bot):
        self.bot = bot
        self.api = 'http://127.0.0.1:8000/estoque'
    
    @commands.command(name='sobre')
    async def get_item(self, ctx, *nome_item):
        '''
        Exibe informações do item escolhido- !sobre <item>
        '''

        item = ' '.join(nome_item)

        response = requests.get(url=f'{self.api}/get-item?nome_item={item}').json()

        if 'Erro' not in response:
            embed = discord.Embed(title=f'Consulta de {item}',
                                    color=discord.Color.orange())
            
            embed.add_field(name='Item', value=response.get('Item'), inline=True)
            embed.add_field(name='Quantidade total', value=response.get('qnt_total'), inline=True)
            embed.add_field(name='Quantidade em Estoque', value=response.get('qnt_estoque'), inline=True)
            embed.add_field(name='Quantidade de emprestados', value=response.get('qnt_emprestados'), inline=True)

            embed.add_field(name='Dica💡', value='Para emprestar um item use !emprestar <nome item> <seu e-mail>', inline=False)

        else:
            embed = discord.Embed(title=f'Consulta de {item}',
                                  description=f'Não foi possivel localizar {item} nos meus registros...',
                                    color=discord.Color.orange())
            
            embed.add_field(name='Dica💡', value='Para saber todos os itens que temos disponiveis para emprestimo use !catalogo')
        
        await ctx.author.send(embed=embed)
        await ctx.message.delete()
    
    @commands.command(name='catalogo')
    async def get_items(self, ctx):
        '''
        Exibe todos os itens no catalogo- !catalogo <item>
        '''

        response = requests.get(url=f'{self.api}').json()
        string = f'Catalogo do GARAGino{linesep}'

        for n,item in enumerate(response):
            item = item.get('item')
            string += f'{item} '
            if n % 4 == 0 and n != 0:
                string += linesep
        
        await ctx.send(string)


async def setup(bot):
    await bot.add_cog(Stock(bot))
