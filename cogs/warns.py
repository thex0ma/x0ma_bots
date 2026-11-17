import datetime
import logging
import disnake
from discorddb import UserDataBase, WarnDataBase, ReputationDataBase
from disnake.ext import commands
import utils.discordhelper as ds
from utils.utils import logs

logger = logging.getLogger(__name__)

class Warns(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        self.rdb = ReputationDataBase()
        self.udb = UserDataBase()
        self.wdn = WarnDataBase()
    
        
    @commands.slash_command(name='warn', description='Give warn', default_member_permissions=disnake.Permissions(moderate_members=True))
    @logs
    async def warn(self, interaction, user: disnake.Member = commands.Param(name='user', description='User for give warn'), reason:str = commands.Param(name='reason', description='Why are you give warn this user', default='Причина не указана')):
            if interaction.author.top_role.position <= user.top_role.position:
                logger.warning(f'User {interaction.author.id} attempted to warn {user.id} but does not have sufficient role hierarchy in guild {interaction.guild_id}.')
                await interaction.response.send_message('Вы не можете выдать наказание пользователю выше своей роли', ephemeral=True)
            else:
                if user.id != interaction.author.id:
                    if user.id != interaction.guild.owner_id:
                        await self.udb.createtable()
                        await self.udb.adduser(interaction.author, interaction.guild_id)
                        await self.udb.adduser(user, interaction.guild_id)
                        await self.udb.updatedata(user, 0, 0, interaction.guild_id, all_warns=1)
                        await self.udb.updatedata(interaction.author, 0, 0, interaction.guild_id, aall_warns=1)
                        await self.rdb.updaterep(interaction.author.id, 4, interaction.guild_id)
                        await self.wdn.warn(user, interaction.author ,reason, interaction.guild_id)
                        embed = disnake.Embed(title='Предупреждение', description=f'{ds.utils.staff} Администратор <@{interaction.author.id}> Выдал предупреждение участнику <@{user.id}>\nПо причине: **{reason}**', colour=disnake.Colour.red())
                        embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
                        logging.info(f'User {interaction.author.id} gave a warning to {user.id} for reason: {reason} in guild {interaction.guild_id}.')
                        
                        await interaction.response.send_message(embed=embed)
                        await user.send(embed=embed)
                    else:
                        await interaction.response.send_message('Ты не можешь выдать наказание владельцу сервера!', ephemeral=True)
                        logger.warning(f'User {interaction.author.id} tried to warn the server owner {user.id} in guild {interaction.guild_id}.')
                else:
                    await interaction.response.send_message('Ты не можешь выдать предупреждение самому себе!')
                    logger.warning(f'User {interaction.author.id} tried to warn themselves in guild {interaction.guild_id}.')
        
    @commands.slash_command(name='warns', description='Get warn by username')
    @logs
    async def warns(self, interaction, user: disnake.Member = commands.Param(name='user', description='User for get warns', default=None)):
        try: 
            if user is None:
                user = interaction.author
            await self.udb.createtable()
            await self.udb.adduser(user, interaction.guild_id)
            get = await self.wdn.getwarn(user, interaction.guild_id)
            embed = disnake.Embed(title=f'Предупреждения пользователя @{user}', colour=disnake.Colour.orange())
            embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            if get == []:
                embed.add_field(name='Предупреждения не найдены', value=f'Возможно у пользователя <@{user.id}> Нету предупреждений!')
                logger.info(f'No warnings found for user {user.id} in guild {interaction.guild_id}.')
            else:
                for i in get:
                    time = datetime.datetime.strptime(i[3], "%Y-%m-%d %H:%M:%S.%f")
                    format_time = disnake.utils.format_dt(time, "f")
                    embed.add_field(name=f'Предупреждение #{i[0]}', value=f'Выдано администратором: <@{i[4]}>\nпо причине: **{i[1]}**\nВыдано {format_time}')
                logger.debug(f'Found warnings for user {user.id} in guild {interaction.guild_id}')
            await interaction.response.send_message(embed=embed)
        except Exception as e: 
            await interaction.response.send_message(f'Oh! We`ve got an error... Please contact the developer! <@{self.bot.owner_id}>')
            logger.error(f'Error occurred while fetching warnings for user {user.id} in guild {interaction.guild_id}: {str(e)[:25]}...')
            
    @commands.slash_command(name='warnid', description='Get warn by id')
    @logs
    async def warnid(self, interaction, id:int = commands.Param(name='warn_id', description='Warn id')):
        try:
            if id < 0:
                await interaction.response.send_message('Номер предупреждения не может быть отрицательным!', ephemeral=True)
                logger.warning(f'User {interaction.author.id} provided an invalid warning ID {id} in guild {interaction.guild_id}.')
            else:
                await self.udb.createtable()
                await self.udb.adduser(interaction.author, interaction.guild_id)
                get = await self.wdn.getwarnbyid(id, interaction.guild_id)
                embed = disnake.Embed(title=f'Предупреждение номер #{id}', colour=disnake.Colour.orange())
                embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                if get is None:
                    embed.add_field(name='Не найдено', value='Возможно этого предупреждения не существует или вы указали не правильный номер')
                    logger.info(f'Warning with ID {id} not found in guild {interaction.guild_id}.')
                else:
                    time = datetime.datetime.strptime(get[3], "%Y-%m-%d %H:%M:%S.%f")
                    format_time = disnake.utils.format_dt(time, "f")
                    embed.add_field(name='Предупреждение', value=f'Предупреждение у <@{get[2]}>\nВыдано Администратором: <@{get[4]}>\nПо причине: **{get[1]}**\nВыдано: {format_time}')
                    logger.debug(f'Found warning #{id} for user {get[2]} in guild {interaction.guild_id}.')
                await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f'Oh! We`ve got an error... Please contact the developer! <@{self.bot.owner_id}>')
            logger.error(f'Error occurred while fetching warning #{id} in guild {interaction.guild_id}: {str(e)[:25]}...')
    @commands.slash_command(name='remwarn', description='Remove warn by id', default_member_permissions=disnake.Permissions(moderate_members=True))
    @logs
    async def remwarn(self, interaction, id: int = commands.Param(name='warn_id', description='Warn id for remove')):
        try:
            await self.udb.createtable()
            await self.udb.adduser(interaction.author, interaction.guild_id)
            await self.rdb.updaterep(interaction.author.id, 4, interaction.guild_id)
            await self.wdn.remwarn(id, interaction.guild_id)
            embed = disnake.Embed(title='Снятие предупреждения', description=f'{ds.utils.staff} Вы успешно сняли предупреждение **#{id}**', colour=disnake.Colour.green())
            embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            logger.info(f'User {interaction.author.id} removed warning #{id} in guild {interaction.guild_id}.')
        except Exception as e:
            await interaction.response.send_message(f'Oh! We`ve got an error... Please contact the developer! <@{self.bot.owner_id}>')
            logger.error(f'Error occurred while removing warning #{id} in guild {interaction.guild_id}: {str(e)[:25]}...')



@logs
def setup(bot):
    bot.add_cog(Warns(bot))
