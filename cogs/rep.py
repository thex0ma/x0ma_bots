import disnake
import logging
from disnake.ext import commands
from discorddb import UserDataBase, PermissionDataBase
from utils.discordhelper import emoji, utils
import utils.discordhelper as ds
from utils.utils import logs

logger = logging.getLogger(__name__)

class Reputation(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        self.udb = UserDataBase()
        self.pdb = PermissionDataBase()
        
    @commands.slash_command(name='getrep', description='Get reputation')
    @logs
    async def getrep(self, interaction, user: disnake.Member = commands.Param(name='user', description='Member', default=None)):
        await self.udb.createtable()
        await self.udb.adduser(interaction.author, interaction.guild_id)
        if await self.pdb.getper(1, interaction.guild_id) == True:
            if user is None:
                user = interaction.author
            await self.udb.adduser(user, interaction.guild_id)
            get = await self.udb.getuser(user, interaction.guild_id)
            embed = disnake.Embed(title=f'Репутация {user}', description=f'{utils.staff} Пользователя {user.mention} **{get[3]}** {emoji.crown}', colour=disnake.Colour.orange())
            embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await interaction.response.send_message(embed=embed)
            logger.debug(f'Reputation command used by {interaction.author.id} in guild {interaction.guild_id}.')
        else:
            await interaction.response.send_message('Владелец сервера отключил данную функцию', ephemeral=True)
            logger.warning(f'User {interaction.author.id} attempted to use getrep command in guild {interaction.guild_id}, but the feature is disabled by the server owner.')
            
@logs
def setup(bot):
    bot.add_cog(Reputation(bot))