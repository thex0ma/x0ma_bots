import disnake
import logging
import utils.discordhelper as ds
from disnake.ext import commands
from utils.utils import logs

logger = logging.getLogger(__name__)

class Help(commands.Cog):
    @logs
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name='help', description='All commands')
    @logs
    async def help(self, interaction):
        embed = disnake.Embed(title='Все команды', colour=disnake.Colour.orange())
        embed.add_field('Модерация', '''
/**clear** - Удаляет сообщения (при удалении +100 сообщений. Сообщения будут удалятся не сразу) *
/**ban** - Забанить пользователя *
/**unban** - Разбанить пользователя (по айди) *
/**mute** - Выдать ограничения по чату пользователю (в минутах) * 
/**unmute** - Снять ограничения по чату пользователю *
/**warn** - Выдать предупреждение пользователю * 
/**remwarn** - Cнять предупреждение по айди (предупреждения) * 
/**warns** - Предупреждения пользователя * 
/**warnid** - Предупреждение по айди *
/**settings** - Настройки бота * 
                        ''')
        embed.add_field('Другое', '''
/**ping** - Задержка бота (в мс)
/**help** - Все команды бота
/**update** - Последнее обновление в боте
/**report** - Сообщение разработчику о ошибке
/**perstats** - Показывает все нужные боту права
/**avatar** - Показывает аватарку пользователя
/**stats** - Статистика бота
/**user** - Cтатистика пользователя
/**server** - Информация о сервере
			''')
        embed.add_field('Система Репутаций', '''
/**getrep** - Баланс репутации (если она не отключена)
                        ''')
        embed.add_field('Система Логов', '''
/**setup** - Настройка системы логов *
                        ''')
        embed.add_field('Контекст меню', value='Translate - Переводит с 109 языков на руский (Доступно с **XPlus**)\n\nКак открыть контекст меню? - Контекст меню можно открыть нажав на правую кнопку мышы по тексту и выбрать "Apps"\nС телефона - Зажмите пальцем на текст и выбираете "Взаемодействие" (или что то другое) ')
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed.set_footer(text='* - Требуется разрешение (Если у вас нету такой команды значит у вас недостаточно прав)')
        await interaction.response.send_message(embed=embed, ephemeral = True)
        logger.debug(f'Help command used by {interaction.author.id} in guild {interaction.guild_id}.')

@logs
def setup(bot):
    bot.add_cog(Help(bot))