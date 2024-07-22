import asyncio
import json
import os

import discord

intents = discord.Intents.default()
intents.members = True
intents.messages = True

client = discord.Client(intents=intents)

last_modified = 0.0

# Load nicknames from a JSON file
def load_player_usernames():
    usernames = {}
    with open('./usercache.json', 'r') as f:
        data = json.load(f)
        for player in data:
            usernames[player['uuid']] = player['name']
    return usernames

# Load player links from a JSON file
def load_player_links():
    links = {}
    with open('./accounts.json', 'r') as f:
        links = json.load(f)
    return links

# Function to update nicknames
async def update_nicknames(guild):
    player_usernames = load_player_usernames()
    player_links = load_player_links()

    for mc_id, discord_id in player_links.items():
        member = guild.get_member(int(discord_id))
        
        if member is None:
            print(f'Failed to find member with ID {discord_id}')
            continue
        
        if member.display_name == player_usernames[str(mc_id)]:
            continue
        
        try:
            print(f'Changed nickname for {member.display_name} to {player_usernames[str(mc_id)]}')
            await member.edit(nick=player_usernames[str(mc_id)])
        except discord.Forbidden:
            print(f'Failed to change nickname for {member.display_name}, insufficient permissions')
        except discord.HTTPException as e:
            print(f'Failed to change nickname for {member.display_name}: {e}')

async def check_accounts(guild):
    global last_modified
    
    if os.path.getmtime('./accounts.json') > last_modified:
            last_modified = os.path.getmtime('./accounts.json')
            print('File has been modified, updating nicknames...')
            await update_nicknames(guild)

# Listen to message on channel X
# @client.event
# async def on_message(message: discord.Message):
#     if message.author == client.user:
#         return

#     # ONLY ALLOW IMAGES
#     if message.channel.id == 1264538863595032616:
#         print(message.attachments)
#         if len(message.attachments) == 0:
#             await message.delete()
#         else:
#             for attachment in message.attachments:
#                 if not attachment.content_type.startswith('image'):
#                     await message.delete()
#                     break
    
#     # ONLY ALLOW MESSAGE WITH LINKS FROM YOUTUBE AND TWITCH
#     if message.channel.id == 1256756505726943345:
#         print(message)
#         for media_provider in ('youtu.be', 'youtube.com', 'twitch.tv'):
#             if media_provider in message.content:
#                 return

#         await message.delete()
            

# Event when the bot is ready
@client.event
async def on_ready():
    global last_modified
    print(f'Logged in as {client.user}')
    guild = client.get_guild(1186647850097057873)
    
    last_modified = os.path.getmtime('./accounts.json')

    print('Updating nicknames...')
    await update_nicknames(guild)
    
    print('Bot is ready and watching for file changes!')
    while True:
        await asyncio.sleep(300)
        await check_accounts(guild)
        
    

# Run the bot
client.run(os.getenv('DISCORD_TOKEN'))
