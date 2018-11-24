class CardDataUnifier:

    @classmethod
    def unify_card_data(cls, data) -> dict:
        """
        Data format per card:
        All cards:
            name - name of the card
            color - color to which card belongs
            type  - hero, item, creep, spell, improvement
            icon - to be displayed next to name
            image - URL of a big image representing whole card
            rarity - self explanatory ;)
        Hero:
            stats - dict with following keys holding integer values:
                attack
                armor
                health
            signature_spell - dict with following keys (# TODO: to be discussed)
                name - spell's name
                image - URL of spell's image
            illustrator - name of the art creator
        :param data:
        :return:
        """
        pass


class CardDataProvider:

    @classmethod
    def get_cards(cls, partial_name: str) -> list:
        pass
