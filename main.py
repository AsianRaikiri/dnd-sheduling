import os
from re import search
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
token = os.getenv('API-TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

player_ranks = {
    2: "Pearl",
    3: "Amethyst",
    4: "Amethyst",
    5: "Topaz",
    6: "Topaz",
    7: "Ruby",
    8: "Ruby",
    9: "Sapphire",
    10: "Sapphire",
    11: "Emerald",
    12: "Emerald",
    13: "Diamond",
    14: "Diamond",
    15: "Alexandrite",
    16: "Alexandrite",
    17: "Jade",
    18: "Jade",
    19: "Amber",
    20: "Amber",
    21: "Aquamarine",
    22: "Aquuamarine",
    23: "Aquamarine"
}


bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f"Ready to work as {bot.user.name}")

@bot.command()
async def update(ctx:commands.Context, *args):
    counter = 0
    nl = "\n"
    list_exists= False
    list_message = None
    dated_games = {}
    undated_games = []
    async for message in ctx.channel.history(limit=500):
        content = message.content
        players_raw = message.mentions
        players= []
        for user in players_raw: 
            players.append(user.display_name)
        if message.author == bot.user:
            list_exists = True
            list_message = message
        if "$list_messages" in content:
            await message.delete()
        content_list = content.splitlines()
        date = ""
        chars = []
        levels = []
        message_link = message.jump_url
        for line in content_list:
            if "@" in line and line.startswith("<"): 
                char_match = search(r">\s*\w+", line)
                if char_match: 
                    chars.append(char_match.group().removeprefix(">").strip())
                level_match = search(r" \d{1,2}$", line)
                if level_match: 
                    levels.append(int(level_match.group().strip()))

            if line.startswith("Date: "): 
                date_match=search(r"\d+/\d+/\d+", line)
                if date_match:
                    date = date_match.group()
            if line.lower().startswith("dm:") and "<" in line and len(players) > 0: 
                players.pop()
        uniquelevels = list(set(levels))
        uniquelevels.sort()
        chars.sort()
        ranks = []
        if levels and chars:
            counter += 1
            found_dm = False
            if message.reactions: 
                found_dm = True
            for level in uniquelevels:
                ranks.append(player_ranks[level])
            ranks = list(set(ranks))
            rank_string = "/".join(ranks)                
            char_string = ", ".join(chars)
            player_string = ", ".join(players)
            deprecated = ""
            if (found_dm):
                deprecated = "~~"
            dated_game = f"{nl}**Game**{nl}{deprecated}Date: {date}{deprecated}{nl}{deprecated}Ranks: {rank_string}{deprecated}{nl}{deprecated}Characters: {char_string}{deprecated}{nl}{deprecated}Players: {player_string}{deprecated}{nl}{deprecated}Link: {message_link}{deprecated}{nl}"
            undated_game = f"{nl}**Game**{nl}{deprecated}Ranks: {rank_string}{deprecated}{nl}{deprecated}Characters: {char_string}{deprecated}{nl}{deprecated}Players: {player_string}{deprecated}{nl}{deprecated}Link: {message_link}{deprecated}{nl}"
            if date != "":
                actual_date = datetime.strptime(date, "%m/%d/%Y")
                actual_date.month
                dated_games[actual_date] = dated_game
            else: 
                undated_games.append(undated_game)
    dated_games_string= ""
    if len(dated_games) > 0:
        sorted_dated_games = dict(sorted(dated_games.items()))
        current_month = ""
        for curr_date, value in sorted_dated_games.items():
            new_month = curr_date.strftime("%B")
            if current_month != new_month:
                current_month = new_month
                dated_games_string += f"## For {new_month}:{nl}"
            dated_games_string += value
            
        
    undated_games_string = "\n".join(undated_games)
    final_message = f'# This channel has {counter} games listed:{nl}{dated_games_string} {nl}## Without Correct Date:{undated_games_string}'
    if (list_exists): 
        await list_message.edit(content=final_message)
    else: 
        await ctx.send(final_message)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)