import disnake
import logging
from disnake.ext import commands
import utils.discordhelper as ds
from discorddb import UserDataBase, ReputationDataBase
from utils.utils import logs

logger = logging.getLogger(__name__)

class Kick(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        self.udb = UserDataBase()
        self.rdb = ReputationDataBase()
    
    @commands.slash_command(name='kick', description='kick user', default_member_permissions=disnake.Permissions(kick_members=True))
    @logs
    async def kick(self, interaction, user: disnake.Member = commands.Param(name='user', description='User'), reason: str = commands.Param(default='Причина не указана', name='reason', description='Reason')):
        try:
            if interaction.author.id != user.id:
                await self.udb.createtable()
                await self.udb.adduser(interaction.author, interaction.guild_id)
                await self.udb.adduser(user, interaction.guild_id)
                await self.udb.updatedata(user, 0, 0, interaction.guild_id, all_kicks=1)
                await self.udb.updatedata(interaction.author, 0, 0, interaction.guild_id, aall_kicks=1)
                await self.rdb.updaterep(interaction.author.id, 5, interaction.guild.id)
                embed = disnake.Embed(title='Кик', description=f'{ds.utils.staff} Администратор: {interaction.author.mention}\n{ds.utils.info} Кикнул Пользователя {user.mention}\n{ds.utils.wow} Причина: {reason}', colour=disnake.Colour.red())
                embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                await user.send(embed=embed)
                await user.kick(reason=reason)
                await interaction.response.send_message(embed=embed)
                logger.info(f'User {interaction.author.id} kicked user {user.id} for reason: {reason} in guild {interaction.guild_id}.')
            else: 
                await interaction.response.send_message('Вы не можете выдать самому себе наказание!', ephemeral=True)
                logger.warning(f'User {interaction.author.id} attempted to kick themselves in guild {interaction.guild_id}.')
        except disnake.errors.Forbidden:
            await interaction.response.send_message("Прости но у меня нету нужных прав для этого!", ephemeral=True)
            logger.warning(f'User {interaction.author.id} attempted to kick a user in guild {interaction.guild_id} without the necessary permissions.')


@logs
def setup(bot):
    bot.add_cog(Kick(bot))