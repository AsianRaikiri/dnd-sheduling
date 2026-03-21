import os
from re import search
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
token = os.getenv('API-TOKEN') # Gets  the API Token for the discord bot from the .env file

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()

# These two intents need to be set for this bot to be able to read messages and to get the users displayName
intents.message_content = True 
intents.members = True

# Below is the rank for each player at the given character level. Should the rank names change, this dictionary would need to be updated
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
    await ctx.message.delete() # Deletes the command message to avoid clutter
    nl = "\n" # New line variable because f-strings don't like backslash 
    shedule_exists = False
    shedule_message = None
    dated_games = {}
    undated_games = []

    # Below is the main loop, going through the whole message history of that channel (up to 500 messages) and reading each message from newest to oldest
    async for message in ctx.channel.history(limit=500):
        content = message.content
        if message.author == bot.user: # This checks for an existing schedule message to later either edit that or send a new one if none exists
            shedule_exists = True
            shedule_message = message
        players= []
        date = ""
        characters = []
        levels = []
        
        players_objects = message.mentions # This returns a list of all players + dm that were mentioned if given
        for user in players_objects: 
            players.append(user.display_name) # Have to check if full display name should be used

        message_list = content.splitlines()
        for line in message_list:

            if "@" in line and line.startswith("<@"): #This checks for all lines that start with a mention of a discord user, which should only be the players
                char_match = search(r">\s*\w+", line) # Regex checks if line has ">" any number of whitespaces and then letters
                if char_match: 
                    characters.append(char_match.group().removeprefix(">").strip()) # this removes the ">" and the whitespaces to leave the word alone
                
                level_match = search(r"\s+\d{1,2}\s*$", line) # This regex checks for at most two digits and whitespaces at the end of the line
                if level_match: 
                    levels.append(int(level_match.group().strip()))

            if line.startswith("Date: "): 
                date_match=search(r"\s*\d+/\d+/\d+\s*", line) # This regex checks for dates as digits with / in between and trailing or preceding whitespaces
                if date_match:
                    date = date_match.group().strip()

        if levels and characters: # Only if there are characters and levels associated with them does it add things to the final message
            levels.sort()
            characters.sort()
            dm_exists = False
            ranks = []
            dm = None
            message_link = message.jump_url # to later reference in the final post
            
            if message.reactions: # Since only one DM is supposed to react to the messages, this checks if a dm is associated to the post
                dm_exists = True
                for reaction in message.reactions: # This whole part can be removed if we don't need to list all players in a game
                    async for user in reaction.users():
                        dm = user.display_name
                        if dm in players:
                            players.remove(dm)

            for level in levels: 
                if player_ranks[level] not in ranks: # This prevents the same rank to be added multiple times
                    ranks.append(player_ranks[level])

            rank_string = "/".join(ranks)                
            char_string = ", ".join(characters)
            player_string = ", ".join(players)

            depr = ""
            if (dm_exists): # If there is DM associated with the post, it can be crossed out to show it in the Schedule
                depr = "~~"

            if date != "":
                actual_date = datetime.strptime(date, "%m/%d/%Y")
                dated_game_string = f"{nl}{depr}Date: {date}{depr}{nl}{depr}Ranks: {rank_string}{depr}{nl}{depr}Characters: {char_string}{depr}{nl}{depr}Players: {player_string}{depr}{nl}{depr}Link:{message_link}{depr}{nl}"
                dated_games[actual_date] = dated_game_string
            else: 
                undated_game_string = f"{nl}{depr}Ranks: {rank_string}{depr}{nl}{depr}Characters: {char_string}{depr}{nl}{depr}Players: {player_string}{depr}{nl}{depr}Link:{message_link}{depr}{nl}"
                undated_games.append(undated_game_string)
    dated_games_string = ""
    undated_games_string = ""
    index = 0
    if len(dated_games) > 0:
        sorted_dated_games = dict(sorted(dated_games.items()))
        current_month = ""
        for curr_date, value in sorted_dated_games.items():
            new_month = curr_date.strftime("%B") # This returns the full name of the month of the datetime object
            if current_month != new_month:
                current_month = new_month
                dated_games_string += f"## {new_month}:{nl}"
            index +=1
            dated_games_string += f"{nl}**Game {index}:**" + value


    if len(undated_games) > 0:
        undated_games_string = "## Without Correct Date:"
        for game_string in undated_games:
            index += 1
            undated_games_string += f"{nl}**Game {index}:**" + game_string

    final_message = f'# This channel has {index} games listed:{nl}{dated_games_string}{nl}{undated_games_string}'

    if (shedule_exists): # Update existing schedule if it exists or send a new one if it doesn't exist yet
        await shedule_message.edit(content=final_message)
    else:
        await ctx.send(final_message)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)