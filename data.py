class CardDataUnifierArticraft:

    @classmethod
    def unify_card_data(cls, data) -> list:
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
            spell - hero's signature spell, represented by dict with following keys (# TODO: to be discussed)
                name - spell's name
                image - URL of spell's image
            illustrator - name of the art creator
        :param data:
        :return:
        """
        return list()


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
        mocked_card_data[0]['illustrator'] = 'Tyler Jacobson'

        return mocked_card_data


class CardDataProviderArticraft:

    @classmethod
    def get_data(cls, partial_name: str) -> list:
        return CardDataUnifierArticraft.unify_card_data(dict())
