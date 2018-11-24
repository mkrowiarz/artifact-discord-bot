# Work with Python 3.6
import discord
from discord.ext.commands import Bot

TOKEN = 'NTE1ODMxMjUwNDM1NTcxNzIz.DtrZHw.vVr3gOnAa5sl8YnG0tdDuks9T5Y'

client = Bot(command_prefix='!')


@client.command()
async def card(card_name):
    # Du medżik
    await client.say("Chaka Laka Pocałuj Mnie W Ptaka")

# @client.event
# async def on_message(message):
#     # we do not want the bot to reply to itself
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('!c'):
#         msg = f'Hello {message.author.mention}'
#         await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
