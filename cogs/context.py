import disnake 
import logging
from disnake.ext import commands
from googletrans import Translator
from discorddb import PermissionDataBase, UserDataBase
from utils.utils import logs

logger = logging.getLogger(__name__)

class ContextMenu(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        self.pdb = PermissionDataBase()
        self.udb = UserDataBase()
    @commands.message_command(name='Translate')
    @logs
    async def translate(self, interaction, message: disnake.Message):
        await self.udb.createtable()
        await self.udb.adduser(interaction.user, interaction.guild_id)
        if await self.pdb.getper(2, interaction.guild_id):
            trans = Translator()
            translation = trans.translate(text=message.content, dest='ru')
            await interaction.response.send_message(translation.text, ephemeral=True)
            logger.debug(f'Translate command used by {interaction.user.id} in guild {interaction.guild_id}.')
        else: 
            await interaction.response.send_message('Простите но для этого требуется **XPlus** который можно приобрести на оф. сервере **XoMa bots | Community**', ephemeral=True)
            logger.warning(f'User {interaction.user.id} attempted to use the translate command in guild {interaction.guild_id} without the subscription.')
    
@logs
def setup(bot):
    bot.add_cog(ContextMenu(bot))
    