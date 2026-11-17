import disnake
import logging
from discorddb import ReputationDataBase, UserDataBase
from disnake.ext import commands
from utils.utils import logs

logger = logging.getLogger(__name__)

class Clear(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        self.rdb = ReputationDataBase()
        self.udb = UserDataBase()
    @commands.slash_command(name='clear', description='Очистка чата', default_member_permissions=disnake.Permissions(manage_messages=True))
    @logs
    async def clear(self, interaction, amount: int = commands.Param(name='amount', description='Amount of delete message')):
        try:
            if amount <= 0:
                await interaction.response.send_message('Вы не можете удалить 0 или меньше сообщений', ephemeral=True)
                logger.warning(f'User {interaction.author.id} attempted to clear {amount} messages in guild {interaction.guild_id}, which is not a valid amount.')
            else:
                await self.udb.createtable()
                await self.udb.adduser(interaction.author, interaction.guild_id)
                await self.rdb.updaterep(interaction.author.id, 1, interaction.guild_id)
                await interaction.channel.purge(limit=amount)
                embed = disnake.Embed(title='Удалить', description=f'Удаленно {amount}/{amount}', colour=disnake.Colour.orange())
                embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
                embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                logger.debug(f'User {interaction.author.id} cleared {amount} messages in guild {interaction.guild_id}.')
        except disnake.errors.Forbidden:
            await interaction.response.send_message("Прости но у меня нету нужных прав для этого! Обратитесь к администратору сервера.", ephemeral=True)
            logger.error(f'User {interaction.author.id} attempted to clear messages in guild {interaction.guild_id} but the bot lacks permissions.')
@logs
def setup(bot):
    bot.add_cog(Clear(bot))