from discord.ext import commands
import requests

class Loan(commands.Cog):
    """ Works with item lending """
    
    def __init__(self, bot):
        self.bot = bot
        self.api = 'http://127.0.0.1:8000/estoque'
    
    @commands.command(name='emprestar')
    async def emprestar(self, ctx, *entrada):
        '''
        Pega um item emprestado, tirando-o do estoque- !emprestar <item> <email> 
        '''

        item = ' '.join(entrada[:-1])
        email = entrada[-1]

        nome = ctx.author.nick
        if nome is None:
            nome = ctx.author.name

        response = requests.put(url=f'{self.api}/emprestar?nome_item={item}&user={nome}&email={email}')
        if 'Erro' not in response.json():
            await ctx.send(f'{item} emprestado para {nome}! Não esqueça de pega-lo!')
        else:
            await ctx.send(f'Não temos {item} no estoque para emprestar :(')

    @commands.command(name='devolver')
    async def devolver(self, ctx, *nome_item):
        '''
        Devolve um item que foi pego, colocando-o no estoque- !devolver <item> <email> 
        '''

        item = ' '.join(nome_item[:-1])
        email = nome_item[-1]

        nome = ctx.author.nick
        if nome is None:
            nome = ctx.author.name

        response = requests.put(url=f'{self.api}/devolver?nome_item={item}&user={nome}&email={email}')
        if 'Erro' not in response.json():
            await ctx.send(f'{item} Devolvido por {nome}! Não esqueça de entrega-lo!')
        else:
            await ctx.send(f'Algo deu errado... não consegui devolver :(')

async def setup(bot):
    await bot.add_cog(Loan(bot))
