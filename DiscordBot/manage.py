from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound

class Manage(commands.Cog):
    """ Manage the bot """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Conectado como {self.bot.user.name}')
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.message.reply('O comando digitado não existe. !help para mais informações', delete_after=20.0)
            await ctx.message.delete()
        else:
            raise error

async def setup(bot):
    await bot.add_cog(Manage(bot))
