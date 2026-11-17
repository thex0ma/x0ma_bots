import disnake
import logging
import re
from disnake.ext import commands
from utils.utils import logs

logger = logging.getLogger(__name__)

class RPCheck(disnake.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @disnake.ui.button(
        style=disnake.ButtonStyle.green,
        label="Верификация",
        emoji="✅",
        custom_id="rp_check_button"
    )
    @logs
    async def check_rp(self,button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer(ephemeral=True)
        nick = inter.author.nick
        pattern = r"^[A-Z][a-z]+_[A-Z][a-z]+$"
        
        if nick and re.fullmatch(pattern, nick):
            embed = disnake.Embed(title='Верификация', description='Вы успешно верифицированы!', color=disnake.Color.green())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await inter.author.remove_roles(inter.guild.get_role(1210704332773920828))
            await inter.author.add_roles(inter.guild.get_role(1210704332773920828))
            await inter.followup.send(embed=embed, ephemeral=True)
            logger.info(f'User {inter.author.id} has been verified successfully in guild {inter.guild.id}.')
        
        else:
            embed = disnake.Embed(title='Верификация', description='Произошла ошибка при верификации! Попробуйте изменить никнейм на РП формат', color=disnake.Color.red())
            embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await inter.followup.send(embed=embed, ephemeral=True)
            logger.info(f'User {inter.author.id} failed to verify in guild {inter.guild.id}.')
@logs          
def setup(bot):
    async def register_view():
        if not getattr(bot, "_rp_view_registered", False):
            bot.add_view(RPCheck(bot))
            bot._rp_view_registered = True

    bot.add_listener(register_view, "on_ready")