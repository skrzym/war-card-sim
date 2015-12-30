import random


class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        numbers = range(2, 11)
        faces = ['A', 'J', 'Q', 'K']
        suites = ['H', 'S', 'C', 'D']
        for suite in suites:
            for face in faces:
                self.cards.append(suite + face)
            for number in numbers:
                self.cards.append(suite + str(number))
        self.shuffle_deck()

    def print_deck(self):
        for card in self.cards:
            print card

    def shuffle_deck(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop(0)
