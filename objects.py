from discord import Embed


class Card:
    def __init__(self, card_data: dict):
        pass

    def to_embed(self) -> Embed:
        pass


class CardSpell(Card):
    pass


class CardHero(Card):
    pass


class CardCreep(Card):
    pass


class CardAbility(Card):
    pass


class CardPassiveAbility(Card):
    pass


class CardItem(Card):
    pass


class CardList(list):
    def to_embed(self):
        pass


class CardFactory:

    @classmethod
    def create_cards(cls, unified_card_data: list, limit: int = 5) -> CardList:
        pass
