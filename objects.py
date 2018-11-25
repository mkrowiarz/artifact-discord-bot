from discord import Embed
from discord import colour


class Card:
    def __init__(self, data: dict):
        self.data = data

    def to_embed(self) -> Embed:
        embed = Embed()
        embed.type = 'rich'
        # TODO: Add self.data['icon'] to the title
        embed.title = self.data['name']
        embed.colour = getattr(colour.Color, self.data['color'])()
        embed.set_image(url=self.data['image'])
        return embed


class CardSpell(Card):
    pass


class CardHero(Card):

    def to_embed(self):
        embed = super(CardHero, self).to_embed()

        # Add attack/armor/health stats
        stats = self.data['stats']
        embed.add_field(name='Stats', value=f'{stats["attack"]} / {stats["armor"]} / {stats["health"]}', inline=False)

        # Add Signature spell description
        # TODO: Display in a better way with link to the spell's image etc.
        embed.add_field(name='Signature spell', value=self.data['spell']['name'], inline=False)

        return embed


class CardCreep(Card):
    pass


class CardItem(Card):
    pass


class CardImprovement(Card):
    pass


class CardList(list):
    def to_embed(self):
        """
        Create embed that will be displayed, either of a single card if there was one match
        or the one which represents list of all matched cards
        :return:
        """

        if len(self) == 1:
            return self[0].to_embed()
        else:
            # TODO: Create actual embed info about the list of items
            return 'Embed'


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
