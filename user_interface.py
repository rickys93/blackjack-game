import time

class UserInterface:

    def __init__(self, players, dealer, deck) -> None:
        self.players = players
        self.dealer = dealer
        self.deck = deck

    @staticmethod
    def print_borders(message):
        line = len(message) * '_'
        print(f'{line}\n\n{message}\n{line}')

    @staticmethod
    def print_end_round():
        end_round_message = '\nRound finished...'
        print(end_round_message)

    @staticmethod
    def print_dealers_hand(dealer):
        print(f'Dealer\'s hand: {str(dealer.hand)}')

    @staticmethod
    def print_dealers_hand_and_score(dealer):
        print(f'Dealer\'s hand: {str(dealer.hand)}, Score: {dealer.score}')

    @staticmethod
    def print_bet_size(player):
        print(f'Bet size: £{player.bet_size}')

    @staticmethod
    def find_player_decision(player) -> str:
        input_question_words = 'Hit/Stand'
        input_question_letters = '(H/S'
        if player.hand.split_possible():
            input_question_words += '/Split'
            input_question_letters += '/SP'
        if len(player.hand.cards) == 2:
            input_question_words += '/Double'
            input_question_letters += '/D'
        input_question_words += '? '
        input_question_letters += ') '
        input_question = input_question_words + input_question_letters

        decision = ''
        while not decision:
            decision = input(input_question)
            if decision == 'd' and player.bet_size > player.balance:
                print(f'Not enough funds to double.')
                print(f'Bet size: £{player.bet_size}')
                print(f'Balance: £{player.balance}')
                decision = ''
        return decision

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
        input('Press enter to start round ')
        print('Starting round...')
        time.sleep(1)


    def get_round_result(self) -> str:
        round_result = 'Round finished...'
        if self.players.all_busted:
            round_result += f'\nAll players bust!'
        for player in self.players.list:
            if player.round_result == 'blackjack':
                round_result += f'\nBLACKJACK!!\n{player.name} wins £{player.bet_size}!'
            if player.round_result == 'win':
                round_result += f'\n{player.name} wins £{player.bet_size}!'
            if player.round_result == 'lose':
                round_result += f'\n{player.name} loses £{player.bet_size}'
            if player.round_result == 'push':
                round_result += f'\n{player.name} pushes'
        return round_result


