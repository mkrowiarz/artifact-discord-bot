# Work with Python 3.6
from discord.ext.commands import Bot
from objects import CardFactory, CardList
from data import CardDataProviderArticraft, CardDataProviderMock
import config

client = Bot(command_prefix='!')


@client.command()
async def card(*card_name):
    # Retrieve unified card data from CardDataProvider using partial card name
    unified_card_data = CardDataProviderArticraft.get_data(' '.join(card_name))

    # Create list of objects which represent cards as close as possible
    card_list: CardList = CardFactory.create_cards(unified_card_data)

    # Display an embed with info about card(s)
    await client.say(embed=card_list.to_embed())


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(config.BOT_TOKEN)
