import discord
from api_keys import disc_keys
from collections import Counter
from string import punctuation
from discord.ext import commands

bot = commands.Bot(command_prefix='~ ')

@bot.event
async def on_ready():
    print('Runing ' + bot.user.name)

@bot.command()
async def send_message(ctx):
    await ctx.send('heyyo (:')

@bot.command()
async def test(ctx, arg1, arg2):
    await ctx.send('You passed {} and {}!'.format(arg1, arg2))

@bot.command()
async def collect(ctx, member: discord.Member = None):
    member = member or ctx.author

    indicator = await ctx.send('Collecting {}\'s data'.format(member.name))
    words = ""

    for channel in ctx.guild.text_channels:
        try:
            async for message in channel.history(limit=None):
                if message.author == member:
                    words += message.content.lower().translate(str.maketrans('', '', punctuation))
        except:
            pass

    # for channel in ctx.guild.text_channels: 
      #   async for message in channel.history(limit=None):
        #    if message.author == member:
         #       words += message.content.lower().translate(str.maketrans('', '', punctuation))
    words = words.split()
    await indicator.edit(content='Done collecting {}\'s data'.format(member.name))

    user_dict = Counter(words)

    filename = 'suite_life_data/' + str(member.name) + '.csv'
    with open(filename, 'w') as f:
        for key in user_dict.keys():
            f.write("%s,%s\n" % (key, user_dict[key]))

    print(user_dict)


bot.run(disc_keys["TOKEN"])