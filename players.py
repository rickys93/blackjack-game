import time
from user_interface import ui
from cards import Hand, Deck



class Participant:
    current_hand = None
    score = None
    got_blackjack = False
    busted = False
    
    def hit(self, deck):
        new_card = self.current_hand.deal_card(deck)
        ui.print_player_hits(self.name, new_card)

    def stand(self):
        ui.print_player_stands(self)
        

class Player(Participant):
    pending_hands = []
    completed_hands = []
   
    def __init__(self, name: str, balance: float) -> None:
        self.name = name
        self.balance = balance

    def choose_bet_size(self):
        bet_size = ui.get_player_bet_size(self)
        
        self.bet_size = bet_size
        self.balance -= bet_size

    def split(self, deck):
        ui.print_player_splits(self)
        
        self.balance -= self.current_hand.bet_size
        hand_1 = Hand([self.current_hand.cards[0]], self.current_hand.bet_size)
        hand_2 = Hand([self.current_hand.cards[1]], self.current_hand.bet_size)
        hand_1.deal_card(deck)
        hand_2.deal_card(deck)
        self.current_hand = hand_1
        self.pending_hands.insert(0, hand_2)

        self.play(deck)

    def double(self, deck):        
        self.current_hand.bet_size *= 2
        new_card = self.current_hand.deal_card(deck)

        ui.print_player_doubles(self, new_card)
        
        self.play(deck, hit_once=True)
        
    def calculate_profit_loss(self):
        profit_loss = 0
        for hand in self.completed_hands:
            profit_loss += hand.calculate_profit_loss()
        
        return profit_loss

    def start_turn(self, deck, dealer):
        ui.print_player_start_turn(self, dealer)

        while self.pending_hands:
            self.current_hand = self.pending_hands.pop(0)
            self.play(deck)
            completed_hands = self.completed_hands + [self.current_hand]
            self.completed_hands = completed_hands

    def play(self, deck, hit_once=False):
        self.current_hand.score = self.current_hand.calculate_score()
        ui.display_player_hands(self)
            
        if self.current_hand.score > 21:
            self.current_hand.bust(self)
            return

        if self.current_hand.score == 21:
            if len(self.current_hand.cards) == 2:
                self.current_hand.got_blackjack = True
            self.stand()
            return

        if hit_once:
            return

        decision = ui.find_player_decision(self)
        
        if decision.lower() == 's':
            self.stand()
            return

        if decision.lower() == 'sp':
            self.split(deck)
            return

        if decision.lower() == 'd':
            self.double(deck)
            return

        if decision.lower() == 'h':
            self.hit(deck)

        self.play(deck)

    def process_balance(self):
        if self.balance <= 0:
            # cannot play, delete player
            return


class Dealer(Participant):
    name = 'Dealer'

    def bust(self):
        ui.print_dealer_bust(self)
        self.busted = True

    def play(self, deck):
        self.current_hand.score = self.current_hand.calculate_score()

        ui.print_dealers_hand_and_score(self)

        if self.current_hand.score > 21:
            self.bust()
            return

        if self.current_hand.score == 21 and len(self.current_hand.cards) == 2:
            self.got_blackjack = True
            self.stand()
            return

        if self.current_hand.score >= 17:
            self.stand()
            return

        self.hit(deck)
        self.play(deck)



            
