"""
Contains the Message Collector discord bot that is used to
pull user message data from Discord and turn it into individual user
CSVs.
"""
from collections import Counter
from string import punctuation
from discord.ext import commands
import discord
from scrape_data import dict_to_csv
from api_keys import disc_keys


bot = commands.Bot(command_prefix='~ ')


@bot.event
async def on_ready():
    """
    As soon as the bot starts up, print a message indicating that it
    successfully started.

    Args:
        None.
    Returns:
        None.
    """
    print(f"Runing {bot.user.name}")


@bot.command()
async def collect(ctx, member: discord.Member = None):
    """
    When called, collects all message data of the listed member; if there is no
    listed member, all messages of the individual who sends the command will be
    collected.

    Args:
        ctx: A context representing data regarding where the command was sent,
            and who sent the command.
        member: A Member representing an individual in the discord server.
    Returns:
        None.
    """
    member = member or ctx.author

    indicator = await ctx.send(f"Collecting {member.name}\'s data")
    words = ""

    for channel in ctx.guild.text_channels:
        try:
            async for message in channel.history(limit=None):
                if message.author == member:
                    words += message.content.lower().translate(str.maketrans(
                        '', '', punctuation))
        except discord.Forbidden:
            pass

    words = words.split()
    await indicator.edit(content=f"Done collecting {member.name}\'s data")

    user_dict = Counter(words)

    filename = f"{member.name}.csv"
    dict_to_csv(user_dict, filename)

bot.run(disc_keys["TOKEN"])
