# Work with Python 3.6
import discord

TOKEN = 'NTE1ODMxMjUwNDM1NTcxNzIz.DtrZHw.vVr3gOnAa5sl8YnG0tdDuks9T5Y'

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!c'):
        msg = f'Hello {message.author.mention}'
        await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
