import disnake
import logging
from disnake.ext import commands 
from discorddb import ReputationDataBase, UserDataBase
import utils.discordhelper as ds
from utils.utils import logs

logger = logging.getLogger(__name__)

class Ban(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        self.rdb = ReputationDataBase()
        self.udb = UserDataBase()
    @commands.slash_command(name='unban', description='Разбан человека', default_member_permissions=disnake.Permissions(administrator=True))
    @logs
    async def unban(self, interaction, userid: disnake.User = commands.Param(name='id', description='id for unban')):
        try:
            await self.udb.createtable()
            await self.udb.adduser(interaction.author, interaction.guild_id)
            await self.rdb.updaterep(interaction.author.id, 10, interaction.guild_id)
            await interaction.guild.unban(userid)
            embed = disnake.Embed(title='РазБан', description=f'{ds.utils.wow} Пользователь: {userid.mention}\nБыл Разбанен\n{ds.utils.staff} Администратором: {interaction.author.name}', colour=disnake.Colour.green())
            embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            logger.info(f'User {interaction.author.id} unbanned user {userid} in guild {interaction.guild_id}.')

        except disnake.errors.Forbidden:
            await interaction.response.send_message("Прости но у меня нету нужных прав для этого! Обратитесь к администратору сервера.", ephemeral=True)
            logger.error(f'User {interaction.author.id} attempted to unban user {userid} in guild {interaction.guild_id} but the bot lacks permissions.')

    @commands.slash_command(name='ban', description='Бан человека', default_member_permissions=disnake.Permissions(administrator=True))
    @logs
    async def ban(self, interaction, user: disnake.User = commands.Param(name='user', description='User or id for ban'), *, reason:str = commands.Param(name='reason', description='Reason', default='Причина не указана')):
        try:
            if user.id != interaction.author.id:
                await self.udb.createtable()
                await self.udb.adduser(interaction.author, interaction.guild_id)
                await self.udb.adduser(user, interaction.guild_id)
                await self.udb.updatedata(user, 0, 0, interaction.guild_id, all_bans=1)
                await self.udb.updatedata(interaction.author, 0, 0, interaction.guild_id, aall_bans=1)
                await self.rdb.updaterep(interaction.author.id, 10, interaction.guild_id)
                embed = disnake.Embed(title='Бан', description=f'{ds.utils.wow} Забанен пользователь: {user.mention} \n{ds.utils.diamond} По причине: {reason}\n{ds.utils.staff} Администратор: {interaction.author.name}', colour=disnake.Colour.red())
                embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                await user.send(embed=embed)
                await interaction.guild.ban(user, reason=reason)
                await interaction.response.send_message(embed=embed)
                logger.info(f'User {interaction.author.id} banned user {user.id} for reason: {reason} in guild {interaction.guild_id}.')
            else:
                await interaction.response.send_message('Вы не можете выдать самому себе наказание!', ephemeral=True)
                logger.warning(f'User {interaction.author.id} attempted to ban themselves in guild {interaction.guild_id}.')
        except disnake.errors.Forbidden:
            await interaction.response.send_message("Прости но у меня нету нужных прав для этого! Обратитесь к администратору сервера.", ephemeral=True)
            logger.error(f'User {interaction.author.id} attempted to ban user {user.id} in guild {interaction.guild_id} but the bot lacks permissions.')
@logs
def setup(bot):
    bot.add_cog(Ban(bot))
