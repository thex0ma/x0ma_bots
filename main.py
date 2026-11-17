import os
from dotenv import load_dotenv
import disnake
import logging
from disnake.ext import commands
from discorddb import UserDataBase
from utils.utils import logs

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | >. %(message)s",
    filename="logs/allbot.log",
    filemode="w",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
    force=True
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug("Creating bot instance")

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)



@bot.event
@logs
async def on_ready():
    game = disnake.Game('Тестовый бот команды XoMa bots | Developer')
    await bot.change_presence(status=disnake.Status.idle, activity=game)
    await UserDataBase().createtable()
    logger.info('Database table loaded successfully.')
    logger.info(f'Bot {bot.user.name} is ready and connected to Discord!')
    
@bot.listen()
@logs
async def on_guild_join(guild: disnake.Guild):
    logger.info(f'Bot has joined a new guild: {guild.name} (ID: {guild.id})')
    
@bot.listen()
@logs
async def on_guild_remove(guild: disnake.Guild):
    logger.warning(f'Bot has left guild: {guild.name} (ID: {guild.id})')

logger.debug("Loading cogs from the 'cogs' directory")
for file in os.listdir('./cogs'):
    if file.endswith('.py') and not file.startswith('__'):
        cog_name = f'cogs.{file[:-3]}'
        try:
            bot.load_extension(cog_name)
            logger.debug(f'Loaded cog: {cog_name}')
        except Exception:
            logger.exception(f'Failed to load cog: {cog_name}; skipping it.')

logger.debug("Loading views from the 'views' directory")
for file in os.listdir('./views'):
    if file.endswith('.py') and not file.startswith('__'):
        view_name = f'views.{file[:-3]}'
        try:
            bot.load_extension(view_name)
            logger.debug(f'Loaded view: {view_name}')
        except Exception:
            logger.exception(f'Failed to load view: {view_name}; skipping it.')
    

# Запуск бота

bot.run(os.getenv('TOKEN'))
