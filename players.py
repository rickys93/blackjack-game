class Participant:
    finished = False
    hand = None
    score = None

    def __init__(self) -> None:
        pass
    
    def hit(self, deck):
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