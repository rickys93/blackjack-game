import time
from user_interface import UserInterface as ui

class Participant:
    hand = None
    score = None
    busted = False
    got_blackjack = False
    
    def hit(self, deck):
        time.sleep(1)
        new_card = deck.cards.pop(0)
        self.hand.cards.append(new_card)
        print(f'{self.name} hits... {str(new_card)}')
        self.score = self.hand.calculate_score()

    def stand(self):
        print(f'{self.name} stands.')
        print(f'{self.name} score: {self.score}')
        time.sleep(1)


class Player(Participant):
   
    def __init__(self, name: str, balance: float, player_id: int) -> None:
        self.name = name
        self.balance = balance
        self.player_id = player_id

    def choose_bet_size(self):
        bet_size = float('inf')
        while bet_size > self.balance:
            if bet_size != float('inf'):
                print('Bet size larger than balance, please enter amount smaller than balance.')
            bet_size = float(input(f'{self.name} bet size: £ '))
        
        self.bet_size = bet_size
        self.balance -= bet_size

    def lose(self):
        self.round_result = 'lose'

    def win(self):
        self.balance += 2 * self.bet_size
        self.round_result = 'win'

    def bust(self):
        print(f'{self.name} score: {self.score}')
        print(f'PLAYER BUST')
        self.round_result = 'bust'
        self.busted = True

    def push(self):
        self.round_result = 'push'

    def double(self, deck):
        time.sleep(1)
        self.bet_size *= 2
        new_card = deck.cards.pop(0)
        self.hand.cards.append(new_card)
        print(f'{self.name} doubles... {str(new_card)}')
        self.play(deck, double=True)
        time.sleep(1)

    def blackjack(self):
        self.balance += self.bet_size * 2.5
        self.round_result = 'blackjack'

    def play(self, deck, double=False):
        self.score = self.hand.calculate_score()
        print(f'{self.name}\'s hand: {str(self.hand)}, Score: {self.score}')
            
        if self.score > 21:
            self.bust()
            return

        if self.score == 21:
            if len(self.hand.cards) == 2:
                self.got_blackjack = True
            self.stand()
            return

        if double:
            return

        decision = ui.find_player_decision(self)
        
        if decision.lower() == 's':
            self.stand()
            return

        if decision.lower() == 'd':
            self.double(deck)
            return

        if decision.lower() == 'h':
            self.hit(deck)

        self.play(deck)

        print(' ')
    
    def determine_result(self, dealer):
        if self.busted:
            ## player lost 
            self.lose()
            return

        if dealer.busted:
            ## player wins
            self.win()
            return

        if self.got_blackjack:
            if not dealer.got_blackjack:
                self.blackjack()
            else:
                self.push()
            return

        if self.score > dealer.score:
            ## player wins
            self.win()
            return

        if self.score == dealer.score:
            ## push
            self.push()
            return

        if self.score < dealer.score:
            ## player loses
            self.lose()
            return

    def process_balance(self):
        if self.balance <= 0:
            # cannot play, delete player
            return


class Dealer(Participant):
    name = 'Dealer'

    def bust(self):
        print(f'{self.name} score: {self.score}')
        print(f'DEALER BUST')
        self.busted = True
        time.sleep(1)

    def play(self, deck):
        self.busted = False
        self.score = self.hand.calculate_score()

        ui.print_dealers_hand_and_score(self)

        if self.score > 21:
            self.bust()
            return

        if self.score == 21 and len(self.hand.cards) == 2:
            self.got_blackjack = True
            self.stand()

        if self.score >= 17:
            self.stand()
            return

        self.hit(deck)
        self.play(deck)

class Players:
    all_busted = False

    def __init__(self, players: list[Player]) -> None:
        self.list = players

    def play_round(self, deck, dealer):
        self.all_busted = True
        for player in self.list:
            ui.print_borders(f'{player.name.upper()}\'S TURN')
            ui.print_bet_size(player)
            ui.print_dealers_hand(dealer)
            player.busted = False
            player.play(deck)
            if not player.busted:
                self.all_busted = False
            time.sleep(2)
        

    def choose_bet_sizes(self):
        for player in self.list:
            player.choose_bet_size()

    def determine_results(self, dealer):
        for player in self.list:
            player.determine_result(dealer)

    def process_balances(self):
        players_to_remove = []
        for player in self.list:
            if player.balance <= 0:
                print(f'{player.name} has run out of money.\nRemoving player...')
                players_to_remove.append(player)

        for player in players_to_remove:
            self.list.remove(player)
            
