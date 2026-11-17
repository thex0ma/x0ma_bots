# import disnake
# from disnake.ext import commands
# from discorddb import UserDataBase, LogDataBase

# class Logs(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.ldb = LogDataBase()
#         self.udb = UserDataBase()
    
#     @commands.Cog.listener()
#     async def on_message_delete(self, message):
#         values = await self.ldb.getlog(message.guild.id)
#         if values is not None and values[1] == 1:
#             channel = self.bot.get_channel(values[3])
#             embed = disnake.Embed(title='Удаление сообщений', description=f'Удалено сообщение:\n```{message.content}```', colour=disnake.Colour.red())
#             await channel.send(embed=embed)
#         else:
#             pass
#     @commands.Cog.listener()
#     async def on_message_edit(self, before, after):
#         if before.content != after.content:
#             values = await self.ldb.getlog(after.guild.id)
#             if values is not None and values[1] == 1:
#                 channel = self.bot.get_channel(values[3])
#                 embed = disnake.Embed(title='Изменение сообщения', description=f'Изменил: {after.author}', colour=disnake.Colour.orange())
#                 embed.add_field('Сообщение до', f'{before.content}')
#                 embed.add_field('Сообщение после', f'{after.content}')
#                 await channel.send(embed=embed)
#             else:
#                 pass
#         else:
#             pass
#     @commands.Cog.listener()
#     async def on_guild_channel_delete(self, channel):
#         values = await self.ldb.getlog(channel.guild.id)
#         if values is not None and values[1] == 1:
#             channels = self.bot.get_channel(values[3])
#             embed = disnake.Embed(title='Удаление канала', description=f'Канал под названием: {channel}\nВ Категории: {channel.category}', colour=disnake.Colour.red())
#             await channels.send(embed=embed)
#         else:
#             pass
#     @commands.Cog.listener()
#     async def on_guild_channel_create(self, channel):
#         values = await self.ldb.getlog(channel.guild.id)
#         if values is not None and values[1] == 1:
#             channels = self.bot.get_channel(values[3])
#             embed = disnake.Embed(title='Создание канала', description=f'Канал: {channel.mention}\nВ Категории: {channel.category}', colour=disnake.Colour.green())
#             await channels.send(embed=embed)
#         else:
#             pass
#     @commands.Cog.listener()
#     async def on_guild_role_delete(self, role):
#         values = await self.ldb.getlog(role.guild.id)
#         if values is not None and values[1]  == 1:
#             channel = self.bot.get_channel(values[3])
#             embed = disnake.Embed(title='Удаление роли', description=f'Роль под названием: {role.name}', colour=disnake.Colour.red())
#             await channel.send(embed=embed)
#         else:
#             pass
#     @commands.Cog.listener()
#     async def on_guild_role_create(self, role):
#         values = await self.ldb.getlog(role.guild.id)
#         if values is not None and values[1]  == 1:
#             channel = self.bot.get_channel(values[3])
#             embed = disnake.Embed(title='Создание роли', description=f'Роль: {role.mention}', colour=disnake.Colour.green())
#             await channel.send(embed=embed)
#         else:
#             pass
#     @commands.Cog.listener()
#     async def on_member_update(self, before, after):
#         values = await self.ldb.getlog(after.guild.id)
#         if values is not None and values[1]  == 1:
#             channel = self.bot.get_channel(values[3])
#             if before.nick == after.nick:
#                 pass
#             else:
#                 embed = disnake.Embed(title='Смена никнейма', description=f'Участнику: {after}\nСменили никнейм на: **{after.nick if after.nick != None else after}**\nБыл: **{before.nick if before.nick != None else before}**', colour=disnake.Colour.orange())
#                 await channel.send(embed=embed)
#             if before.avatar == after.avatar:
#                 pass
#             else:
#                 embed = disnake.Embed(title='Смена Аватара', description=f'Участник: {after}\nСменил аватар на:', colour=disnake.Colour.orange())
#                 embed.set_image(url=after.display_avatar.url)
#                 await channel.send(embed=embed)
#             if before.roles == after.roles:
#                 pass
#             else:
#                 a = before.roles
#                 b = after.roles
#                 roles = []
#                 try:
#                     for i in a:
#                         b.remove(i) # Додавання ролі
#                     for i in b:
#                         roles.append(i.mention)
#                     embed = disnake.Embed(title='Добавление ролей', description=f'Пользователю: {after}\nДобавили роли: {", ".join(roles)}', colour=disnake.Colour.green())
#                     await channel.send(embed=embed)
#                 except ValueError:
#                     for j in b:
#                         a.remove(j) # Видалення ролі
#                     a.pop(0)
#                     for j in a:
#                         roles.append(j.mention)
#                     embed = disnake.Embed(title='Удаление ролей', description=f'Пользователю: {after}\nУдалили роли: {", ".join(roles)}', colour=disnake.Colour.red())
#                     await channel.send(embed=embed)
                    
    
                
#         else:
#             pass
#     @commands.Cog.listener()
#     async def on_member_join(self, member):
#         values = await self.ldb.getlog(member.guild.id)
#         if values is not None and values[1]  == 1:
#             channel = self.bot.get_channel(values[3])
#             embed = disnake.Embed(title='Зашел пользователь', description=f'Зашел пользователь: {member}\nАккаунт был создан: {disnake.utils.format_dt(member.created_at)}', colour=disnake.Colour.red())
#             await channel.send(embed=embed)
#         else:
#             pass
#     @commands.Cog.listener()
#     async def on_member_ban(self, guild, user):
#         values = await self.ldb.getlog(guild.id)
#         if values is not None and values[1]  == 1:
#             channel = self.bot.get_channel(values[3])
#             embed = disnake.Embed(title='Бан', description=f'Заблокировали пользователя: {user}\nАккаунт был создан: {disnake.utils.format_dt(user.created_at)}', colour=disnake.Colour.red())
#             await channel.send(embed=embed)
#         else:
#             pass
#     @commands.Cog.listener()
#     async def on_member_unban(self, guild, user):
#         values = await self.ldb.getlog(guild.id)
#         if values is not None and values[1]  == 1:
#             channel = self.bot.get_channel(values[3])
#             embed = disnake.Embed(title='РазБан', description=f'Разблокировали пользователя: {user}\nАккаунт был создан: {disnake.utils.format_dt(user.created_at)}', colour=disnake.Colour.green())
#             await channel.send(embed=embed)
#         else:
#             pass
        
# def setup(bot):
#     bot.add_cog(Logs(bot))