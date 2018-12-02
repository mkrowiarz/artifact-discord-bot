import requests
from bs4 import BeautifulSoup
import urllib.parse

# TODO: Discuss creep description on example of "Oglodi Vandal"
""" 
    Each key should be present only if applicable to a certain card type.
    Data format per card:
        name - name of the card
        color - color to which card belongs
        type  - hero, item, creep, spell, improvement
        icon - to be displayed next to name
        image - URL of a big image representing whole card
        rarity - self explanatory ;)
        description - card description
        mana_cost - cost to play the card
        gold_cost - cost to buy an item
        stats - dict with following keys holding integer values:
            attack
            armor
            health
        spell - hero's signature spell, represented by dict with following keys
            name - spell's name
            image - URL of spell's image
        abilities - list hero's abilities, represented by entries (dicts) with following keys
            name - ability's name
            image - URL of ability's image
            description - string with description
        artist - name of the art creator
"""


class CardDataUnifierArticraft:

    @classmethod
    def unify_card_data(cls, data: list, limit: int = 5) -> list:
        return [cls.unify_card(item) for item in data[0:limit]]

    @classmethod
    def unify_card(cls, card_data: dict) -> dict:
        card = dict()

        card['type'] = cls.get_type(card_data)
        card['rarity'] = cls.get_rarity(card_data['rarity'])

        card['name'] = card_data['name']
        card['color'] = card_data['colour']

        if card['color'] == 'item':
            card['color'] = 'dark_gold'

        card['icon'] = card_data['images']['icon']
        card['image'] = card_data['images']['cardArt']

        if 'stats' in card_data:
            card['stats'] = {
                'attack': card_data['stats']['attack'],
                'armor': card_data['stats']['armour'],
                'health': card_data['stats']['health']
            }

        if card['type'] == 'spell':
            card['spell'] = {
                'name': card_data['name'],
                'image': card_data['images']['card']
            }
        elif card['type'] == 'hero':
            card['spell'] = {
                'name': 'To be implemented',
                'image': ''
            }

        if 'abilities' in card_data:
            card['abilities'] = cls.get_abilities(card_data['abilities'])

        if 'artist' in card_data:
            card['artist'] = card_data['artist']['name']

        if 'description' in card_data:
            card['description'] = card_data['description']

        if 'gold' in card_data:
            card['gold_cost'] = card_data['gold']

        if 'mana' in card_data:
            card['mana_cost'] = card_data['mana']

        if 'steam_market_data' in card_data:
            card['steam_market_data'] = card_data['steam_market_data']

        return card

    @classmethod
    def get_type(cls, card_data: dict) -> str:
        if card_data['type'] == 'main':
            return card_data['subType']
        else:
            return card_data['type']

    @classmethod
    def get_abilities(cls, items: list) -> list:
        abilities = list()

        for item in items:
            ability = {
                'type': item['type'],
                'description': item['description'],
            }

            if 'name' in item:
                ability['name'] = item['name']
            else:
                ability['name'] = ''

            if 'image' in item:
                ability['image'] = item['image']
            else:
                ability['image'] = ''

            if 'cooldown' in item:
                ability['cooldown'] = item['cooldown']
            else:
                ability['cooldown'] = ''

            abilities.append(ability)

        return abilities

    @classmethod
    def get_rarity(cls, rarity: int) -> str:
        if rarity == 0:
            return 'No rarity'
        elif rarity == 1:
            return 'Common'
        elif rarity == 2:
            return 'Rare'
        else:
            return 'Very rare'  # FIXME: No such rarity


class CardDataProviderMock:

    @classmethod
    def get_data(cls, partial_name: str = ''):
        mocked_card_data = list()
        mocked_card_data.append(dict())
        mocked_card_data[0]['name'] = 'Mocked Axe'
        mocked_card_data[0]['color'] = 'red'
        mocked_card_data[0]['type'] = 'hero'
        mocked_card_data[0]['icon'] = 'https://steamcdn-a.akamaihd.net/apps/583950/icons/set01/10020.023febd622949d771d9f6a4322efc339ced8c560.png'
        mocked_card_data[0]['image'] = 'https://steamcdn-a.akamaihd.net/apps/583950/icons/set01/10020_large_english.2eabe3c2871aa2ebc94e78033faae2374457292e.png'
        mocked_card_data[0]['rarity'] = 'rare'
        mocked_card_data[0]['stats'] = {'attack': 7, 'armor': 2, 'health': 11}
        mocked_card_data[0]['spell'] = {'name': "Berserker's Call", 'image': 'URL_TO_SPELL'}
        mocked_card_data[0]['abilities'] = [{'name': 'Multicast', 'image': 'URL_TO_ABILITY', 'description': 'After you play a blue spell, there is a 25% chance to put a base copy of that card in to your hand.'}]
        mocked_card_data[0]['artist'] = 'Tyler Jacobson'

        return mocked_card_data


class CardDataProviderDrawTwoGG:

    @classmethod
    def get_data(cls, partial_name: str, limit: int = 5) -> list:
        r = requests.get('https://api.drawtwo.gg/api/cards/search?search=' + partial_name)
        r.raise_for_status()
        items = r.json()

        # Add market info for single results only
        if len(items) == 1:
            items[0]['steam_market_data'] = SteamMarketPriceProvider.get_market_data(items[0]['name'])

        return CardDataUnifierArticraft.unify_card_data(items, limit)


class SteamMarketPriceProvider:

    CURRENCY_ID_TO_SYMBOL = {
        1: 'USD',
        2: 'GBP',
        3: 'EUR'
    }

    @classmethod
    def get_market_data(cls, card_name: str):
        """
        Query Steam marketplace to grab information about card price etc.
        :param card_name: Name of the card which is going to be used as a search query
        :return: dict with relevant Steam Market info about provided card, if card was found in the marketplace listings
                else returns None
        """
        url_safe_card_name = urllib.parse.quote_plus(card_name)
        page = requests.get(f'https://steamcommunity.com/market/search?appid=583950&q={url_safe_card_name}')

        soup = BeautifulSoup(page.content, 'html.parser')

        for link in soup.find_all('a', {'class': 'market_listing_row_link'}):
            item_name = link.find('span', {'class': 'market_listing_item_name'}).getText()
            if item_name.lower() == card_name.lower():
                item_price_span = link.find('span', {'data-price': True})

                base_price = int(item_price_span.get('data-price')) / 100
                base_currency = SteamMarketPriceProvider.CURRENCY_ID_TO_SYMBOL[int(item_price_span.get('data-currency'))]

                exchange_rates = ExchangeRatesProvider.get_exchange_rates(
                    base_currency=base_currency, other_currencies=[base_currency, 'PLN'])

                # Returning dict with field 'prices' instead of just that value since it's quite possible
                # that this data structure will be expanded with more fields in near future
                market_info = dict()
                market_info['prices'] = {symbol: base_price * rate for symbol, rate in exchange_rates.items()}
                return market_info

        return None


class ExchangeRatesProvider:

    # TODO: Could be optimized to fetch rates only when all previous symbols are outdated by at least 24 hrs
    @classmethod
    def get_exchange_rates(cls, base_currency: str = 'USD', other_currencies: list = None):
        if other_currencies is not None:
            rates = requests.get(
                f'https://api.exchangeratesapi.io/latest?base={base_currency}&symbols={",".join(other_currencies)}')
            rates.raise_for_status()
            rates = rates.json()['rates']
            return rates
        else:
            return []
