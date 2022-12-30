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


class Participant:
    finished = False
    hand = None
    score = None

    def __init__(self) -> None:
        pass
    
    def hit(self, deck: Deck):
        self.hand.cards.append(deck.cards.pop(0))
        self.score = self.hand.calculate_score()

class Player(Participant):
    
    def __init__(self, name: str, funds: float) -> None:
        self.name = name
        self.funds = funds

    def stand(self):
        self.finished = True
        print(f'{self.name} stands')

    def bust(self):
        print(f'{self.name} score: {self.score}')
        print(f'Player Bust')

    def choose_bet_size(self):
        bet_size = float('inf')
        while bet_size > self.funds:
            if bet_size != float('inf'):
                print('Bet size larger than funds, please enter amount smaller than balance.')
            print(f'{self.name} balance: {self.funds}')
            bet_size = float(input(f'Choose bet size: '))
        self.bet_size = bet_size

    def lose(self):
        self.funds -= self.bet_size

    def win(self):
        self.funds += self.bet_size

    def play(self, deck):
        self.score = self.hand.calculate_score()

        decision = ''
        while decision.lower() != 's':
            print(f'{self.name}\'s turn: {str(self.hand)}')
            print(f'Score: {self.score}')
            if self.score == 21:
                self.stand()
                break

            if self.score > 21:
                self.bust()
                break

            decision = input('Hit or stand? (H/S) ')
            if decision.lower() == 'h':
                self.hit(deck)
            if decision.lower() == 's':
                self.stand()


class Dealer(Participant):
    name = 'Dealer'

    def play(self):
        print('Dealer\'s Turn')
        while self.score <= 17:
            if self.score > 21:
                self.bust()
            self.hit()     


class Participants:
    
    def __init__(self, players: list[Player], dealer: Dealer) -> None:
        self.players = players
        self.dealer = dealer  


class BlackjackGame:
    deck = Deck()

    def __init__(self) -> None:
        self.players = self.get_player_names()
        self.dealer = Dealer()

    def get_player_names(self):
        player_number = 1
        players = []
        name = 'None'
        while len(players) <= 4 and name:
            name = input(f'Type name of player {player_number} (leave blank if completed): ')
            if not name and len(players) > 0:
                break

            funds = input(f'How much money is {name} playing with? ')
            player = Player(name, float(funds))
            players.append(player)
            player_number += 1

        return players

    def initialize_round(self):
        for player in self.players:
            player.choose_bet_size()

        self.deck.shuffle()
        self.deck.deal(self.players, self.dealer)

        print(f'Dealer: {str(self.dealer.hand)}')
        player_hand_message = ''
        for player in self.players:
            player_hand_message += f'{player.name}: {str(player.hand)}, '
        print(player_hand_message[:-2])

    def play_round(self):
        self.initialize_round()

        for player in self.players:
            player.play(self.deck)

        self.dealer.play()





        



game = BlackjackGame()
game.play_round()









    



        


