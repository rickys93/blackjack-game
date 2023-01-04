from cards import (
    Deck,
)
from players import (
    Dealer,
    Player,
)
from user_interface import ui


class BlackjackGame:
    """
    Command line interface Blackjack game
    """

    deck_size = 7
    currency_sign = ''
    
    dealer = Dealer()

    def __init__(self) -> None:
        pass
        
    def start_game(self):
        """
        Start new round
        """

        self.round.initialize()
        self.round.players_turn()

        # if all players are bust, can skip the dealer playing
        if not self.round.all_players_busted:
            self.round.dealer_turn()

        self.round.determine_results()
        self.round.process_balances()

    def play(self):
        # players = ui.get_player_names()
        # for player in players:
        #     self.round.players.append(Player(**player))
        self.players = [Player('John', 100), Player('Tim', 100)]
        self.round = Round(self.dealer, self.deck_size)
        self.round.players = self.players

        while self.round.players:
            self.start_game()

        ui.print_game_over()

class Round:

    def __init__(self, dealer: Dealer, deck_size: int) -> None:
        self.dealer = dealer
        self.deck_size = deck_size

    def initialize(self):
        """Get all objects ready for a new round.
        
        Ask for bet sizes, shuffle and deal."""

        self.deck = Deck(self.deck_size)
        ui.print_new_round(self.players)
        self.dealer.busted = False

        for player in self.players:
            player.completed_hands = []
            player.choose_bet_size()
            player.busted = False

        self.deck.shuffle()
        self.deck.deal(self.players, self.dealer)  
        ui.print_start_round(self.players, self.dealer)

    def all_busted(self):
        for player in self.players:
            for hand in player.completed_hands:
                if not hand.busted:
                    return False
        return True

    def players_turn(self):

        for player in self.players:
            player.start_turn(self.deck, self.dealer)        

        self.all_players_busted = self.all_busted() 

    def dealer_turn(self):
        ui.print_dealer_start_turn(self.dealer)
        self.dealer.play(self.deck)

    def determine_results(self):
        for player in self.players:
            for hand in player.completed_hands:
                hand.determine_result(self.dealer)
            
            player.round_profit_loss = player.calculate_profit_loss()
            player.balance += player.bet_size * len(player.completed_hands)
            player.balance += player.round_profit_loss

        ui.print_round_result(self)
            
    def process_balances(self):
        players_to_remove = []
        for player in self.players:
            if player.balance <= 0:
                ui.print_removing_player(player)
                
                players_to_remove.append(player)

        for player in players_to_remove:
            self.players.remove(player)


game = BlackjackGame()
game.play()








    



        


