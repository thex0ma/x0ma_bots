import aiosqlite as sq
import disnake
import logging
from datetime import datetime
from typing import Union
from utils.utils import logs


logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

class UserDataBase:
    @logs
    def __init__(self):
        self.db = 'database.db'
    @logs
    async def createtable(self):
        async with sq.connect(self.db) as db:
            cur = await db.cursor()
            
            await cur.execute('''CREATE TABLE IF NOT EXISTS users(
                id INTEGER,
                money INTEGER,
                warns INTEGER,
                reputation INTEGER,
                guild INTEGER,
                premium INTEGER, 
                allwarns INTEGER,
                allbans INTEGER,
                alltimeouts INTEGER,
                allkicks INTEGER,
                aallwarns INTEGER,
                aallbans INTEGER,
                aalltimeouts INTEGER,
                aallkicks INTEGER
                )''')
            await cur.execute('''CREATE TABLE IF NOT EXISTS warns(
                count INTEGER,
                reason TEXT,
                who INTEGER,
                timestamp INTEGER, 
                admins INTEGER,
                guild INTEGER
                )''')
            await cur.execute('''CREATE TABLE IF NOT EXISTS sys(
                idsys INTEGER,
                count INTEGER,
                guild INTEGER
                )''')
            await cur.execute('''CREATE TABLE IF NOT EXISTS permission(
                perid INTEGER,
                turn INTEGER,
                guild INTEGER
                )''')
            await cur.execute('''CREATE TABLE IF NOT EXISTS logs(
                logid INTEGER,
                turn INTEGER,
                guild INTEGER
                )''')
            await cur.execute('''CREATE TABLE IF NOT EXISTS xmod(
                guild INTEGER,
                words TEXT,
                turn INTEGER
                )''')
            await db.commit()
            logger.debug("Database tables loaded successfully.")
    
    @logs
    async def adduser(self, user: Union[disnake.User, disnake.Member] , guild_id:int):
        async with sq.connect(self.db) as db:
            logger.debug(f"Adding user {user.id} to the database for guild {guild_id}")
            cur = await db.cursor()
            await cur.execute(f'SELECT * FROM users WHERE guild = {guild_id} and id = {user.id}')
            if await cur.fetchone() is None:
                await cur.execute(f"INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (user.id, 0, 0, 0, guild_id, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                logger.info(f"User {user.id} added to the database for guild {guild_id}")
            await cur.execute(f'SELECT count FROM sys WHERE idsys = {0} and guild = {guild_id}')
            if await cur.fetchone() is None:
                await cur.execute(f"INSERT INTO sys VALUES (?,?,?)", (0, 1, guild_id))
            await cur.execute(f'SELECT turn FROM permission WHERE perid = {1} and guild = {guild_id}')
            if await cur.fetchone() is None:
                await cur.execute(f"INSERT INTO permission VALUES (?,?,?)", (1, 0, guild_id)) 
            await cur.execute(f'SELECT turn FROM permission WHERE perid = {2} and guild = {guild_id}')
            if await cur.fetchone() is None:
                await cur.execute(f"INSERT INTO permission VALUES (?,?,?)", (2, 0, guild_id)) 
            await cur.execute(f'SELECT turn FROM logs WHERE logid = {0} and guild = {guild_id}')
            if await cur.fetchone() is None:
                await cur.execute('INSERT INTO logs VALUES (?,?,?)', (0, 0, guild_id))
            await cur.execute(f'SELECT turn FROM xmod WHERE guild = {guild_id}')
            if await cur.fetchone() is None:
                await cur.execute('INSERT INTO xmod VALUES (?,?,?)', (guild_id, 'NONE', 0))
                logger.info(f"Default settings of guild {guild_id} added to the database.")
            await db.commit()
    @logs
    async def getuser(self, user: Union[disnake.Member, disnake.User], guild_id:int):
        async with sq.connect(self.db) as db:
            cur = await db.cursor()
            await cur.execute(f'SELECT * FROM users WHERE id = {user.id} and guild = {guild_id}')
            logger.debug(f"Fetching data for user {user.id} in guild {guild_id}")
            return await cur.fetchone()
    
    @logs
    async def updatedata(self, user: Union[disnake.Member, disnake.User],money:int,premium:int,guild_id:int, all_warns:int = 0, all_kicks:int = 0, all_bans:int = 0, all_timeouts:int = 0, aall_warns:int = 0, aall_kicks:int = 0, aall_bans:int = 0, aall_timeouts:int = 0):
        async with sq.connect(self.db) as db:
            cur = await db.cursor()
            await cur.execute(f'UPDATE users SET money = money + {money}, premium = {premium}, allwarns = allwarns + {all_warns}, allbans = allbans + {all_bans}, allkicks = allkicks + {all_kicks}, alltimeouts = alltimeouts + {all_timeouts}, aallwarns = aallwarns + {aall_warns}, aallbans = aallbans + {aall_bans}, aallkicks = aallkicks + {aall_kicks}, aalltimeouts = aalltimeouts + {aall_timeouts} WHERE id = {user.id} and guild = {guild_id}')
            logger.info(f"Data updated for user {user.id} in guild {guild_id}")
            await db.commit()
            
class WarnDataBase:
    @logs
    def __init__(self) -> None:
        self.db = 'database.db'
    
    @logs
    async def warn(self, user:disnake.Member, admin, reason:str, guild_id:int):
        async with sq.connect(self.db) as db:
            cur = await db.cursor()
            await cur.execute(f'SELECT count FROM sys WHERE idsys = {0} and guild = {guild_id}')
            values = await cur.fetchone()
            await cur.execute(f'UPDATE users SET warns = warns + {1} WHERE id = {user.id} and guild = {guild_id}')
            await cur.execute(f'UPDATE sys SET count = {values[0]+1} WHERE idsys = {0} and guild = {guild_id}')
            await cur.execute(f'INSERT INTO warns VALUES (?,?,?,?,?,?)', (values[0], reason, user.id, datetime.now(), admin.id, guild_id))
            logger.info(f"Warning added for user {user.id} in guild {guild_id} (warnid: {values[0]+1})")
            await db.commit()
    
    @logs
    async def getwarn(self, user: disnake.Member, guild_id:int):
        async with sq.connect(self.db) as db:
            warns = []
            cur = await db.cursor()
            async for values in await cur.execute(f'SELECT * FROM warns WHERE who = {user.id} and guild = {guild_id}'):
                warns.append(values)
                logger.debug(f"Fetched warning for user {user.id} in guild {guild_id}")
            return warns
        
    @logs
    async def getwarnbyid(self, id:int, guild_id:int):
        async with sq.connect(self.db) as db:
            cur = await db.cursor()
            async for i in await cur.execute(f'SELECT * FROM warns WHERE count = {id} and guild = {guild_id}'):
                logger.debug(f"Fetched warning by ID {id} in guild {guild_id}")
                return i
            
    @logs
    async def remwarn(self, id:int, guild_id:int):
        try:
            async with sq.connect(self.db) as db:
                cur = await db.cursor()
                await cur.execute(f'DELETE FROM warns WHERE count = {id} and guild = {guild_id}')
                await db.commit()
                logger.info(f"Warning with ID {id} removed from guild {guild_id}")
        except Exception as e:
            logger.error(f"Error occurred while removing warning: {e[:25]}...")
            
class ReputationDataBase:
    @logs
    def __init__(self):
        self.db = 'database.db'
    
    @logs
    async def updaterep(self, id, rep:int, guild_id:int):
        async with sq.connect(self.db) as db:
            cur = await db.cursor()
            await cur.execute(f'UPDATE users SET reputation = reputation + {rep} WHERE id = {id} and guild = {guild_id}')
            await db.commit()
            logger.debug(f"Reputation updated for user {id} in guild {guild_id} by {rep} points")
class PermissionDataBase:
    @logs
    def __init__(self):
        self.db = 'Discord/database.db'
        
    @logs
    async def updateper(self, bool: bool, perid:int, guild_id:int):
        async with sq.connect(self.db) as db:
            cur = await db.cursor()
            if bool == True:
                await cur.execute(f'UPDATE permission SET turn = {1} WHERE perid = {perid} and guild = {guild_id}')
            if bool == False: 
                await cur.execute(f'UPDATE permission SET turn = {0} WHERE perid = {perid} and guild = {guild_id}')
            await db.commit()
            logger.info(f"Permission updated for ID {perid} in guild {guild_id}")
                
    @logs
    async def getper(self, perid:int,guild_id:int):
        async with sq.connect(self.db) as db:
            cur = await db.cursor()
            await cur.execute(f'SELECT turn FROM permission WHERE perid = {perid} and guild = {guild_id}')
            value = await cur.fetchone()
            logger.debug(f"Permission fetched for ID {perid} in guild {guild_id}")
            if value is not None and value[0] == 0:
                return False
            if value is not None and value[0] == 1:
                return True
            
class LogDataBase:
    @logs
    def __init__(self):
        self.db = 'database.db'
    
    @logs
    async def updatelog(self, turn:bool, guild_id:int):
        async with sq.connect(self.db) as db:
            cur = await db.cursor()
            if turn is False:
                await cur.execute(f'UPDATE logs SET turn = {0} WHERE logid = {0} and guild = {guild_id}')
            else:
                await cur.execute(f'UPDATE logs SET turn = {1}, guild = {guild_id} WHERE logid = {0} and guild = {guild_id}')
            await db.commit()
    @logs
    async def getlog(self, guild_id:int):
        async with sq.connect(self.db) as db:
            cur = await db.cursor()
            await cur.execute(f'SELECT * FROM logs WHERE logid = {0} and guild = {guild_id}')
            return await cur.fetchone()
    
class ModerationDataBase:
    @logs
    def __init__(self):
        self.db = 'database.db'
        
    @logs
    async def updatelog(self, turn:bool, guild_id, words:str):
        async with sq.connect(self.db) as db:
            cur = await db.cursor()
            if turn is False:
                await cur.execute(f'UPDATE xmod SET turn = {0} WHERE guild = {guild_id}')
            else:
                await cur.execute(f'UPDATE xmod SET turn = {1}, words = {words}, WHERE guild = {guild_id}')
            await db.commit()
    @logs
    async def getlog(self, guild_id:int):
        async with sq.connect(self.db) as db:
            cur = await db.cursor()
            await cur.execute(f'SELECT * FROM xmod WHERE guild = {guild_id}')
            return await cur.fetchone() 