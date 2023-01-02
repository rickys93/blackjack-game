class UserInterface:

    def __init__(self, players, dealer, deck) -> None:
        self.players = players
        self.dealer = dealer
        self.deck = deck

    @staticmethod
    def print_new_round(message):
        line = len(message) * '_'
        print(f'{line}\n\n{message}\n{line}')

    @staticmethod
    def print_end_round():
        end_round_message = '\nRound finished.\n'
        print(end_round_message)

    def print_balances(self):
        players_balance_message = 'Player bank balances...\n'
        for player in self.players.list:
            players_balance_message += f'{player.name}: £{str(player.balance)}, '
        print(players_balance_message[:-2])

    def print_hands(self):
        players_hand_message = f'Dealer: {str(self.dealer.hand)}\n'
        for player in self.players.list:
            players_hand_message += f'{player.name}: {str(player.hand)}, '
        players_hand_message = players_hand_message[:-2] + '\n'
        print(players_hand_message)
