import random


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.won_cards = []

    def add_cards_to_hand(self, cards):
        if isinstance(cards, str):
            self.hand.append(cards)
        else:
            for card in cards:
                self.hand.append(card)

    def add_cards_to_won_cards(self, cards):
        if isinstance(cards, str):
            self.won_cards.append(cards)
        else:
            for card in cards:
                self.won_cards.append(card)

    def put_won_cards_into_hand(self):
        random.shuffle(self.won_cards)
        self.add_cards_to_hand(self.won_cards)
        self.won_cards = []

    def replenish_hand_check(self):
        if self.get_total_card_count() == 0:
            return False
        if self.get_hand_count() == 0:
            self.put_won_cards_into_hand()
        return True

    def draw_card(self):
        return self.hand.pop(0)

    def get_hand_count(self):
        return len(self.hand)

    def get_total_card_count(self):
        return len(self.hand) + len(self.won_cards)

    def get_name(self):
        return self.name

    def shuffle_hand(self):
        random.shuffle(self.hand)
