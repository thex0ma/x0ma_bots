import disnake
import logging
from disnake.ext import commands
from discorddb import PermissionDataBase, UserDataBase
from utils.utils import logs

logger = logging.getLogger(__name__)

class XPlus(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        self.pdb = PermissionDataBase()
        self.udb = UserDataBase()
    
    @commands.slash_command(name='xplus', guild_ids=[1071143492211978281])
    @logs
    async def xplus(self, interaction, bool:bool, server_id):
        await self.udb.createtable()
        await self.udb.adduser(interaction.user, server_id)
        await self.pdb.updateper(bool, 2, server_id)
        await interaction.response.send_message('ИксПлюс выдан серверу!', ephemeral=True)
        logger.info(f'XPlus command used by {interaction.user.id} in guild {interaction.guild_id} for server {server_id} with bool value {bool}.')
        
        
@logs
def setup(bot):
    bot.add_cog(XPlus(bot))
    