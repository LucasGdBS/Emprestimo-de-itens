import discord
import requests
from os import linesep
from decouple import config
from discord.ext import commands


path = 'http://127.0.0.1:8000/estoque'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def veritem(ctx, *entrada):
    '''
    Exibe informações do item escolhido 
    >get_item [nome_do_item]
    '''

    item = ' '.join(entrada)

    response = requests.get(url=f'{path}/get-item?nome_item={item}').json()
    string = f'{item} no GARAGino'

    
    for k,v in response.items():
        if not k == 'qnt_quebrados':
            string += f'{linesep}{k}: {v}'
    await ctx.send(string)

@bot.command()
async def emprestar(ctx, *entrada):
    '''
    Pega um item emprestado, tirando-o do estoque
    >emprestar [nome_do_item]
    '''

    item = ' '.join(entrada[:-1])
    email = entrada[-1]

    nome = ctx.author.nick
    if nome is None:
        nome = ctx.author.name

    response = requests.put(url=f'{path}/emprestar?nome_item={item}&user={nome}&email={email}')
    if 'Erro' not in response.json():
        await ctx.send(f'{item} emprestado para {nome}! Não esqueça de pega-lo!')
    else:
        await ctx.send(f'Não temos {item} no estoque para emprestar :(')

@bot.command()
async def devolver(ctx, *entrada):
    '''
    Devolve um item que foi pego, colocando-o no estoque
    >devolver [nome_do_item]
    '''

    item = ' '.join(entrada[:-1])
    email = entrada[-1]

    nome = ctx.author.nick
    if nome is None:
        nome = ctx.author.name

    response = requests.put(url=f'{path}/devolver?nome_item={item}&user={nome}&email={email}')
    if 'Erro' not in response.json():
        await ctx.send(f'{item} Devolvido por {nome}! Não esqueça de entrega-lo!')
    else:
        await ctx.send(f'Algo deu errado... não consegui devolver :(')


bot.run(config('TOKEN'))