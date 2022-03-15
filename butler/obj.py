import discord

class RoleParam:
    def __init__(self, emoji, name, on_add, on_remove, role=None):
        self.emoji = emoji
        self.name = name
        self.on_add = on_add
        self.on_remove = on_remove
        self.role = role

class Category:
    inited = False

    poll = [
        RoleParam('🙂', 'Human', '{name} is a human being', '{name} is inhuman'),
        RoleParam('🐺', 'Beast', '{name} is a beast, hopefully a friendly one', '{name} is no longer a monster'),
        RoleParam('✨', 'Illusion', '{name} is an illusion', '{name} is now part of reality'),
        RoleParam('🧊', 'Inanimate object', '{name} is non-living matter', 'There is a chance that {name} is self conscious'),
        RoleParam('🚫', 'Void', '{name} is just another name for emptiness', '{name} now occupies space')
    ]

    description = ''
    posts = {}

    async def post(self, bot, ctx):
        if not self.inited:
            for item in self.poll:
                item.role = discord.utils.get(ctx.guild.roles, name=item.name)
            self.inited = True

        if not self.description:
            self.description = '*Select the category you belong to:*\n\n'
            for item in self.poll:
                self.description = self.description + item.emoji + ' - ' + item.role.mention + '\n'
        
        embed = discord.Embed(title='Change Identity', description=self.description)

        msg = await ctx.send(embed=embed)
        self.posts[msg.id] = {}

        for item in self.poll:
            await msg.add_reaction(item.emoji)



    async def add_role(self, message, channel, user, emoji):
        x = None
        for item in self.poll:
            if (str(emoji) == item.emoji):
                x = item
                break
        if x:
            await self.clear_roles(message, user)
            
            await user.add_roles(x.role)

            if user.id in self.posts[message.id]:
                self.posts[message.id][user.id].append(emoji)
            else:
                self.posts[message.id][user.id] = [emoji]

            await channel.send(x.on_add.format(name=user.mention))



    async def remove_role(self, channel, user, emoji):
        x = None
        for item in self.poll:
            if (str(emoji) == item.emoji):
                x = item
                break
        if x:
            await user.remove_roles(x.role)
            #await channel.send(x.on_remove.format(name=user.mention))


    async def clear_roles(self, message, user):
        rls = [role for role in user.roles]
        for item in self.poll:
            if item.role in rls:
                await user.remove_roles(item.role)
                
        if user.id in self.posts[message.id]:
            for e in self.posts[message.id][user.id]:
                await message.remove_reaction(e, user)
            self.posts[message.id][user.id] = []

    def has_message(self, message):
       return message in self.posts


