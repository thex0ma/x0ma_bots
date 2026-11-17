import disnake
import logging
from disnake.ext import commands
import utils.discordhelper as ds
from discorddb import PermissionDataBase, UserDataBase
from utils.utils import logs

logger = logging.getLogger(__name__)

class Settings(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        self.pdb = PermissionDataBase()
        self.udb = UserDataBase()

    @commands.slash_command(name='settings', description='Set Bot settings')
    @logs
    async def settings(self, interaction):
        await self.udb.createtable()
        await self.udb.adduser(interaction.author, interaction.guild_id)
        embed = disnake.Embed(colour=disnake.Colour.green())
        embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        if await self.pdb.getper(1, interaction.guild_id) == True:
            embed.add_field(name='Настройки бота',value=f'{ds.utils.wow} | Система Репутации: {ds.emoji.yes}')
            if interaction.guild.owner_id == interaction.author.id:
                await interaction.response.send_message(embed=embed, ephemeral=True, components=[
                    disnake.ui.Button(label=f'Выключить', style=disnake.ButtonStyle.danger, custom_id='off')
                ])
                logger.debug(f'Owner {interaction.author.id} accessed settings command in guild {interaction.guild_id}.')
            else:
                await interaction.response.send_message(embed=embed)
                logger.debug(f'User {interaction.author.id} checked settings command in guild {interaction.guild_id}.')
        if await self.pdb.getper(1, interaction.guild_id) == False:
            embed.add_field(name='Настройки бота',value=f'{ds.utils.wow} | Система Репутации: {ds.emoji.no}')
            if interaction.guild.owner_id == interaction.author.id:
                await interaction.response.send_message(embed=embed, ephemeral=True,components=[
                    disnake.ui.Button(label=f'Включить', style=disnake.ButtonStyle.success, custom_id='on')
                ])
                logger.debug(f'Owner {interaction.author.id} accessed settings command in guild {interaction.guild_id}.')
            else:
                await interaction.response.send_message(embed=embed)
                logger.debug(f'User {interaction.author.id} checked settings command in guild {interaction.guild_id}.')
    @commands.Cog.listener()
    @logs
    async def on_button_click(self, interaction):
        if interaction.component.custom_id not in ['on','off']:
            logger.warning(f'User {interaction.author.id} clicked an unknown button with custom_id {interaction.component.custom_id} in guild {interaction.guild_id}.')
        if interaction.component.custom_id == 'off':
            await self.pdb.updateper(False, 1, interaction.guild_id)
            await interaction.response.send_message('Вы отключили Систему репутации ', ephemeral=True)
            logger.debug(f'Owner {interaction.author.id} disabled reputation system in guild {interaction.guild_id}.')
        if interaction.component.custom_id == 'on':
            await self.pdb.updateper(True, 1, interaction.guild_id)
            await interaction.response.send_message('Вы включили Систему репутации ', ephemeral=True)
            logger.debug(f'Owner {interaction.author.id} enabled reputation system in guild {interaction.guild_id}.')
@logs
def setup(bot):
    bot.add_cog(Settings(bot))