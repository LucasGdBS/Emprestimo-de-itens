import json
import discord
import requests
from discord.ext import commands

path = 'http://127.0.0.1:8000/estoque'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def get_item(ctx, item):
    response = requests.get(url=f'{path}/get-item/{item}').json()

    await ctx.send(f'{item} no GARAGino')
    for k,v in response.items():
        await ctx.send(f'{k}: {v}')

@bot.command()
async def emprestar(ctx, item):
    response = requests.put(url=f'{path}/emprestar?nome_item={item}')
    if 'Erro' not in response:
        await ctx.send(f'{item} emprestado! Não esqueça de pega-lo!')
    else:
        await ctx.send(f'Não temos {item} no estoque para emprestar :()')

@bot.command()
async def devolver(ctx, item):
    response = requests.put(url=f'{path}/devolver?nome_item={item}')
    if 'Erro' not in response:
        await ctx.send(f'{item} Devolvido! Não esqueça de entrega-lo!')
    else:
        await ctx.send(f'Algo deu errado... não consegui devolver :()')

bot.run('MTEyNjI5Mzg4ODMyMDE1MTU1Mw.GpvvCD.hhcnNi3qzqA46JFlwt9AO3BYRC_Bx8vJO9-zew')