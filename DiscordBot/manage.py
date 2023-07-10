from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound

class Manage(commands.Cog):
    """ Manage the bot """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Conectado como {self.bot.user.name}')
    
    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send('Favor enviar todos os argumentos')
        elif isinstance(error, CommandNotFound):
            await ctx.send('O camando digitado não existe. !help para mais informações')
        else:
            raise error

async def setup(bot):
    await bot.add_cog(Manage(bot))
