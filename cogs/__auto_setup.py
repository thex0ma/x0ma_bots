# import disnake
# from disnake.ext import commands
# from discorddb import UserDataBase, ModerationDataBase
# from discordhelper import utils

# class TextInputModal(disnake.ui.Modal):
#     def __init__(self):
#         components = [
#             disnake.ui.TextInput(label="Запрет. слова", placeholder="Привет/ hello", custom_id="text", style=disnake.TextInputStyle.paragraph)
#         ]
#         super().__init__(title="", components=components)
#         self.udb = UserDataBase()
#         self.mdb = ModerationDataBase()
    
#     async def callback(self, interaction) -> None:
#         text = interaction.text_values['text']
#         await self.udb.createtable()
#         await self.mdb.updatelog(True, interaction.guild.id, text)
#         await interaction.response.send_message('Вы успешно настроили XMod', ephemeral=True)
        

# class TextInputButton(disnake.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)
        
#     @disnake.ui.button(label="Настроить", style=disnake.ButtonStyle.green, custom_id="start")
#     async def callback(self, button: disnake.ui.Button, inter: disnake.Interaction):
#         await inter.response.send_modal(TextInputModal())

# class AutoSetUp(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.udb = UserDataBase()
        
#     @commands.slash_command(name='setup_xmod', description='SetUp XMod')
#     async def text_input(self, inter):
#         embed = disnake.Embed(title="Настройка XMod", description="", colour=disnake.Colour.orange())
#         await self.udb.adduser(inter.author, inter.guild_id)
#         embed.add_field(name='Настройка', value=f'{utils.news} При нажатии кнопки "Настроить" вы должны ввести в поле "Запрет. слова" слова (кол-во не ограничено) отделять слова через ", " *Например:*\nПривет, как дела (на сервере будут запрещены слова Привет и как дела)\nКак только бот увидит в чате запрещенное слово он выдает мьют на 5 минут за каждое нарушение')
#         embed.set_footer(text=inter.author.name, icon_url=inter.author.avatar.url)
#         embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
#         view = TextInputButton()
#         await inter.response.send_message(embed=embed, view=view, ephemeral=True)
    
# def setup(bot):
#     bot.add_cog(AutoSetUp(bot))