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
    await ctx.message.delete()
    counter = 0
    nl = "\n"
    shedule_exists = False
    shedule_message = None
    dated_games = {}
    undated_games = []
    async for message in ctx.channel.history(limit=500):
        content = message.content
        if message.author == bot.user:
            shedule_exists = True
            shedule_message = message
        players= []
        message_list = content.splitlines()
        date = ""
        characters = []
        levels = []

        message_link = message.jump_url
        players_objects = message.mentions
        for user in players_objects: 
            players.append(user.display_name)

        for line in message_list:
            if "@" in line and line.startswith("<"): 
                char_match = search(r">\s*\w+", line)
                if char_match: 
                    characters.append(char_match.group().removeprefix(">").strip())
                level_match = search(r" \d{1,2}$", line)
                if level_match: 
                    levels.append(int(level_match.group().strip()))

            if line.startswith("Date: "): 
                date_match=search(r"\d+/\d+/\d+", line)
                if date_match:
                    date = date_match.group()
                    
        levels.sort()
        characters.sort()

        if levels and characters:
            counter += 1
            dm_exists = False
            ranks = []
            dm = None
            
            if message.reactions: 
                dm_exists = True
                for reaction in message.reactions:
                    async for user in reaction.users():
                        dm = user.display_name
                        if dm in players:
                            players.remove(dm)

            for level in levels:
                if player_ranks[level] not in ranks:
                    ranks.append(player_ranks[level])

            rank_string = "/".join(ranks)                
            char_string = ", ".join(characters)
            player_string = ", ".join(players)

            depr = ""
            if (dm_exists):
                depr = "~~"

            dated_game_string = f"{nl}{depr}Date: {date}{depr}{nl}{depr}Ranks: {rank_string}{depr}{nl}{depr}Characters: {char_string}{depr}{nl}{depr}Players: {player_string}{depr}{nl}{depr}Link: {message_link}{depr}{nl}"
            undated_game_string = f"{nl}{depr}Ranks: {rank_string}{depr}{nl}{depr}Characters: {char_string}{depr}{nl}{depr}Players: {player_string}{depr}{nl}{depr}Link: {message_link}{depr}{nl}"
            if date != "":
                actual_date = datetime.strptime(date, "%m/%d/%Y")
                dated_games[actual_date] = dated_game_string
            else: 
                undated_games.append(undated_game_string)
    dated_games_string = ""
    undated_games_string = ""
    index = 1 
    if len(dated_games) > 0:
        sorted_dated_games = dict(sorted(dated_games.items()))
        current_month = ""
        for curr_date, value in sorted_dated_games.items():
            new_month = curr_date.strftime("%B")
            if current_month != new_month:
                current_month = new_month
                dated_games_string += f"## {new_month}:{nl}"
            dated_games_string += f"{nl}**Game {index}:**" + value
            index +=1

    if len(undated_games) > 0:   
        undated_games_string = "## Without Correct Date:"
        for game_string in undated_games:
            undated_games_string += f"{nl}**Game {index}:**" + game_string 
            index += 1
    
    final_message = f'# This channel has {counter} games listed:{nl}{dated_games_string}{nl}{undated_games_string}'
    if (shedule_exists): 
        await shedule_message.edit(content=final_message)
    else: 
        await ctx.send(final_message)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)