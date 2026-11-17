import disnake
import logging
from disnake.ext import commands
import utils.discordhelper as ds
from utils.utils import logs

logger = logging.getLogger(__name__)

class Stats(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name='perstats', description='Check bot permissions')
    @logs
    async def perstats(self, interaction):
        bot = interaction.guild.get_member(self.bot.user.id)
        if bot.guild_permissions.administrator:
            embed = disnake.Embed(title='Проверка прав бота', description=f'Права администратора: {ds.emoji.yes}')
            logger.info(f'Bot has administrator permissions in {interaction.guild.name}')
        else:
            embed = disnake.Embed(title='Требуемые права боту', description='')
            embed.add_field(name='Модерация', value=f'''
Разрешение блокировать: {ds.emoji.yes if bot.guild_permissions.ban_members else ds.emoji.no}
Разрешение изменять сообщения: {ds.emoji.yes if bot.guild_permissions.manage_messages else ds.emoji.no}
Разрешение выдавать тайм-аунты участникам: {ds.emoji.yes if bot.guild_permissions.moderate_members else ds.emoji.no}
                            
                            ''')
            embed.add_field(name='Чат и другие', value=f'Разрешение на отправку сообщения: {ds.emoji.yes if bot.guild_permissions.send_messages else ds.emoji.no}')
        embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.debug(f'Permission stats command used by {interaction.author.id} in guild {interaction.guild_id}.')
        
        
@logs
def setup(bot):
    bot.add_cog(Stats(bot))