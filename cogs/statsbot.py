import disnake
import logging
from disnake.ext import commands
import utils.discordhelper as ds
from utils.utils import logs

logger = logging.getLogger(__name__)

class Stats_bot(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name='stats', description='Info about bot')
    @logs
    async def statsbot(self, interaction):
        members = 0
        guilds = 0
        ping = int(self.bot.latency*1000)
        for i in self.bot.guilds:
            guilds += 1
            members += i.member_count
            
        embed = disnake.Embed(title=f'Статистика {self.bot.user.name}', description=f'Серверов: **{guilds}**\n\nПользователей: **{members}**\n\nПинг: **{str(ping)}** ms\n\nДискорд-Сервер: [XoMa bots | Community](https://discord.gg/mpBdan6Jr7)', colour=disnake.Colour.orange())
        embed.set_footer(text=interaction.author.name, icon_url=interaction.author.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)
        logger.debug(f'Stats command used by {interaction.author.id} in guild {interaction.guild_id}.')
        
@logs
def setup(bot):
    bot.add_cog(Stats_bot(bot))