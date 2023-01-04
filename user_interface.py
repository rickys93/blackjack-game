import time

class UserInterface:

    def __init__(self) -> None:
        pass        

    @staticmethod
    def print_borders(message: str):
        """
        Prints a message with a border of underscores around it.

        Parameters:
            - message: The message to be printed
        """
        number_of_lines = message.count('\n') if message.count('\n') > 0 else 1
        line_length = int(len(message) / number_of_lines)
        line = '_' * line_length
        print(f'{line}\n\n{message}\n{line}')

    @staticmethod
    def print_end_round():
        """
        Prints a message indicating that the round has ended.
        """
        end_round_message = '\nRound finished...'
        print(end_round_message)

    @staticmethod
    def string_dealers_hand_and_score(dealer):
        """
        Creates string of the dealer's current hand.

        Parameters:
            - dealer: The Dealer object
        """
        return f'Dealer\'s hand: {str(dealer.current_hand)}, Score: {dealer.current_hand.score}'

    @staticmethod
    def print_dealers_hand(dealer):
        """
        Prints the dealer's current hand.

        Parameters:
            - dealer: The Dealer object
        """
        print(f'Dealer\'s hand: \n{str(dealer.current_hand)}')

    def print_dealers_hand_and_score(self, dealer):
        """
        Prints the dealer's current hand and score.

        Parameters:
            - dealer: The Dealer object
        """
        print(self.string_dealers_hand_and_score(dealer))

    def print_player_start_turn(self, player, dealer):
        self.print_borders(f'{player.name.upper()}\'S TURN')
        self.print_dealers_hand(dealer)

    def print_dealer_start_turn(self, dealer):
        self.print_borders(f'{dealer.name.upper()}\'S TURN')
        
    @staticmethod
    def print_removing_player(player):
        print(f'{player.name} has run out of money.\nRemoving player...')

    @staticmethod
    def print_bet_size(hand):
        """
        Prints the bet size of a hand.

        Parameters:
            - hand: The Hand object
        """
        print(f'Bet size: £{hand.bet_size}')

    @staticmethod
    def display_player_hands(player):
        """
        Prints all of the player's hands, including completed, current, and pending hands.
        Indicates which hand is the current hand with "<<<<".

        Parameters:
            - player: The Player object
        """
        hands = player.completed_hands + [player.current_hand] + player.pending_hands
        if len(hands) == 1:
            hand_string = f'\n{player.name}\'s hand: \nBet size: £{hands[0].bet_size}\n{str(player.current_hand)}, Score: {player.current_hand.score}' 
        else: 
            hand_string = f'\n{player.name}\'s hands:' 
            for hand in hands:
                hand_string += f'\nBet size: £{hand.bet_size}\n{str(hand)}, Score: {hand.score}'
                if hand == player.current_hand:
                    hand_string += ' <<<<'

        print(hand_string)

    @staticmethod
    def get_hand_string(hand):
        return f'{str(hand)}, Score: {hand.score}' 

    @staticmethod
    def print_balances(players):
        """
        Prints the current balances for each player.
        """
        players_balance_message = '\nPlayer bank balances...\n'
        for player in players:
            players_balance_message += f'{player.name}: £{str(player.balance)}, '
        print(players_balance_message[:-2])

    @staticmethod
    def print_hands(players, dealer):
        players_hand_message = f'Dealer: {str(dealer.current_hand)}\n'
        for player in players:
            players_hand_message += f'{player.name}: {str(player.pending_hands[0])}, '
        players_hand_message = players_hand_message[:-2] + '\n'
        print(players_hand_message)
        input('Press enter to start round ')
        print('Starting round...')

    @staticmethod
    def print_dealer_bust(dealer):
        print(f'{dealer.name} score: {dealer.current_hand.score}')
        print(f'DEALER BUST')

    @staticmethod
    def print_player_bust(player):
        print(f'{player.name} score: {player.current_hand.score}')
        print(f'PLAYER BUST')

    def print_new_round(self, players):
        self.print_borders('NEW ROUND')
        self.print_balances(players)

    def print_start_round(self, players, dealer):
        """
        Prints the details for the start of the round.
        """

        self.print_balances(players)
        self.print_hands(players, dealer)

    def print_round_result(self, round) -> None:
        round_result = 'Round finished...\n'
        round_result += self.string_dealers_hand_and_score(round.dealer)
        if round.all_busted():
            round_result += f'\nAll players bust!'
        for player in round.players:
            round_result += f'\n{player.name}\'s hand:'
            for hand in player.completed_hands:
                round_result += '\n' + self.get_hand_string(hand)
                if hand.round_result == 'blackjack':
                    round_result += f' BLACKJACK!! Win £{hand.bet_size}!'
                if hand.round_result == 'win':
                    round_result += f' WIN £{hand.bet_size}!'
                if hand.round_result == 'lose':
                    round_result += f' LOSE £{hand.bet_size}'
                if hand.round_result == 'push':
                    round_result += f' PUSH '

            profit_loss = f'£{player.round_profit_loss}' if player.round_profit_loss > 0 else f'-£{-player.round_profit_loss}'
            round_result += f'\n{player.name} total round result: {profit_loss}'
        self.print_borders(round_result)

    def print_game_over(self):
        self.print_borders('All players have been busted, game over!')

    @staticmethod
    def print_player_stands(player):
        print(f'{player.name} stands.')
        print(f'{player.name} score: {player.current_hand.score}')

    @staticmethod
    def print_player_hits(name, new_card):
        print(f'{name} hits... {str(new_card)}')

    @staticmethod
    def print_player_splits(player):
        print(f'{player.name} splits.')

    @staticmethod
    def print_player_doubles(player, new_card):
        print(f'{player.name} doubles. Bet size: £{player.current_hand.bet_size}... {str(new_card)}')

    @staticmethod
    def get_player_bet_size(player):
        bet_size = float('inf')
        while bet_size > player.balance:
            if bet_size != float('inf'):
                print('Bet size larger than balance, please enter amount smaller than balance.')
            bet_size = float(input(f'{player.name} bet size: £ '))
        return bet_size

    @staticmethod
    def get_input_question(player):
        """
        Creates a string that asks the user which decision to take.

        Parameters:
            - player: The Player object

        Returns:
            - The input question (a string)
        """
        input_question_words = 'Hit/Stand'
        input_question_letters = '(H/S'
        if player.current_hand.split_possible():
            input_question_words += '/Split'
            input_question_letters += '/SP'
        if len(player.current_hand.cards) == 2:
            input_question_words += '/Double'
            input_question_letters += '/D'
        input_question_words += '? '
        input_question_letters += ') '
        input_question = input_question_words + input_question_letters
        return input_question

    def find_player_decision(self, player) -> str:
        """
        Prompts the player to enter their decision (hit, stand, split, or double) and returns their response.

        Parameters:
            - player: The Player object

        Returns:
            - The player's decision (a string)
        """

        input_question = self.get_input_question(player)
        decision = ''
        while not decision:
            decision = input(input_question)
            if decision in ['d', 'sp'] and player.current_hand.bet_size > player.balance:
                print(f'Not enough funds.')
                print(f'Bet size: £{player.current_hand.bet_size}')
                print(f'Balance: £{player.balance}')
                decision = ''
        return decision

    @staticmethod
    def get_player_names() -> list:
        """
        Ask for names of players and bank balance upon first starting the game.
        """

        players = []
        name = 'None'
        while len(players) <= 4 and name:
            name = input(f'Type name of player {len(players) + 1} (leave blank if completed): ')
            if not name and len(players) > 0:
                break

            balance = input(f'How much money is {name} playing with? ')

            player = {'name':name, 'balance':float(balance)}
            players.append(player)

        return players



ui = UserInterface()