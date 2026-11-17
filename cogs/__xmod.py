# import disnake
# from disnake.ext import commands
# from discorddb import ModerationDataBase
# import discordhelper as ds
# from datetime import datetime, timedelta

# class Moderation(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.mdb = ModerationDataBase()
        
#     @commands.Cog.listener()
#     async def on_message(self, message: disnake.Message):
#         if message.guild is not None:
#             database = await self.mdb.getlog(message.guild.id)
#             if database is not None and database[2] == 1:
#                 words = database[1]
#                 print(words)
#                 mutes = 0
#                 words = words.split(' ')
#                 print(words)
#                 for i in words:
#                     if i in message.content:
#                         mutes += 1
#                     else:
#                         pass
#                 if mutes > 0:
#                     time = mutes*5
#                     time = datetime.now() + timedelta(minutes=int(time))
#                     member = message.guild.get_member(message.author.id)
#                     moderator = False
#                     if member is not None:
#                         if member is not member.current_timeout:
#                             for roles in member.roles:
#                                 if roles.permissions.moderate_members:
#                                     moderator = True
#                                     break
#                             if moderator is False:
#                                 await member.timeout(reason=f'Автомодерация (XMOD): Нарушил правила чата х{mutes}', until=time)
#                                 cool_time = disnake.utils.format_dt(time, style='R')
#                                 embed = disnake.Embed(title='Мьют', description=f'{ds.utils.wow} Пользователю {member.mention} выдали мьют на {cool_time} \nПо причине: Нарушил правила чата **х{mutes}** \n{ds.utils.staff}Администратор: Автомодерация XMOD', colour=disnake.Colour.red())
#                                 await message.channel.send(embed=embed)
#                                 await member.send(embed=embed)
#                             else: pass
#                         else: pass
#                     else:
#                         embed = disnake.Embed(title='Ошибка', description=f'Сработала автомодерация. Но у бота либо отсутствует доступ к каналу либо пользователь не существует', colour=disnake.Colour.red())
#                         embed.set_footer(text='При этой ошибке просим обратится к модерации сервера либо к разработчику!')
#                         await message.channel.send(embed=embed)
            
# def setup(bot):
#     bot.add_cog(Moderation(bot))