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

class Round:
    results = None
    
    def __init__(self, players) -> None:
        self.players = players


class BlackjackGame:
    deck = Deck()
    dealer = Dealer()

    def __init__(self) -> None:
        self.players = Players([Player('John', 1000, 1), Player('James', 2000, 2)])
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
            player = Player(name, float(balance), player_number)
            players.append(player)
            player_number += 1

        return players

    def initialize_round(self):
        self.ui.print_borders('NEW ROUND')
        self.ui.print_balances()

        self.players.choose_bet_sizes()

        self.deck.shuffle()
        self.deck.deal(self.players, self.dealer)

        self.ui.print_hands()
        
    def play_round(self):
        self.initialize_round()

        self.players.play_round(self.deck, self.dealer)

        if not self.players.all_busted:
            self.ui.print_borders(f'{self.dealer.name.upper()}\'S TURN')
            self.dealer.play(self.deck)

        self.players.determine_results(self.dealer)

        round_results = self.ui.get_round_result()
        time.sleep(1)
        self.ui.print_borders(round_results)

        self.players.process_balances()
        time.sleep(2)

    def play(self):
        while self.players.list:
            self.play_round()

        self.ui.print_borders('All players have been busted, game over!')




game = BlackjackGame()
game.play()








    



        


