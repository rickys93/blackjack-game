import time

from cards import (
    Deck,
    Card,
    Hand
)
from players import (
    Dealer,
    Player,
    Players
)
from user_interface import UserInterface


class BlackjackGame:
    deck = Deck()
    dealer = Dealer()

    def __init__(self) -> None:
        self.players = Players([Player('John', 1000), Player('James', 2000)])
        self.ui = UserInterface(self.players, self.dealer, self.deck)

    def get_player_names(self):
        player_number = 1
        players = []
        name = 'None'
        while len(players) <= 4 and name:
            name = input(f'Type name of player {player_number} (leave blank if completed): ')
            if not name and len(players) > 0:
                break

            balance = input(f'How much money is {name} playing with? ')
            player = Player(name, float(balance))
            players.append(player)
            player_number += 1

        return players

    def initialize_round(self):
        self.ui.print_new_round('NEW ROUND')
        self.ui.print_balances()

        self.players.choose_bet_sizes()

        self.deck.shuffle()
        self.deck.deal(self.players, self.dealer)

        self.ui.print_hands()

    def play_round(self):
        self.initialize_round()

        self.players.play_round(self.deck)

        if not self.players.all_busted:
            self.dealer.play(self.deck)

        self.players.determine_results(self.dealer)

        self.ui.print_end_round()
        self.players.process_balances()
        time.sleep(1)

    def play(self):
        while self.players.list:
            self.play_round()

        self.ui.print_new_round('All players have been busted, game over!')




game = BlackjackGame()
game.play()









    



        


