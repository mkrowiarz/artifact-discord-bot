from discord import Embed
from discord import colour


class Card:
    def __init__(self, data: dict):
        self.data = data

    def __str__(self):
        return self.data['name']

    def to_embed(self) -> Embed:
        embed = Embed()
        embed.type = 'rich'
        embed.set_author(name=self.data['name'], url=self.data['image'], icon_url=self.data['icon'])
        embed.colour = getattr(colour.Color, self.data['color'])()
        embed.url = self.data['image']
        embed.set_thumbnail(url=self.data['image'])
        return embed


class CardSpell(Card):
    pass


class CardHero(Card):

    def to_embed(self):
        embed = super(CardHero, self).to_embed()

        # Add Signature spell description
        embed.add_field(name='**Spell**', value=self.data['spell']['name'])

        # Add hero's abilities description
        for ability in self.data['abilities']:
            embed.add_field(name=f'**Ability:** {ability["name"]}', value=ability["description"])

        # Add attack/armor/health stats
        stats = self.data['stats']
        embed.add_field(name='**Stats**', value=f':crossed_swords: **{stats["attack"]}** :shield: **{stats["armor"]}**  :heart: **{stats["health"]}**')

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
            embed = Embed()
            embed.type = 'rich'
            embed.set_author(name='Multiple results')
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
