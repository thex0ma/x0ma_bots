import disnake
import logging
from disnake.ext import commands
import utils.discordhelper as ds
from discorddb import UserDataBase
from utils.utils import logs

logger = logging.getLogger(__name__)

class StatsUser(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        self.udb = UserDataBase()
    
    @commands.slash_command(name='user', description='Info about users')
    @logs
    async def user(self, interaction, user: disnake.Member = commands.Param(default=None, name='user', description='User')):
        if user is None:
            user = interaction.author
        await self.udb.createtable()
        await self.udb.adduser(user, interaction.guild_id)
        data = await self.udb.getuser(user, interaction.guild_id)
        embed = disnake.Embed(title=f'Информация об учаснике {user}', description=f'Пользователь: {user.mention}\nАкаунт создан: {disnake.utils.format_dt(user.created_at, "R")}\nСамая высокая роль: {user.top_role.mention}\nБан чата: {"Нету" if user.current_timeout is None else "До " + disnake.utils.format_dt(user.current_timeout, "T")}', colour=disnake.Colour.orange())
        embed.add_field(name='Пользовательская информация', value=f'Всего получено предупреждений: **{data[6]}**\nВсего получено банов: **{data[7]}**\nВсего получено мутов: **{data[8]}**\nВсего получено киков: **{data[9]}**\n')
        embed.add_field(name='Модераторская информация', value=f'Всего выдано предупреждений: **{data[10]}**\nВсего выдано банов: **{data[11]}**\nВсего выдано мутов: **{data[12]}**\nВсего выдано киков: **{data[13]}**\n')
        embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        logger.debug(f'User command used by {interaction.author.id} in guild {interaction.guild_id}.')

@logs
def setup(bot):
    bot.add_cog(StatsUser(bot))
    