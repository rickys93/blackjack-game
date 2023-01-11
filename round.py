from players import Player, Dealer
from cards import Deck
from user_interface import ui


class Round:
    players = []

    def __init__(self, players, dealer: Dealer, deck_size: int) -> None:
        """
        Initialize the round with players, dealer and number of decks
        """
        self.players = players
        self.dealer = dealer
        self.deck_size = deck_size

    def add_player(self, player):
        self.players.append(player)

    def initialize(self):
        """
        Get all objects ready for a new round. Ask for bet sizes, shuffle and deal.
        """
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
        """
        Check if all players are bust
        """
        for player in self.players:
            for hand in player.completed_hands:
                if not hand.busted:
                    return False
        return True

    def players_turn(self):
        """
        Play each player's turn
        """
        for player in self.players:
            player.start_turn(self.deck, self.dealer)

        self.all_players_busted = self.all_busted()

    def dealer_turn(self):
        """
        Play dealer's turn
        """
        ui.print_dealer_start_turn(self.dealer)
        self.dealer.play(self.deck)

    def determine_results(self):
        """
        Determine results for each hand for each player and 
        update their balances based on those results
        """
        for player in self.players:
            for hand in player.completed_hands:
                hand.determine_result(self.dealer)

            player.round_profit_loss = player.calculate_profit_loss()
            player.balance += player.bet_size * len(player.completed_hands)
            player.balance += player.round_profit_loss

        ui.print_round_result(self)

    def process_balances(self):
        """
        Remove players with zero or negative balance
        """
        players_to_remove = []
        for player in self.players:
            if player.balance <= 0:
                ui.print_removing_player(player)
                self.players.remove(player)
