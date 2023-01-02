import time
from user_interface import UserInterface as ui

class Participant:
    hand = None
    score = None
    busted = False
    got_blackjack = False

    def __init__(self) -> None:
        pass
    
    def hit(self, deck):
        time.sleep(1)
        new_card = deck.cards.pop(0)
        self.hand.cards.append(new_card)
        print(f'{self.name} hits... {str(new_card)}')

    def stand(self):
        print(f'{self.name} stands.')
        print(f'{self.name} score: {self.score}')
        time.sleep(1)


class Player(Participant):
    
    def __init__(self, name: str, balance: float) -> None:
        self.name = name
        self.balance = balance

    def choose_bet_size(self):
        bet_size = float('inf')
        while bet_size > self.balance:
            if bet_size != float('inf'):
                print('Bet size larger than balance, please enter amount smaller than balance.')
            bet_size = float(input(f'{self.name} bet size: £'))
        
        self.bet_size = bet_size

    def lose(self):
        print(f'{self.name} loses £{self.bet_size}')
        self.balance -= self.bet_size

    def win(self):
        print(f'{self.name} wins £{self.bet_size}!')
        self.balance += self.bet_size

    def bust(self):
        print(f'{self.name} score: {self.score}')
        print(f'PLAYER BUST')
        self.busted = True

    def push(self):
        print(f'{self.name} push')

    def blackjack(self):
        win_amount = self.bet_size * 1.5
        print(f'BLACKJACK!!\n{self.name} wins £{win_amount}!')
        self.balance += win_amount

    def play(self, deck):
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

        decision = input('Hit or stand? (H/S) ')
        if decision.lower() == 's':
            self.stand()
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
                self.blackjack(dealer)
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
    busted = False

    def bust(self):
        print(f'{self.name} score: {self.score}')
        print(f'DEALER BUST')
        self.busted = True

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
    all_busted = None

    def __init__(self, players: list[Player]) -> None:
        self.list = players

    def play_round(self, deck, dealer):
        self.all_busted = True
        for player in self.list:
            ui.print_borders(f'{player.name.upper()}\'S TURN')
            ui.print_dealers_hand(dealer)
            player.busted = False
            player.play(deck)
            if not player.busted:
                self.all_busted = False

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
            
