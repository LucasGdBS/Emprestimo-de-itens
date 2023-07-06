from os import linesep
import json
import discord
import requests
from discord.ext import commands
from key import key

path = 'http://127.0.0.1:8000/estoque'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def get_item(ctx, item):
    '''
    Exibe informações do item escolhido 
    >get_item [nome_do_item]
    '''
    response = requests.get(url=f'{path}/get-item/{item}').json()
    string = f'{item} no GARAGino'

    
    for k,v in response.items():
        string += f'{linesep}{k}: {v}'
    await ctx.send(string)

@bot.command()
async def emprestar(ctx, item):
    '''
    Pega um item emprestado, tirando-o do estoque
    >emprestar [nome_do_item]
    '''
    response = requests.put(url=f'{path}/emprestar?nome_item={item}')
    if 'Erro' not in response.json():
        await ctx.send(f'{item} emprestado! Não esqueça de pega-lo!')
    else:
        await ctx.send(f'Não temos {item} no estoque para emprestar :(')

@bot.command()
async def devolver(ctx, item):
    '''
    Devolve um item que foi pego, colocando-o no estoque
    >devolver [nome_do_item]
    '''
    response = requests.put(url=f'{path}/devolver?nome_item={item}')
    if 'Erro' not in response.json():
        await ctx.send(f'{item} Devolvido! Não esqueça de entrega-lo!')
    else:
        await ctx.send(f'Algo deu errado... não consegui devolver :(')

bot.run(key)