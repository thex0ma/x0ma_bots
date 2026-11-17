import disnake
import logging
from disnake.ext import commands
from utils.utils import logs

logger = logging.getLogger(__name__)

class Avatar(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name='avatar', description='User Avatar')
    @logs
    async def avatar(self, interaction, member: disnake.Member = commands.Param(default=None, description='User')):
        user = member or interaction.author
        embed = disnake.Embed(title='Аватарка', color=0x2f3136)
        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        logger.debug(f'Avatar command used by {interaction.author.name} in server {interaction.guild.name} for user {user.name}.')
        await interaction.response.send_message(embed=embed)
        
@logs
def setup(bot):
    bot.add_cog(Avatar(bot))