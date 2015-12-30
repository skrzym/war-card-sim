import random
import time
import os
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


clear = lambda: os.system('cls')
NUM_WAR_CARDS = 3
VERBOSE = True

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


class Game:
    def __init__(self, num_players):
        self.winner = None
        self.num_players = num_players
        self.game_deck = Deck()
        self.players = []

        self.stat_step_count = 0
        self.stat_card_count = []
        self.stat_wins_array = []
        self.stat_wars_array = []
        self.stat_winning_card_array = []
        self.stat_wars_won_array = []
        self.stat_wins = {}
        self.stat_wars = {}
        self.stat_wars_won = {}
        self.stat_winning_card = []

        self.init_game()

    def init_game(self):
        # Create each player in the game and give them a generic name
        for count in range(self.num_players):
            self.players.append(Player('Player ' + str(count + 1)))

        # Deal the deck completely to each player (checks that deck isn't empty on each deal)
        while len(self.game_deck.cards) > 0:
            for player in self.players:
                if len(self.game_deck.cards) > 0:
                    player.add_cards_to_hand(self.game_deck.draw_card())

        # Initialize stats for game
        for x in range(self.num_players):
            self.stat_wins[x] = 0
            self.stat_wars[x] = 0
            self.stat_wars_won[x] = 0

    def run_step(self):
        table = []
        pot = []

        for player in self.players:
            if player.replenish_hand_check():
                table.append(player.draw_card())
            else:
                table.append(None)
        # Logging
        # print '\t', table
        war_occurred = False
        war_exists = self.check_for_war(table)
        while war_exists:
            # Logging
            war_occurred = True
            # print str('*** War Exists!'), war_exists.count(True), 'players at War!'
            for index in range(len(war_exists)):
                if war_exists[index]:
                    self.stat_wars[index] += 1

            for item in range(len(table)):
                pot.append(table.pop())
            for index in range(len(self.players)):
                if war_exists[index]:
                    for x in range(NUM_WAR_CARDS):
                        if self.players[index].replenish_hand_check():
                            pot.append(self.players[index].draw_card())
                    if self.players[index].replenish_hand_check():
                        table.append(self.players[index].draw_card())
                    else:
                        table.append(None)
                else:
                    table.append(None)
            war_exists = self.check_for_war(table)

        # Evaluate who wins this step and give winning player all the cards on the table and pot
        step_winner = self.evaluate_step_winner(table)
        # Logging
        if war_occurred:
            self.stat_wars_won[step_winner] += 1
        self.stat_wins[step_winner] += 1
        self.stat_winning_card.append(table[step_winner])
        for card in table:
            if card is not None:
                self.players[step_winner].add_cards_to_won_cards(card)
        for card in pot:
            if card is not None:
                self.players[step_winner].add_cards_to_won_cards(card)

        # Check if a winner exists
        self.check_for_winner()

    def evaluate_step_winner(self, table):
        table_values = self.get_table_values(table)
        max_value = max(table_values)
        for player in range(len(table_values)):
            if table_values[player] is max_value:
                winner = player
                break
        return winner

    def card_value(self, card):
        if card is None:
            return 0
        if len(card) == 3:
            return 10
        elif card[-1].isdigit():
            return int(card[-1])
        else:
            if card[-1] == 'J':
                return 11
            elif card[-1] == 'Q':
                return 12
            elif card[-1] == 'K':
                return 13
            elif card[-1] == 'A':
                return 14

    def get_table_values(self, table):
        table_values = []
        for card in table:
            table_values.append(self.card_value(card))
        return table_values

    def check_for_winner(self):
        for player in self.players:
            # print player.get_card_count()
            if player.get_total_card_count() == 52:
                self.winner = player

    def check_for_war(self, table):
        table_values = self.get_table_values(table)
        max_value = max(table_values)
        if max_value is None:
            return False
        if table_values.count(max_value) > 1:
            mask = [x == max_value for x in table_values]
            return mask
        else:
            return False

    def run_game(self):
        while self.winner is None:
            self.stat_step_count += 1
            if VERBOSE: print str(self.stat_step_count) + '-' * 20
            self.run_step()
            if (self.stat_step_count % 1 == 0) or (self.stat_step_count == 1):
                self.stat_card_count = []
                for player in self.players:
                    self.stat_card_count.append(player.get_total_card_count())
            if self.stat_step_count == 1000000:
                break
            if VERBOSE:
                # print '  ' + 'Cards: ' + str(self.stat_card_count)
                # print '  ' + 'Wins : ' + str(self.stat_wins)
                # print '  ' + 'Wars : ' + str(self.stat_wars)
                # print '  ' + 'WarsW: ' + str(self.stat_wars_won)
                # print '  ' + 'WCard: ' + str(self.stat_winning_card[-1])
                print self.stat_step_count, self.num_players, self.stat_card_count[0], self.stat_card_count[1], \
                    self.stat_winning_card[-1]
                time.sleep(.1)
                clear()
        if VERBOSE:
            clear()
            if self.winner is None:
                print 'Nobody wins!', str(self.stat_step_count) + ':', self.stat_card_count
            else:
                print self.winner.name, 'wins the game!'
            print '  ' + 'Games: ' + str(self.stat_step_count)
            print '  ' + 'Cards: ' + str(self.stat_card_count)
            print '  ' + 'Wins : ' + str(self.stat_wins)
            print '  ' + 'Wars : ' + str(self.stat_wars)
            print '  ' + 'WarsW: ' + str(self.stat_wars_won)
            print '  ' + 'WCard: ' + str(self.stat_winning_card[-1])
            cards_by_value = [self.stat_winning_card[x][1:] for x in range(len(self.stat_winning_card))]
            value_frequency = Counter(cards_by_value)
            print '  ' + 'Freq : ' + str(value_frequency)
            print ''
            # plt.plot(card_count)
            # plt.show()


class Simulation:

    def __init__(self,num_games, num_players, output_filename, verbose=False, num_war_cards=3):
        global VERBOSE, NUM_WAR_CARDS
        VERBOSE = verbose
        NUM_WAR_CARDS = num_war_cards

        self.num_games = num_games
        self.num_players = num_players
        self.output_filename = output_filename

    def run_simulation(self):
        for count in range(self.num_games):
            sim_game = Game(self.num_players)
            sim_game.run_game()
            print 'Game', count + 1, 'of', self.num_games
            clear()
            #print ''
            #time.sleep(0.01)


my_sim = Simulation(2000, 2, 'testing', True, 3)
my_sim.run_simulation()





