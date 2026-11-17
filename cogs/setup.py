import disnake
import logging
from disnake.ext import commands
import utils.discordhelper as ds
from discorddb import LogDataBase, UserDataBase
from utils.utils import logs

logger = logging.getLogger(__name__)

class SetUp(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name='setup_logs', description='SetUp logs', default_member_permissions=disnake.Permissions(administrator=True))
    @logs
    async def set(self, interaction):
        embed = disnake.Embed(title='Настройки Логов', description=f'{ds.utils.developer} | Для работы с логами нужен канал куда отправлять сообщения. Выберите канал где будут приходить сообщения при любых действий', colour=disnake.Colour.orange())
        embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.add_field(name='Предупреждение', value=f'{ds.utils.developer} | При подключении логов убедитесь что у бота есть все нужные права! </perstats:1>')
        logger.debug(f'Setup logs command used by {interaction.author.id} in guild {interaction.guild_id}.')
        if ds.logs_beta:
            embed.add_field(name='Пользовательское соглашение', value=f'{ds.utils.navigation} | При выборе канала, вы соглашаетесь на использование нашей продукции которая находится на **BETA** Версии')
        await interaction.response.send_message(embed=embed, view=View(), ephemeral=True)
        

class View(disnake.ui.View):
    @logs
    def __init__(self):
        super().__init__(timeout=None)
        
        self.add_item(Select_Channel('Select channel', 'channel_setup', 1, 1,1, self))
        
class Select_Channel(disnake.ui.ChannelSelect):
    @logs
    def __init__(self, placeholder, custom_id, row, min_values, max_values, button):
        super().__init__(placeholder=placeholder, custom_id=custom_id, row=row, min_values=min_values, max_values=max_values, channel_types=[disnake.ChannelType.text])
        print(disnake.ChannelType)
        self.button = button
        self.ldb = LogDataBase()
        self.udb = UserDataBase()
        
    @logs
    async def callback(self, interaction):
        await self.udb.createtable()
        selected_channel = interaction.guild.get_channel(int(interaction.values[0]))
        print(interaction.guild.get_channel(int(interaction.values[0])))
        perms = selected_channel.permissions_for(interaction.guild.me)
        server_id = interaction.guild_id
        await self.udb.adduser(interaction.author, server_id)
        log_values = await self.ldb.getlog(server_id)
        if perms.view_channel and perms.send_messages:
            if log_values is not None and log_values[1] == 1:
                await self.ldb.updatelog(True, server_id, selected_channel.id)
                await interaction.response.send_message('Вы успешно Изменили канал. настройка завершена', ephemeral=True)
            else:
                await self.ldb.updatelog(True, server_id, selected_channel.id)
                await interaction.response.send_message('Вы успешно выбрали канал. настройка завершена', ephemeral=True)
            logger.debug(f'User {interaction.author.id} set up logs in channel {selected_channel.id} in guild {interaction.guild_id}.')
        else:
            await interaction.response.send_message(f'Отсутствует доступ к каналу **{selected_channel}**', ephemeral=True)
            logger.warning(f'User {interaction.author.id} attempted to set up logs in channel {selected_channel.id} in guild {interaction.guild_id}, but the bot lacks permissions.')
        
@logs
def setup(bot):
    bot.add_cog(SetUp(bot))