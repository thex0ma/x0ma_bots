import disnake
import logging
from disnake.ext import commands
from datetime import datetime, timedelta
from discorddb import ReputationDataBase, UserDataBase
import utils.discordhelper as ds
from utils.utils import logs

logger = logging.getLogger(__name__)

class Timeout(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        self.rdb = ReputationDataBase()
        self.udb = UserDataBase()

    @commands.slash_command(name='unmute', description='Размьют человека', default_member_permissions=disnake.Permissions(administrator=True))
    @logs
    async def unmute(self, interaction, member: disnake.Member = commands.Param(name='user', description='User to unmute'), reason:str = commands.Param(default='Причина не указана', description='Reason')):
        try:
            if member.current_timeout != None:
                await self.udb.createtable()
                await self.udb.adduser(interaction.author, interaction.guild_id)
                await self.rdb.updaterep(interaction.author.id, 3, interaction.guild_id)
                await member.timeout(reason=reason, until=None)
                embed = disnake.Embed(title='РазМьют', description=f'{ds.utils.wow}Пользователю: {member.mention} \nУбрали мьют По причине: {reason}\n{ds.utils.staff} Администратор: {interaction.author.name}', colour=disnake.Colour.green())
                embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                await interaction.response.send_message(embed=embed)
                await member.send(embed=embed)
                logger.debug(f'User {interaction.author.id} unmuted user {member.id} for reason: {reason} in guild {interaction.guild_id}.')
            else: 
                await interaction.response.send_message('Участник не находится в мьюте!', ephemeral=True)
                logger.warning(f'User {interaction.author.id} attempted to unmute user {member.id} in guild {interaction.guild_id}, but the user is not currently muted.')
        except disnake.errors.Forbidden:
            await interaction.response.send_message("Прости но у меня нету нужных прав для этого! Обратитесь к администратору сервера.", ephemeral=True)
            logger.warning(f'User {interaction.author.id} attempted to unmute user {member.id} in guild {interaction.guild_id}, but the bot lacks permissions.')

    @commands.slash_command(name='mute', description='Мьют человека', default_member_permissions=disnake.Permissions(administrator=True))
    @logs
    async def mute(self, interaction, member: disnake.Member = commands.Param(name='user', description='User to mute'), time:int = commands.Param(name='minute', description='Minute for mute this user'), reason: str = commands.Param(name='reason', description='Why are you mute this user', default='Причина не указана')):
        try:
            if member.id != interaction.author.id:
                if member.current_timeout is None:
                    time = datetime.now() + timedelta(minutes=int(time))
                    await self.udb.createtable()
                    await self.udb.adduser(interaction.author, interaction.guild_id)
                    await self.udb.adduser(member, interaction.guild_id)
                    await self.udb.updatedata(member, 0, 0, interaction.guild_id, all_timeouts=1)
                    await self.udb.updatedata(interaction.author, 0, 0, interaction.guild_id, aall_timeouts=1)
                    await self.rdb.updaterep(interaction.author.id, 3, interaction.guild_id)
                    await member.timeout(reason=reason, until=time)                   
                    cool_time = disnake.utils.format_dt(time, style='R')
                    embed = disnake.Embed(title='Мьют', description=f'{ds.utils.wow} Пользователю {member.mention} выдали мьют на {cool_time} \nПо причине: {reason} \n{ds.utils.staff}Администратор: {interaction.author.name}', colour=disnake.Colour.red())
                    embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
                    embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                    await interaction.response.send_message(embed=embed)
                    await member.send(embed=embed)
                    logger.debug(f'User {interaction.author.id} muted user {member.id} for reason: {reason} until {time} in guild {interaction.guild_id}.')
                else:
                    await interaction.response.send_message(f'Данный пользователь уже находится в мьюте! (Закончится в {disnake.utils.format_dt(member.current_timeout, style="T")})', ephemeral=True)
                    logger.warning(f'User {interaction.author.id} attempted to mute user {member.id} in guild {interaction.guild_id}, but the user is already muted until {disnake.utils.format_dt(member.current_timeout, style="T")}.')
            else: 
                await interaction.response.send_message('Вы не можете выдать самому себе наказание!', ephemeral=True)
                logger.warning(f'User {interaction.author.id} attempted to mute themselves in guild {interaction.guild_id}.')
        except disnake.errors.Forbidden:
            await interaction.response.send_message("Прости но у меня нету нужных прав для этого! Обратитесь к администратору сервера.", ephemeral=True)
            logger.warning(f'User {interaction.author.id} attempted to mute user {member.id} in guild {interaction.guild_id}, but the bot lacks permissions.')

@logs
def setup(bot):
    bot.add_cog(Timeout(bot))