import os
import discord
from discord.ext import commands
import dotenv

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {self.user}!')
@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    if message.content.startswith("$"):
        await message.delete()
        await message.channel.send(f'This is what you get for using a command {message.author.mention}: \n{message.content}')
@bot.command()
async def test(ctx, *args):
    arg_list = ', '.join(args)
    await ctx.send(f'{ctx.author.mention} You sent following arguments: {arg_list}')
    
@bot.command()
async def test_message(ctx:commands.Context, *args):
    message_list = []
    async for message in ctx.channel.history(limit=7):
        content_first = message.content.splitlines()[0]
        if "@" in content_first:
            message_list.append(content_first)

    end_message = "\n".join(message_list)
    await ctx.send(f'These are the messages sent: {end_message}')

client = MyClient(intents=intents)
client.run(os.getenv('API-TOKEN'))