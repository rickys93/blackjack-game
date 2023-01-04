import random
import time

from user_interface import UserInterface as ui

class Card:

    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit
        self.rank = rank
        self.ascii_value = self.get_ascii_value()
    
    def __str__(self) -> str:
        if self.suit == 's':
            suit = 'Spades'
        elif self.suit == 'h':
            suit = 'Hearts'
        elif self.suit == 'd':
            suit = 'Diamonds'
        elif self.suit == 'c':
            suit = 'Clubs'
        
        return f'{self.rank}{self.ascii_value}'

    def get_ascii_value(self):
        ascii_values = {
            's': '\u2660',  # spades
            'h': '\u2665',  # hearts
            'c': '\u2663',  # clubs
            'd': '\u2666'   # diamonds
        }
        return ascii_values[self.suit]


class Deck:
    suits = ['c', 'd', 'h', 's']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    cards = []

    def __init__(self, deck_size=1) -> None:
        self.deck_size = deck_size
        for i in range(self.deck_size):
            for suit in self.suits:
                for rank in self.ranks:
                    self.cards.append(Card(suit, rank))

    def shuffle(self) -> None:
        shuffled_deck = []
        deck_size = len(self.cards)

        while self.cards:
            random_int = random.randint(0, len(self.cards)-1)
            random_card = self.cards[random_int]
            shuffled_deck.append(random_card)
            self.cards.remove(random_card)

        self.cards = shuffled_deck

    def deal(self, players, dealer):
        for player in players:
            hand = Hand([self.cards.pop(0), self.cards.pop(0)], player.bet_size)
            player.pending_hands = [hand]

        hand = Hand([self.cards.pop(0)])
        dealer.current_hand = hand


class Hand:
    got_blackjack = False
    busted = False

    def __init__(self, cards, bet_size=None) -> None:
        self.cards = cards
        self.bet_size = bet_size
        self.score = self.calculate_score()
    
    def __str__(self) -> str:
        card_string = ''
        for card in self.cards:
            card_string += f'{card.rank}{card.ascii_value} '
        return card_string

    def calculate_score(self):
        score = 0
        number_of_aces = 0
        for card in self.cards:
            if card.rank in 'TJQK':
                score += 10
            elif card.rank == 'A':
                number_of_aces += 1
                score += 11
            else:
                score += int(card.rank)

            if score > 21 and number_of_aces:
                score -= 10
                number_of_aces -= 1

        return score

    def split_possible(self):
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def split(self):
        hands = [Hand(self.cards[0], Hand(self.cards[1]))]
        return hands

    def deal_card(self, deck):
        new_card = deck.cards.pop(0)
        self.cards.append(new_card)
        self.score = self.calculate_score()
        return new_card      

    def bust(self, player):
        ui.print_player_bust(player)
        self.round_result = 'bust'
        self.busted = True            

    def calculate_profit_loss(self):
        if self.round_result in ['lose', 'bust']:
            return -self.bet_size
        
        if self.round_result == 'blackjack':
            return self.bet_size
        
        if self.round_result == 'win':
            return self.bet_size

        if self.round_result == 'push':
            return 0

    def determine_result(self, dealer):
        if self.busted:
            ## player lost 
            self.round_result = 'lose'
            return

        if dealer.busted:
            ## player wins
            self.round_result = 'win'
            return

        if self.got_blackjack:
            if not dealer.got_blackjack:
                self.round_result = 'blackjack'
                self.bet_size *= 1.5
            else:
                self.round_result = 'push'  
            return

        if self.score > dealer.current_hand.score:
            ## player wins
            self.round_result = 'win'
            return

        if self.score == dealer.current_hand.score:
            ## push
            self.round_result = 'push' 
            return

        if self.score < dealer.current_hand.score:
            ## player loses
            self.round_result = 'lose'
            return



