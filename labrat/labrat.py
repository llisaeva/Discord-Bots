import os
from random import Random
import discord
from discord.ext import commands
import time
import math
from tkn import LABRAT_TOKEN as TOKEN
from tkn import OWNER

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix='!', owner_id=OWNER, intents=intents)

bot.number = 0
bot.numberGame = False
bot.time = time.time()

# init message
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# Greet User (!hello)
@bot.command(pass_context=True)
async def hello(ctx):
    await ctx.message.add_reaction('👋')
    await ctx.send('Hello ' + ctx.author.mention + '!')

@bot.command(pass_context=True)
@commands.is_owner()
async def die(ctx, arg):
    if arg=='labrat':
        await ctx.send("Goodbye.")
        await bot.close()
        print('{0.user} has logged off'.format(bot))

@die.error
async def die_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You are not my maker')


@bot.command(pass_context=True)
async def fruit(ctx):
    fruit = ['🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍒', '🍑', '🍍', '🥥', '🥝']
    random = Random()
    x = len(fruit)
    slot1 = fruit[random.randrange(x)]
    slot2 = fruit[random.randrange(x)]
    slot3 = fruit[random.randrange(x)]

    pair = ["You got a pair. Almost there, try again.", "Dang, only two match. Better try harder."]

    fail = [
        "Not even a single match, shame.", 
        "You failed.",
        "Boo, try harder.",
        "You got junk.",
        "Today is not your lucky day.",
        "Here is a clover 🍀, maybe it will help you next time."]

    await ctx.send(slot1 + slot2 + slot3)

    if slot1 == slot2 == slot3:
        await ctx.message.add_reaction('🏆')
        await ctx.send("JACKPOT!! That does not make you special though, just luck")
    elif slot1 == slot2 or slot1 == slot3 or slot2 == slot3:
        await ctx.send(pair[random.randrange(len(pair))])
    else:
        await ctx.send(fail[random.randrange(len(fail))])

@bot.command(pass_context=True)
async def card(ctx):
    rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'K', 'Q']
    suit = [':clubs: - Club', ':diamonds: - Diamond', ':hearts: - Heart', ':spades: - Spade' ]
    random = Random()
    await ctx.send(rank[random.randrange(len(rank))] + ' ' + suit[random.randrange(len(suit))])


@bot.command(pass_context=True)
@commands.is_owner()
async def boot(ctx, arg):
    if arg == 'butler':
        os.system("butler/compile.sh &")

@boot.error
async def boot_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You are not my maker')


# ======================= Game Jam =========================

@bot.command(pass_context=True)
async def game(ctx):
    random = Random()
    bot.numberGame = True
    bot.number = random.randrange(1001)
    await ctx.send('**Guess a number in the range [0, 1000]**\n*You have 100 seconds!*\nUse **!guess** *number*')
    bot.time = time.time()

@bot.command(pass_context=True)
async def guess(ctx, arg):
    number = bot.number
    timestamp = time.time()
    if bot.numberGame:
        time_left = timestamp - bot.time
        if time_left < 100:
            if arg.isnumeric():
                num = int(arg)
                if num == number:
                    bot.numberGame = False
                    await ctx.message.add_reaction('🥳')
                    await ctx.send("That's right, you guessed it!")
                else:
                    dif = abs(number - num)
                    if dif > 500:
                        await ctx.send("Far away, try again")
                    elif dif > 300:
                        await ctx.send("Not near, but not too far")

                    elif dif > 100:
                        if number - num > 0:
                            await ctx.send("Getting closer, number is larger")
                        else:
                            await ctx.send("Getting closer, number is smaller")
    
                    elif dif > 50:
                        if number - num > 0:
                            await ctx.send("Near, number is larger")
                        else:
                            await ctx.send("Near, number is smaller")
    
                    elif dif > 10:
                        if number - num > 0:
                            await ctx.send("Almost there, number is larger")
                        else:
                            await ctx.send("Almost there, number is smaller")

                    elif dif > 5:
                        if number - num > 0:
                            await ctx.send("Almost got it! Its a bit larger")
                        else:
                            await ctx.send("Almost got it! Its a bit smaller")
                    else:
                        if number - num > 0:
                            await ctx.send("Just a bit larger")
                        else:
                            await ctx.send("A little smaller")

                    await ctx.send('You have ' + str(100 - int(math.ceil(time_left))) + ' seconds remaining.')

            else:
                await ctx.send("Guess must be a number")

        else:
            await ctx.send("Out of time... Try again.")
            bot.numberGame = False

    else:
        await ctx.send("You must start the game with !game before guessing.")

# ==========================================================
bot.run(TOKEN)