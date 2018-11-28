from discord import Embed


class Card:
    def __init__(self, data: dict):
        self.data = data

    def __str__(self):
        return self.data['name']

    def to_embed(self) -> Embed:
        embed = Embed()
        embed.type = 'rich'
        embed.set_author(name=self.data['name'], url=self.data['image'], icon_url=self.data['icon'])
        embed.colour = self.get_color(self.data['color'])
        embed.url = self.data['image']
        embed.set_thumbnail(url=self.data['image'])
        embed.description = self.data['description'] if 'description' in self.data else None
        self.add_market_data(embed)
        return embed

    def add_stats(self, embed: Embed) -> Embed:
        """
        Add attack/armor/health stats section to the embed
        :param embed: Embed to which new field will be addec
        :return: Returns embed, passed via parameter, which it has already modified
        """
        if 'stats' in self.data:
            stats = self.data['stats']
            embed.add_field(
                name='**Stats**',
                value=f':crossed_swords: **{stats["attack"]}** '
                      f':shield: **{stats["armor"]}** '
                      f':heart: **{stats["health"]}**')

        return embed

    def add_abilities(self, embed: Embed) -> Embed:
        """
        Add description of active abilities
        :param embed:
        :return:
        """
        for ability in self.data['abilities']:
            embed.add_field(name=f'**Ability:** {ability["name"]}', value=ability["description"], inline=False)

        return embed

    def add_mana_cost(self, embed: Embed) -> Embed:
        if 'mana_cost' in self.data:
            embed.add_field(
                name='**Mana cost**',
                value=f':large_blue_diamond: **{self.data["mana_cost"]}**')

        return embed

    def get_color(self, color: str) -> int:
        colors = {
            'red': 0xe74c3c,
            'orange': 0xe67e22,
            'green': 0x2ecc71,
            'dark_gold': 0xc27c0e,
            'black': 0x000000,
            'blue': 0x3498db,
            'neutral': 0x0
        }

        if color in colors:
            return colors[color]
        else:
            return 0

    def add_market_data(self, embed: Embed) -> Embed:
        """
        Add information about card price to the embed
        :param embed: Embed to which new field (footer) will be added
        :return: Returns embed, passed via parameter, which was modified here
        """
        currency = {
            1: 'USD',
            2: 'GBP',
            3: 'EUR'
        }

        if 'card_market_data' not in self.data:
            return embed

        price = self.data['card_market_data']['price'] / 100
        currency_code = currency[self.data['card_market_data']['currency_id']]

        embed.set_footer(text=f'Card price: {price} {currency_code}')

        return embed


class CardSpell(Card):

    def to_embed(self):
        embed = super(CardSpell, self).to_embed()
        self.add_mana_cost(embed)
        return embed


class CardHero(Card):

    def to_embed(self):
        embed = super(CardHero, self).to_embed()

        self.add_abilities(embed)

        # Add Signature card description
        embed.add_field(name='**Signature card**', value=self.data['spell']['name'], inline=False)

        self.add_stats(embed)
        return embed


class CardCreep(Card):

    def to_embed(self):
        embed = super(CardCreep, self).to_embed()
        self.add_stats(embed)
        self.add_mana_cost(embed)
        return embed


class CardItem(Card):

    def add_gold_cost(self, embed: Embed) -> Embed:
        if 'gold_cost' in self.data:
            embed.add_field(
                name='**Gold cost**',
                value=f':moneybag: **{self.data["gold_cost"]}**')

        return embed

    def to_embed(self):
        embed = super(CardItem, self).to_embed()
        self.add_mana_cost(embed)
        self.add_gold_cost(embed)
        return embed


class CardImprovement(Card):

    def to_embed(self):
        embed = super(CardImprovement, self).to_embed()
        self.add_mana_cost(embed)
        return embed


class CardList(list):
    def to_embed(self):
        """
        Create embed that will be displayed, either of a single card if there was one match
        or the one which represents list of all matched cards
        :return:
        """

        if len(self) == 0:
            embed = Embed()
            embed.type = 'rich'
            embed.title = 'No results found.'
            return embed
        elif len(self) == 1:
            return self[0].to_embed()
        else:
            embed = Embed()
            embed.type = 'rich'
            embed.title = 'Multiple results found:'
            embed.description = "\n".join([str(card) for card in self])
            return embed


class CardFactory:
    @classmethod
    def get_card_class(cls, card_data: dict) -> type:
        if card_data['type'] == 'hero':
            return CardHero
        elif card_data['type'] == 'item':
            return CardItem
        elif card_data['type'] == 'creep':
            return CardCreep
        elif card_data['type'] == 'spell':
            return CardSpell
        elif card_data['type'] == 'improvement':
            return CardImprovement
        else:
            return Card

    @classmethod
    def create_cards(cls, unified_card_data: list) -> CardList:
        card_list = CardList()

        for card_data in unified_card_data:
            card_list.append(CardFactory.get_card_class(card_data)(card_data))

        return card_list
