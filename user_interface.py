import time

class UserInterface:
    currency = '£'

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

    def print_bet_size(self, hand):
        """
        Prints the bet size of a hand.

        Parameters:
            - hand: The Hand object
        """
        print(f'Bet size: {self.currency}{hand.bet_size}')

    def display_player_hands(self, player):
        """
        Prints all of the player's hands, including completed, current, and pending hands.
        Indicates which hand is the current hand with "<<<<".

        Parameters:
            - player: The Player object
        """
        hands = player.completed_hands + [player.current_hand] + player.pending_hands
        if len(hands) == 1:
            hand_string = f'\n{player.name}\'s hand: \nBet size: {self.currency}{hands[0].bet_size}\n{str(player.current_hand)}, Score: {player.current_hand.score}' 
        else: 
            hand_string = f'\n{player.name}\'s hands:' 
            for hand in hands:
                hand_string += f'\nBet size: {self.currency}{hand.bet_size}\n{str(hand)}, Score: {hand.score}'
                if hand == player.current_hand:
                    hand_string += ' <<<<'

        print(hand_string)

    @staticmethod
    def get_hand_string(hand):
        return f'{str(hand)}, Score: {hand.score}' 

    def print_balances(self, players):
        """
        Prints the current balances for each player.
        """
        players_balance_message = '\nPlayer bank balances...\n'
        for player in players:
            players_balance_message += f'{player.name}: {self.currency}{str(player.balance)}, '
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
                    round_result += f' BLACKJACK!! Win {self.currency}{hand.bet_size}!'
                if hand.round_result == 'win':
                    round_result += f' WIN {self.currency}{hand.bet_size}!'
                if hand.round_result == 'lose':
                    round_result += f' LOSE {self.currency}{hand.bet_size}'
                if hand.round_result == 'push':
                    round_result += f' PUSH '

            profit_loss = f'{self.currency}{player.round_profit_loss}' if player.round_profit_loss > 0 else f'-{self.currency}{-player.round_profit_loss}'
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

    def print_player_doubles(self, player, new_card):
        print(f'{player.name} doubles. Bet size: {self.currency}{player.current_hand.bet_size}... {str(new_card)}')

    def get_player_bet_size(self, player):
        while True:
            try:
                bet_size = float(input(f'{player.name} bet size: {self.currency} '))
                if bet_size <= 0:
                    print('Please choose a bet size greater than 0.')
                    continue
                if bet_size > player.balance:
                    print(f'Please choose bet size less than player balance ({self.currency}{player.balance}).')
                    continue
                break
            except ValueError:
                print("Please enter a valid bet size greater than 0.")
        return bet_size

    @staticmethod
    def invalid_decision_string(valid_decisions):
        string = "Invalid input. Please enter "
        for d in valid_decisions:
            string += f"'{d}', "
        string = string[:-2] + '.'
        return string     

    @staticmethod
    def get_input_word(input):
        if input == 'h':
            return 'Hit'
        if input == 's':
            return 'Stand'
        if input == 'sp':
            return 'Split'
        if input == 'd':
            return 'Double'

    def get_input_question(self, allowed_inputs):
        """
        Creates a string that asks the user which decision to take.

        Parameters:
            - player: The Player object

        Returns:
            - The input question (a string)
        """
        input_question_words = ''
        input_question_letters = '('
        for input in allowed_inputs:
            input_question_words += self.get_input_word(input) + '/'
            input_question_letters += input.upper() + '/'

        input_question_words = input_question_words[:-1] + '? '
        input_question_letters = input_question_letters[:-1] + ') '

        input_question = input_question_words + input_question_letters
        return input_question

    def find_player_decision(self, player, valid_decisions) -> str:
        """
        Prompts the player to enter their decision (hit, stand, split, or double) and returns their response.

        Parameters:
            - player: The Player object

        Returns:
            - The player's decision (a string)
        """

        input_question = self.get_input_question(valid_decisions)
        decision = ''
        while not decision:
            decision = input(input_question)
            if decision not in valid_decisions:
                decision = ''
                print(self.invalid_decision_string(valid_decisions))

            elif decision in ['d', 'sp'] and player.current_hand.bet_size > player.balance:
                print(f'Not enough funds.')
                print(f'Bet size: {self.currency}{player.current_hand.bet_size}')
                print(f'Balance: {self.currency}{player.balance}')
                decision = ''

        return decision

    def get_player_balance(self, name):
        while True:
            try:
                balance = float(input(f'How much money is {name} playing with? {self.currency} '))
                if balance <= 0:
                    print("Please enter a valid balance amount greater than 0.")
                    continue
                return balance
            except ValueError:
                print("Please enter a valid balance amount.")
                continue

    def get_player_names(self) -> list:
        """
        Ask for names of players and bank balance upon first starting the game.
        """

        players = []
        names = set()
        name = 'None'
        while len(players) <= 4:
            name = input(f'Type name of player {len(players) + 1} (type F to finish): ')

            if name.lower() == 'f':
                if len(players) > 0:
                    break
                print('Need to have at least one player')
                continue
            if not name:
                print("Please enter a valid name.")
                continue
            if name in names:
                print("Name already in use, please try a different name.")
                continue
            names.add(name)

            balance = self.get_player_balance(name)
            player = {'name':name, 'balance':float(balance)}
            players.append(player)

        return players



ui = UserInterface()