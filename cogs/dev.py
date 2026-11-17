import disnake
import logging
import re
from disnake.ext import commands
from utils.utils import logs
from views.verif import RPCheck

logger = logging.getLogger(__name__)

class Dev(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name='use_description', description='Create description')
    @logs
    async def description(self, interaction, title: str = commands.Param(description='Title', default=None), text: str = commands.Param(description='Description')):
        if interaction.user.id == 843203650285076531:
            embed = disnake.Embed(title=title, description=text, color=disnake.Color.orange())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            embed.set_footer(text=f'used by dev. {interaction.author.name}', icon_url=interaction.author.avatar.url)
            await interaction.response.send_message(embed=embed)
            
    @commands.slash_command(description="Verification")
    async def button(self, inter: disnake.ApplicationCommandInteraction):

        embed = disnake.Embed(title='Верификация', description='Для верификации требуется изменить ник в данном Discord сервере как в игре (РП формат) Например Codie_Foster \nПосле смены никнейма требуется нажать на кнопку ниже', color=disnake.Color.green())        
        if inter.user.id == 843203650285076531:
            await inter.response.send_message(
                embed=embed,
                view=RPCheck(self.bot)
            )

            

def setup(bot):
    bot.add_cog(Dev(bot))