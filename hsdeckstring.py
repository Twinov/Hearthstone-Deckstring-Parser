import sys

from prettytable import PrettyTable

from hearthstone.deckstrings import Deck
from hearthstone.cardxml import load_dbf
from hearthstone.enums import get_localized_name


for i, hs_deck in enumerate(sys.argv):
    if not i == 0:
        locale = 'enUS'
        deck = Deck.from_deckstring(hs_deck)
        db, _ = load_dbf(locale=locale)
        english_db = db

        card_includes = deck.cards
        cards = [(db[dbf_id], count) for dbf_id, count in card_includes]
        cards.sort(key=lambda include: (include[0].cost, include[0].name))
        try:
            hero = db[deck.heroes[0]]
            class_name = get_localized_name(hero.card_class, locale=locale)
            hero_name = f"{class_name} ({hero.name})"
        except KeyError:
            hero_name = "Unknown"

        card_list = PrettyTable()
        card_list.field_names = ['Card Cost', 'Card Name', 'Card Count']
        for card, count in cards:
            card_list.add_row([card.cost, card.name, count])

        print(hero_name)
        print(card_list)
        print('Deckstring: ', hs_deck, '\n')
