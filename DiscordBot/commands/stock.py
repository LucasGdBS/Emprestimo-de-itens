import discord
import requests
from os import linesep
from discord.ext import commands
from dispie import Paginator

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
    async def get_list(self, ctx):
        """
        Exibe um catálogo com todos os itens disponiveis - !catalogo
        """

        response = requests.get(url=f'{self.api}').json()

        itens = [str(item.get('item')) for item in response]

        paginas = int(len(itens)/6) + (len(itens)/6 > int(len(itens)/6))

        embeds = list()
        for n,lines in enumerate(discord.utils.as_chunks(itens, 6)):
            embed = discord.Embed(title='Itens disponiveis para emprestimo', description=f'Página {n+1} de {paginas}', color=discord.Color.orange())
            for line in lines:
                embed.add_field(name=line, value='', inline=True)

            embeds.append(embed)
        
        pages = Paginator(embeds)
        await pages.start(ctx)


async def setup(bot):
    await bot.add_cog(Stock(bot))
