from cards import (
    Deck,
    Card,
    Hand
)
from players import (
    Dealer,
    Player
)

class UserInterface:

    def __init__(self) -> None:
        pass
    #######################


class BlackjackGame:
    deck = Deck()
    dealer = Dealer()

    def __init__(self) -> None:
        self.players = self.get_player_names()

    def get_player_names(self):
        player_number = 1
        players = []
        name = 'None'
        while len(players) <= 4 and name:
            name = input(f'Type name of player {player_number} (leave blank if completed): ')
            if not name and len(players) > 0:
                break

            funds = input(f'How much money is {name} playing with? ')
            player = Player(name, float(funds))
            players.append(player)
            player_number += 1

        return players

    def initialize_round(self):
        for player in self.players:
            player.choose_bet_size()

        self.deck.shuffle()
        self.deck.deal(self.players, self.dealer)

        print(f'Dealer: {str(self.dealer.hand)}')
        player_hand_message = ''
        for player in self.players:
            player_hand_message += f'{player.name}: {str(player.hand)}, '
        print(player_hand_message[:-2])

    def play_round(self):
        self.initialize_round()

        for player in self.players:
            player.play(self.deck)

        self.dealer.play()

        



game = BlackjackGame()
game.play_round()









    



        


