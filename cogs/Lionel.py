from discord.ext import commands
import random
from LionelUtils import *

class LionelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="lionel")
    async def lionel(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(random.choice(["Oui oui je suis bien là.",
                                          "Oui ?",
                                          "Quoi ?",
                                          "Je suis là.",
                                          "Dis moi tout.",
                                          "Qu'est-ce que ?",
                                          "Présent !"]))

    @commands.command(name="testmenu")
    async def test_menu(self, ctx):
        options = {"1️⃣": "La première",
                   "2️⃣": "Peut-être la deuxième",
                   "3️⃣": "Qui sait, pourquoi pas la troisième",
                   "4️⃣": "La réponse D"}
        choice = await reaction_menu(self.bot, ctx, "Choisis une option :",  options)
        await ctx.send("Tu as choisi l'option %s : %s" % (choice, options[choice]))

    @commands.command(name="testmenu2")
    async def test_menu2(self, ctx):
        options = ["👍", "👎"]
        choice = await reaction_menu(self.bot, ctx, "Ceci est le deuxième menu de test, avec PAS des nombres. Tu le trouves bien ?",
                                          options)
        if choice[0] == "👍":
            await ctx.send("Merci, ça fait plaisir.")
        elif choice[0] == "👎":
            await ctx.send("Oh pourquoi ? 🙁")
        else:
            await ctx.send("Comment ça %s ???" % choice[0])

    @commands.command(name="yesorno")
    async def yesorno(self, ctx):
        if await yes_or_no(self.bot, ctx, "Ça va ou quoi ?"):
            await ctx.send("Coolos !")
        else:
            await ctx.send("Bah merde alors !")

    @commands.command(name="say")
    async def say(self, ctx, *, message):
        print("%s a utilisé !say pour me faire dire \"%s\"" % (ctx.author.display_name, message))
        await ctx.send(message)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(LionelCog(bot))
