from discord.ext import commands
from LionelUtils import *


class RolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_role(self, ctx, user_input, scope):
        for role in scope:
            # Si le rôle existe (indépendant de la casse)
            if user_input.lower() == role.name.lower():
                return role

        for role in scope:  # En deux boucles pour que les rôles existants soient bien prioritaires

            # Si un rôle ressemblant existe
            if is_similar(user_input, role.name):
                if await yes_or_no(self.bot, ctx, "Est-ce que tu veux dire \"%s\" ?" % role.name):
                    return role
                else:
                    if await yes_or_no(self.bot, ctx, "Donc tu veux bien dire %s ?" % user_input):
                        return user_input
                    else:
                        await ctx.send("Ouais ben reviens me voir quand tu seras décidé alors hein. Merde.")
                        return None

        # Si le rôle n'existe pas
        return user_input  # ATTENTION c'est une string

    @commands.group(name="role")
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            options = {"➕": "M'ajouter un rôle",
                       "➖": "Me retirer un rôle",
                       "📄": "Voir la liste des rôles existants",
                       "👨‍👨‍👦‍👦": "Voir les membres d'un rôle"}
            choice1 = await reaction_menu(self.bot, ctx, "Tu veux faire quoi mon coco ?", options)

            def check(m):
                return m.author == ctx.author
            if choice1 == "➕":
                rolename = await cancellable_question(self.bot, ctx, "Tu veux quoi comme rôle ?")
                try:
                    await self.add_role(ctx, role_name=rolename)
                except AttributeError:
                    return
            elif choice1 == "➖":
                rolename = await cancellable_question(self.bot, ctx, "Lequel ?")
                try:
                    await self.remove_role(ctx, role_name=rolename)
                except AttributeError:
                    return
            elif choice1 == "📄":
                try:
                    await self.list_roles(ctx)
                except AttributeError:
                    return
            elif choice1 == "👨‍👨‍👦‍👦":
                rolename = await cancellable_question(self.bot, ctx, "De quel rôle tu veux voir la liste des membres ?")
                try:
                    if rolename is None:
                        return
                    else:
                        await self.list_roles(ctx, role=rolename)
                except AttributeError:
                    return

    # S'attribuer un rôle avec !role add rôle
    @role.command(name="add")
    async def add_role(self, ctx, *, role_name):
        new_role = await self.get_role(ctx, role_name, ctx.guild.roles)
        if new_role is None:
            return
        else:
            first = False
            if isinstance(new_role, str):
                new_role = await ctx.guild.create_role(name=new_role, mentionable=True)
                first = True
            if ctx.author in new_role.members:
                await ctx.send("Tu as déjà le rôle %s, couillon." % new_role.name)
                return
            await ctx.author.add_roles(new_role)
            message_text = "Voilà %s, tu as maintenant le rôle %s !" % (
                ctx.author.display_name, new_role.name)
            if first:
                message_text += " Tu es le premier, invite tes copains !"
            else:
                message_text += " Vous êtes %i. Je crois. Mais je suis pas fort en math" % len(new_role.members)
            message = await ctx.send(message_text)

            #me_too
            await message.add_reaction("🙋")
            me_too_people = []
            def check(react, user):
                print("CHECK")
                print(react.message.id == message.id and react.emoji == "🙋" and user.id != 648215524290854929)
                return react.message.id == message.id and react.emoji == "🙋" and user.id != 648215524290854929 and user != ctx.author
            while True:
                me_too_react = await self.bot.wait_for("reaction_add", check=check)
                me_too_people.append(me_too_react[1].display_name)
                await list(me_too_react)[1].add_roles(new_role)
                await message.edit(content=message_text + "\n(Ajouté : " + ", ".join(me_too_people) + ")")

                me_too_cancel = await self.bot.wait_for("reaction_remove", check=check) # TODO Use the same method as cancel with pending_tasks
                me_too_people.remove(me_too_cancel[1].display_name)
                await list(me_too_cancel)[1].remove_roles(new_role)
                if len(me_too_people) == 0:
                    await message.edit(content=message_text)
                else:
                    await message.edit(content=message_text + "\n(Ajouté : " + ", ".join(me_too_people) + ")")



            return

    # S'enlever un rôle avec !role remove rôle
    @role.command(name="remove")
    async def remove_role(self, ctx, *, role_name):
        role_to_remove = await self.get_role(ctx, role_name, ctx.author.roles)
        if role_to_remove is None:
            return
        elif role_to_remove in ctx.author.roles:
            await ctx.author.remove_roles(role_to_remove)
            if len(role_to_remove.members) == 0:
                await role_to_remove.delete()
                await ctx.send(
                    "Voilà %s, tu n'as maintenant plus le rôle %s. Plus personne ne l'a, d'ailleurs. Je le ferme." % (
                        ctx.author.display_name, role_to_remove.name))
                return
            else:
                await ctx.send(
                    "Voilà %s, tu n'as maintenant plus le rôle %s." % (ctx.author.display_name, role_to_remove.name))
                return
        else:
            await ctx.send("Tu n'as pas le rôle %s, andouille." % role_to_remove)

    # Voir la liste des rôles avec !role list /// Voir les membres d'un rôle avec !role list rôle
    @role.command(name="list")
    async def list_roles(self, ctx, *, role=None):
        if role is None:
            roles_list = ""
            for role in ctx.guild.roles:
                roles_list = roles_list + ("%s (%i membres)\n" % (role.name, len(role.members)))
            message = await ctx.send("Voici la liste des rôles qui existent ici :"
                                     "\n```\n%s\n```"
                                     "Cette liste est peut-être très longue, pour éviter le spam tu peux l'effacer avec 🧽." % str(roles_list))
            await sponge(self.bot, ctx, message,
                         "Voici la liste des rôles qui existent ici :"
                         "\n```\nListe des rôles effacée\n```"
                         "Cette liste est peut-être très longue, pour éviter le spam tu peux l'effacer avec 🧽.")

        else:
            in_role = await self.get_role(ctx, role, ctx.guild.roles)
            if isinstance(in_role, str):
                await ctx.send("Le rôle %s n'existe pas." % in_role)
            elif in_role is None:
                return
            else:
                members_list = ""
                for member in in_role.members:
                    members_list = members_list + member.display_name + "\n"
                await ctx.send("Voici la liste des gens dans %s :\n```\n%s\n```" % (in_role.name, members_list))

    # Drôle
    @role.command(name="ass")
    async def ass(self, ctx):
        await ctx.send("Non mais là c'est indécent. Autocorrect ou pas autocorrect.")

    # Rappel
    @commands.command(name="add")
    async def add(self, ctx):
        await ctx.send("Non c'est `!role add`.")

    # Pour Sam
    @commands.command(name="roll")
    async def add(self, ctx):
        await ctx.send("ROLE bordel, pas roll. Fais un effort marde.")


def setup(bot):
    bot.add_cog(RolesCog(bot))
