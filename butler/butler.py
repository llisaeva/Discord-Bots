import os
from random import Random
import discord
from discord.ext import commands
from tkn import BUTLER_TOKEN as TOKEN
from tkn import OWNER
from obj import Category

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix='!', owner_id=OWNER, intents=intents)

#TODO check if labrat is already logged in before trying to boot it
# same with butler

# ===================== Fields =============================
bot.categories = Category()
bot.animals = []
bot.myths = []

# ================ Terminal Messages =======================
# init message ---------------------------------------------
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# ================== User Commands =========================
# Greet bot ------------------------------------------------
@bot.command(pass_context=True)
async def hello(ctx):
    await ctx.message.add_reaction('👋')
    await ctx.send('Hello ' + ctx.author.mention + '!')

# List commands --------------------------------------------
@bot.command(pass_context=True)
async def cmds(ctx):
    embed = discord.Embed(title="Server Commands",
        description=
            "**!hello** - greet the robots\n"
            "**!change** - change what you are\n"
            "**!sos** - get help\n"
            "**!fruit** - play fruit jackpot with Labrat\n"
            "**!card** - get a random poker card\n"
            "**!question** - ask Butler a yes/no question *(he likes to lie sometimes)*\n"
            "**!animal** - get a random imaginary pet\n"
            "**!myth** - get a mythical animal, with a brief description\n"
            "**!game** - play a number guessing game with Labrat\n"
            "**!roles** - display all of categories of server members\n"
            "**!cmds** - post all commands (post this post)\n"
            "-------------------------------\n"
            "**Maker Commands**\n"
            "**!clear** - clear all messages in a thread\n"
            "**!die labrat** - kill Labrat\n"
            "**!die butler** - kill Butler\n"
            "**!boot labrat** - make Butler trigger a script on the server to run Labrat\n"
            "**!boot butler** - make Labrat trigger a script on the server to run Butler")

    await ctx.send(embed=embed)

# List all server roles ------------------------------------
@bot.command(pass_context=True)
async def roles(ctx):
    guild = ctx.guild
    roles = [role for role in guild.roles if role != ctx.guild.default_role]
    embed = discord.Embed(title="Server Roles", description=f"\n \n".join([role.mention for role in roles]))
    await ctx.send(embed=embed)

# Ask a yes/no question ------------------------------------
@bot.command(pass_context=True)
async def question(ctx, *args):
    random = Random()
    num = random.randrange(12)
    if num == 0:
        await ctx.send('Absolutely not.')
    elif num == 1:
        await ctx.send('NO!')
    elif num == 2:
        await ctx.send('Of course not, why would you ask that?')
    elif num == 3:
        await ctx.send('nope')
    elif num == 4:
        await ctx.send("I don't think so")
    elif num == 5:
        await ctx.send("Maybe?")
    elif num == 6:
        await ctx.send("I don't know, Google it")
    elif num == 7:
        await ctx.send("I think yes?")
    elif num == 8:
        await ctx.send("Yes")
    elif num == 9:
        await ctx.send("Yes, of course")
    elif num == 10:
        await ctx.send("Without a doubt, yes")
    elif num == 11:
        await ctx.send("YES! I'm surprised you didn't know that")

# Get a random animal --------------------------------------
@bot.command(pass_context=True)
async def animal(ctx):
    if not bot.animals:
        with open('./text/animals.txt') as f:
            bot.animals = [line.strip('*\n') for line in f]
    random = Random()
    word = bot.animals[random.randrange(len(bot.animals))]
    await ctx.send('You got: **' + word + '**')

# Get a random mythical animal -----------------------------
@bot.command(pass_context=True)
async def myth(ctx):
    if not bot.myths:
        with open('./text/mythical.txt') as f:
            bot.myths = [line.strip('\n') for line in f]
    random = Random()
    word = bot.myths[random.randrange(len(bot.myths))]
    await ctx.send('You got:\n' + word)

# Ask for help ---------------------------------------------
@bot.command(pass_context=True)
async def sos(ctx):
    with open('./img/chill-amigo.jpg', 'rb') as f:
        picture = discord.File(f)
        await ctx.channel.send(file=picture)

# Post a reaction poll (server roles) ----------------------
@bot.command(pass_context=True)
async def change(ctx, arg=None):
    if (arg == 'help'):
        with open('./img/identity.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.channel.send(file=picture) 
    else: 
        await bot.categories.post(bot, ctx)


# ================= Maker Commands =========================
# Kill bot -------------------------------------------------
@bot.command(pass_context=True)
@commands.is_owner()
async def die(ctx, arg):
    if arg=='butler':
        await ctx.send("Goodbye.")
        await bot.close()
        print('{0.user} has logged off'.format(bot))

@die.error
async def die_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You are not my maker')

# Boot other bot -------------------------------------------
@bot.command(pass_context=True)
@commands.is_owner()
async def boot(ctx, arg):
    if arg == 'labrat':
        os.system("labrat/compile.sh &")

@boot.error
async def boot_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You are not my maker')

# Clear all messages in channel ----------------------------
@bot.command(pass_context=True)
@commands.is_owner()
async def clear(ctx):
        await ctx.channel.delete()
        new_channel = await ctx.channel.clone(reason='Channel was purged')
        await new_channel.edit(position=ctx.channel.position)
        await new_channel.send('Channel was purged ☠️')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You are not my maker')


# ====================== Events ============================

@bot.event
async def on_raw_reaction_add(payload):
    user = payload.member
    emoji = payload.emoji
    message = payload.message_id
    channel = bot.get_channel(payload.channel_id)
    msg = await channel.fetch_message(message)

    if user != bot.user and bot.categories.has_message(message):
        await bot.categories.add_role(msg, channel, user, emoji)

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    emoji = payload.emoji
    message = payload.message_id
    channel = bot.get_channel(payload.channel_id)

    if user != bot.user and bot.categories.has_message(message):
        await bot.categories.remove_role(channel, user, emoji)

# ==========================================================

bot.run(TOKEN)