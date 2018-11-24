# Work with Python 3.6
from discord.ext.commands import Bot
from discord import Embed
from objects import CardFactory, CardList
from data import CardDataProvider

TOKEN = 'NTE1ODMxMjUwNDM1NTcxNzIz.DtrZHw.vVr3gOnAa5sl8YnG0tdDuks9T5Y'

client = Bot(command_prefix='!')


@client.command()
async def card(card_name):
    # Du medżik
    unified_card_data = CardDataProvider.get_card(card_name)
    card_list: CardList = CardFactory.create_cards(unified_card_data)

    embed = Embed()
    embed.add_field(name='sdasdsa', value='sdsadasdsadw22434', inline=False)
    await client.say(embed=embed)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
