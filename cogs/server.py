import disnake
import logging
from disnake.ext import commands
from utils.discordhelper import utils, emoji
from discorddb import PermissionDataBase
from utils.utils import logs

logger = logging.getLogger(__name__)

class Server(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        self.pdb = PermissionDataBase()
    
    @commands.slash_command(name='server', description='Info about Server')
    @logs
    async def server(self, interaction):
        guild = interaction.guild
        embed = disnake.Embed(title=f'Информация об сервере *{guild.name}*')
        embed.add_field(name='Общие', value=f'{utils.diamond} Название сервера: **{guild.name}**\n{utils.navigation} Количество пользователей: **{guild.member_count}**\n{utils.info} Владелец: **{guild.owner}**')
        embed.add_field(name='Дополнения', value=f'{utils.diamond} XPlus: {emoji.yes if await self.pdb.getper(2, guild.id) else emoji.no}')
        embed.add_field(name='Другие', value=f'{utils.bag} ID сервера: **{guild.id}**\nКоличество ролей: **{len(guild.roles)}**\n{utils.navigation}Количество текстовых каналов: **{len(guild.text_channels)}**\n{utils.news} Количетсво голосовых каналов: **{len(guild.voice_channels)}**\n{utils.diamond} Общее количество каналов: **{len(guild.channels)}**')
        try:
            embed.set_thumbnail(guild.banner.url)
        except AttributeError:
            logger.warning(f'Guild {guild.id} does not have a banner set.')
        try:
            embed.set_image(guild.icon.url)
        except AttributeError:
            logger.warning(f'Guild {guild.id} does not have an icon set.')
        embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        logger.debug(f'Server command used by {interaction.author.id} in guild {interaction.guild_id}.')
        
@logs
def setup(bot):
    bot.add_cog(Server(bot))