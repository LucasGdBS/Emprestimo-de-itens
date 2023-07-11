from discord.ext import commands
import discord
import requests
from os import linesep

class Loan(commands.Cog):
    """ Works with item lending """
    
    def __init__(self, bot):
        self.bot = bot
        self.api = 'http://127.0.0.1:8000/estoque'
    
    def get_user_name(self, ctx:commands.Context):
        try:
            nome = ctx.author.nick
        except:
            nome = ctx.author.name
        else:
            if nome is None:
                nome = ctx.author.name
        
        return nome
    
    @commands.command(name='emprestar')
    async def emprestar(self, ctx, *entrada):
        '''
        Pega um item emprestado, tirando-o do estoque- !emprestar <item> <email> 
        '''

        item = ' '.join(entrada[:-1])
        email = entrada[-1]

        nome = self.get_user_name(ctx)

        response = requests.put(url=f'{self.api}/emprestar?nome_item={item}&user={nome}&email={email}')
        if 'Erro' not in response.json():
            embed = discord.Embed(title=f'Emprestimo para {nome}!',
                                  description=f'Emprestimo de {item} para {nome} realizado com sucesso!',
                                  color=discord.Color.orange())
            
            embed.add_field(name='Item', value=item, inline=True)
            embed.add_field(name='Usuario', value=nome, inline=True)
            embed.add_field(name='E-mail', value=email, inline=True)

            embed.add_field(name='⚠️Atenção⚠️', value='Não esqueça de pega-lo!', inline=False)
            
        else:
            embed = discord.Embed(title=f'Emprestimo para {nome}!',
                                  description=f'Não foi possivel realizar o emprestimo de {item} para {nome} 😢',
                                  color=discord.Color.orange())
            
            embed.add_field(name='Item', value=item, inline=True)
            embed.add_field(name='Usuario', value=nome, inline=True)
            embed.add_field(name='E-mail', value=email, inline=True)
            
            embed.add_field(name='Sinto muito 😢', value=f'Não temos {item} no estoque para emprestar no momento', inline=False)
        
        await ctx.author.send(embed=embed)
        await ctx.message.delete()

    @commands.command(name='devolver')
    async def devolver(self, ctx, *nome_item):
        '''
        Devolve um item que foi pego, colocando-o no estoque- !devolver <item> <email> 
        '''

        item = ' '.join(nome_item[:-1])
        email = nome_item[-1]

        nome = self.get_user_name(ctx)

        response = requests.put(url=f'{self.api}/devolver?nome_item={item}&user={nome}&email={email}')
        if 'Erro' not in response.json():
            embed = discord.Embed(title=f'Devolução de {nome}!',
                                  description=f'Devolução de {item} por {nome} realizada com sucesso!',
                                  color=discord.Color.orange())
            
            embed.add_field(name='Item', value=item, inline=True)
            embed.add_field(name='Usuario', value=nome, inline=True)
            embed.add_field(name='E-mail', value=email, inline=True)

            embed.add_field(name='⚠️Atenção⚠️', value='Não esqueça de entrega-lo!', inline=False)

        else:
            embed = discord.Embed(title=f'Devolução de {nome}!',
                                  description=f'{nome}, não foi possivel realizar a devolução de {item}',
                                  color=discord.Color.orange())
            
            embed.add_field(name='Item', value=item, inline=True)
            embed.add_field(name='Usuario', value=nome, inline=True)
            embed.add_field(name='E-mail', value=email, inline=True)
            
            embed.add_field(name='Algo de errado aconteceu...🧐', value=f'Não foi possivel realizar a devolução.{linesep}\
                            Tenta novamente em alguns instantes ou fala com o resposavel pelo lab.{linesep}', inline=False)
        
        await ctx.author.send(embed=embed)
        await ctx.message.delete()
    
    @commands.command(name='emprestimos')
    async def emprestimos(self, ctx:commands.Context, email):
        '''
        Função que mostra todos os itens em posse do usuario - !emprestimos <e-mail>
        '''

        nome = self.get_user_name(ctx)

        response = requests.get(url=f'{self.api}/get_user?user={nome}&email={email}').json()

        embed = discord.Embed(title=f'Itens emprestados por {nome}',
                              description=f'Esses são os itens que você pegou emprestado e ainda não devolveu',
                              color=discord.Color.orange())
        
        if 'Nenhum item' not in response:
            for item in response:
                embed.add_field(name=item[0], value='', inline=False)
        else:
            embed.add_field(name='Tá tudo certo!', value='Não encontrei nenhum item emprestado em seu nome', inline=False)
            embed.add_field(name='Dica💡', value='Para pegar um item emprestado use !emprestar <nome do item> <seu email>', inline=False)
        
        await ctx.author.send(embed=embed)
        await ctx.message.delete()

            

async def setup(bot):
    await bot.add_cog(Loan(bot))
