from players import Dealer, Player
from round import Round
from user_interface import ui


class BlackjackGame:
    """
    Command line interface Blackjack game
    """

    def __init__(self) -> None:
        """
        Initialize the game with default values for number of decks and empty players list
        """
        self.DEFAULT_DECK_SIZE = 7
        self.players = []
        self.dealer = Dealer()

    def start_game(self):
        """
        Start new round. 
        Initialize the round, play players turn, play dealer's turn if required,
        determine results and process balances
        """

        self.round.initialize()
        self.round.players_turn()

        # if all players are bust, can skip the dealer playing
        if not self.round.all_players_busted:
            self.round.dealer_turn()

        self.round.determine_results()
        self.round.process_balances()

    def add_players(self, players):
        """
        Add players to the game
        """
        for player in players:
            self.players.append((Player(**player)))

    def play(self):
        """
        Start the game, get player names, add them, start rounds and repeat until game over
        """
        players = ui.get_player_names()
        self.add_players(players)

        self.round = Round(self.players, self.dealer, self.DEFAULT_DECK_SIZE)

        while self.round.players:
            self.start_game()

        ui.print_game_over()


game = BlackjackGame()
game.play()
