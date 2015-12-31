import game
import time


class Simulation:

    def __init__(self, num_games, num_players, verbose=False, num_war_cards=3):
        self.verbose = verbose
        self.num_war_cards = num_war_cards
        self.num_games = num_games
        self.num_players = num_players
        self.sim_winner = []
        self.sim_length = []
        self.sim_step_d = []
        self.sim_wars = []
        self.sim_gw_wins = []

    def run_simulation(self):
        for count in range(self.num_games):
            sim_game = game.Game(self.num_players, self.num_war_cards, self.verbose)
            sim_game.run_game()

            # LOGGING #################################
            # Update sim_winner array
            if sim_game.step_winner == 0:
                self.sim_winner.append(True)
            else:
                self.sim_winner.append(False)

            # Update sim_length array
            self.sim_length.append(sim_game.stat_step_count)

            # Update sim_step_d array
            self.sim_step_d.append(abs(sim_game.stat_wins[0]-sim_game.stat_wins[1]))

            # Update sim_wars array
            war_count = 0
            for player in sim_game.stat_wars:
                war_count += sim_game.stat_wars[player]
            self.sim_wars.append(war_count)

            # Update sim_gw_wins
            if sim_game.step_winner == [val == max(sim_game.stat_wars_won.values()) for val in sim_game.stat_wars_won.values()].index(True):
                self.sim_gw_wins.append(True)
            else:
                self.sim_gw_wins.append(False)

            p1_wins = self.sim_winner.count(True)
            p2_wins = self.sim_winner.count(False)
            avg_len = sum(self.sim_length)/(len(self.sim_length)*1.0)
            avg_wd = sum(self.sim_step_d)/(len(self.sim_step_d)*1.0)
            avg_wars = sum(self.sim_wars)/(len(self.sim_wars)*1.0)
            sum_wars = sum(self.sim_wars)
            annom_rate = self.sim_gw_wins.count(False)/(len(self.sim_gw_wins)*1.0)

        #Report Simulation Results
        print 'Game', count + 1, 'of', self.num_games
        print 'War Cards:\t', self.num_war_cards
        print 'P1 Wins:\t', p1_wins
        print 'P2 Wins:\t', p2_wins
        print 'Avg Len:\t', avg_len
        print 'Avg WDif:\t', avg_wd
        print 'Avg Wars:\t', avg_wars
        print 'Sum Wars:\t', sum_wars
        print 'Annom Rate:\t', annom_rate
        time.sleep(0)

# WARNING: the higher the num war cards, the higher the probability of both players running out of cards mid war
# causing an infinite loop of fail... so less than 6 is a good number right now

#if len(sys.argv) > 1:
#    games = int(sys.argv[1])
#    if len(sys.argv) > 2:
#        war_cards = int(sys.argv[2])
#        my_sim = Simulation(games, 2, False, war_cards)
#    else:
#        my_sim = Simulation(games, 2, False, 3)
#else:
#    my_sim = Simulation(10000, 2, False, 3)
#
#my_sim.run_simulation()





