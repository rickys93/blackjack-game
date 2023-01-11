import time
from user_interface import ui
from cards import Hand, Deck


class Participant:
    """
    A participant of the game can be a Player or a Dealer
    """
    current_hand = None
    score = None
    got_blackjack = False
    busted = False

    def hit(self, deck: Deck):
        """
        A participant will draw a card from the deck and 
        prints the card drawn
        """
        new_card = self.current_hand.deal_card(deck)
        ui.print_player_hits(self.name, new_card)

    def stand(self):
        """
        A participant will stand 
        """
        ui.print_player_stands(self)


class Player(Participant):
    """
    A player can split,double and play their turn
    """
    pending_hands = []
    completed_hands = []

    def __init__(self, name: str, balance: float) -> None:
        """
        Initialize the player with their name and balance
        """
        self.name = name
        self.balance = balance

    def choose_bet_size(self):
        """
        A player will choose the size of their bet and will have their balance updated
        """
        bet_size = ui.get_player_bet_size(self)

        self.bet_size = bet_size
        self.balance -= bet_size

    def split(self, deck: Deck):
        """
        A player will split their cards 
        """
        ui.print_player_splits(self)

        self.balance -= self.current_hand.bet_size
        hand_1 = Hand([self.current_hand.cards[0]], self.current_hand.bet_size)
        hand_2 = Hand([self.current_hand.cards[1]], self.current_hand.bet_size)
        hand_1.deal_card(deck)
        hand_2.deal_card(deck)
        self.current_hand = hand_1
        self.pending_hands.insert(0, hand_2)

        self.play(deck)

    def double(self, deck: Deck):
        """
        A player will double their bet and draws one card
        """
        self.current_hand.bet_size *= 2
        new_card = self.current_hand.deal_card(deck)

        ui.print_player_doubles(self, new_card)

        self.play(deck, hit_once=True)

    def calculate_profit_loss(self):
        """
        Calculate the player's profit/loss after each round
        """
        profit_loss = 0
        for hand in self.completed_hands:
            profit_loss += hand.calculate_profit_loss()

        return profit_loss

    def start_turn(self, deck: Deck, dealer):
        """
        Player will begin their turn 
        """
        ui.print_player_start_turn(self, dealer)

        while self.pending_hands:
            self.current_hand = self.pending_hands.pop(0)
            self.play(deck)
            completed_hands = self.completed_hands + [self.current_hand]
            self.completed_hands = completed_hands

    def find_valid_decisions(self):
        """
        Determine the valid decisions the player can make 
        based on their current hand and balance
        """
        valid_decisions = ['h', 's']
        if self.current_hand.split_possible() and self.balance >= self.bet_size:
            valid_decisions.append('sp')
        if len(self.current_hand.cards) == 2 and self.balance >= self.bet_size:
            valid_decisions.append('d')
        return valid_decisions

    def play(self, deck: Deck, hit_once=False):
        """
        A player will play their turn, make decisions and 
        update their current hand's score
        """
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

        valid_decisions = self.find_valid_decisions()
        decision = ui.find_player_decision(self, valid_decisions)

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


class Dealer(Participant):
    """
    A Dealer will play their turn and follow the rules 
    of the game 
    """
    name = 'Dealer'

    def bust(self):
        ui.print_dealer_bust(self)
        self.busted = True

    def play(self, deck: Deck):
        """
        A dealer will play their turn and draw card when 
        their score is less than 17 
        """
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
