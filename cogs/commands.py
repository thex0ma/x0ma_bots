import disnake
import utils.discordhelper as ds
import logging
from disnake.ext import commands
from datetime import datetime
from random import randint
from utils.utils import logs

logger = logging.getLogger(__name__)

class AllCommands(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.slash_command(name='ping', description='Ping the bot')
    @logs
    async def ping(self, interaction):
        try:
            ping = int(self.bot.latency*1000)
            embed = disnake.Embed(title='Ping', description='Мой пинг: `' + str(ping) + '`ms')
            embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            logger.debug(f'Ping command used by {interaction.author.id} in guild {interaction.guild_id}. Latency: {ping}ms.')
        except Exception as error:
            await interaction.response.send_message(embed=disnake.Embed(title='Sorry!', description=f'I get a error please contact the developer <@{self.bot.owner_id}>', colour=disnake.Colour.orange()), ephemeral=True)
            logger.error(f'User {interaction.author.id} attempted to use the ping command in guild {interaction.guild_id} but encountered an error: {str(error)[:25]}...')
    
    @commands.slash_command(name='update', description='Check update')
    @logs
    async def update(self, interaction):
        time = datetime(year=2025, month=5, day=19, hour=19)
        cooltime = disnake.utils.format_dt(time, 'R')
        v = ds.version
        c = ds.numcode
        embed = disnake.Embed(title=f'Обновление {v}', description=f'''В обновлении **{v}** Добавилось:
1. Исправление багов </setup_logs:0>
2. Обновленное оформление </clear:0>
3. Исправление багов в базе данных
4. Исправление багов в системе логов
Выпущено: {cooltime}''')
        embed.add_field(name=f'Обновление {v}', value='В обновлении исправлены Логи (с присоеденением участника) И псевдо-кеш')
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_footer(text=f'Update code {c}')
        embed.set_default_colour(disnake.Colour.orange())
        await interaction.response.send_message(embed=embed)
        logger.debug(f'Update command used by {interaction.author.id} in guild {interaction.guild_id}.')
    
    @commands.slash_command(name='report', description='Report a bug')
    @logs
    async def report(self, interaction, text:str = commands.Param(name='text', description='Text that you want to send the developer')):
        user = f'<@{interaction.author.id}>'
        developer = self.bot.get_user(843203650285076531)
        await developer.send(f'Уведомление от {user}\n{text}')
        logger.warning(f'Report command used by {interaction.author.id} in guild {interaction.guild_id}.')
        
    
    # @commands.slash_command(name='letter', description='Send the letter for your friends')
    # @commands.cooldown(1, 3600, commands.BucketType.user)
    # async def letter(self, interaction, user:disnake.Member = commands.Param(name='user', description='User'), text:str = commands.Param(name='text', description='Text that you want to send')):
    #     codeid = randint(1, 99999999)
    #     sender = self.bot.get_user(user.id)
    #     developer = self.bot.get_user(843203650285076531)
    #     embed1 = disnake.Embed(title='Сообщение', description=f'Привет тебе отправили сообщение с сервера: {interaction.guild.name} ({interaction.guild.id})\nСообщение: \n**{text}**\n\nВнимание при нарушение правил, сервера выше сообщите администрации сервера с скриншотом данного фото\nАдминистрация сервера пожалуйста свяжитесь с разработчиком сервера для получения доп. данных\nУникальное айди: **{codeid}**')
    #     embed2 = disnake.Embed(title='Сообщение', description=f'Пользователь <@{interaction.author.id}> отправил сообщение пользователю <@{user.id}>,\nСообщение:\n**{text}**\n\nУникальное айди: **{codeid}**')
    #     await sender.send(embed=embed1)
    #     await developer.send(embed=embed2)
    #     await interaction.response.send_message('Отправленно!', ephemeral=True)
    
    # @letter.error
    # async def letter_error(self, interaction, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await interaction.send(f'Вы уже использовали данную команду, следующее использование через {error.retry_after:.2f} секунд', ephemeral=True)
@logs
def setup(bot):
    bot.add_cog(AllCommands(bot))