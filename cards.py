import random

class Card:

    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit
        self.rank = rank
    
    def __str__(self) -> str:
        if self.suit == 's':
            suit = 'Spades'
        elif self.suit == 'h':
            suit = 'Hearts'
        elif self.suit == 'd':
            suit = 'Diamonds'
        elif self.suit == 'c':
            suit = 'Clubs'
        
        return f'{self.rank} of {suit}'


class Deck:
    suits = ['c', 'd', 'h', 's']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    cards = []

    def __init__(self) -> None:
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
            hand = Hand([self.cards.pop(0), self.cards.pop(0)])
            player.hand = hand

        hand = Hand([self.cards.pop(0)])
        dealer.hand = hand


class Hand:

    def __init__(self, cards) -> None:
        self.cards = cards
    
    def __str__(self) -> str:
        card_string = ''
        for card in self.cards:
            card_string += f'{card.rank}{card.suit} '
        return card_string

    def calculate_score(self):
        score = 0
        for card in self.cards:
            if card.rank in 'TJQK':
                score += 10
            elif card.rank == 'A':
                score += 11
                if score > 21:
                    score -= 10
            else:
                score += int(card.rank)
        return score