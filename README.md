# Blackjack Game
This is a command line interface Blackjack game implemented in Python. The game uses classes for the Deck, Player, and Dealer, as well as a user interface module for input and output.

## Installation
The Blackjack Game can be run directly from your command line without any additional installation.

You need to have python3 installed on your system, you can check this by running python3 -v on your command line. If python3 is not installed you can download it from the official website https://www.python.org/downloads/

Once you have python3 installed, you can start the game by running the `main.py` script on your command line.

To run the script open your command line, navigate to the directory where the game is located and run the following command:

`python3 main.py`
This will start the game and you will be prompted to enter the names and initial balances of the players. Once the players are added, the game will begin.

You should be able to play the game on any system that supports python3.

Requirements
- python3

## How to Play
To start the game, run the blackjack.py script in your command line. The game will prompt you to enter the names of the players and their initial balances. Once the players are added, the game will begin.

Each round, players will be prompted to place their bets. The game will then deal two cards to each player and one card to the dealer. Players will have the option to hit, stand, split, or double down. If a player splits their hand, they will play each hand individually. If a player doubles down, they will receive one more card and their bet will be doubled.

After all the players have completed their turn, the dealer will play. The dealer will hit until their hand is worth at least 17 points. If the dealer busts, all remaining players win. If the dealer does not bust, the player's hands will be compared to the dealer's hand. If a player's hand is worth more than the dealer's hand, the player wins. If the player's hand is worth less than the dealer's hand, the player loses. If the player's hand is worth the same as the dealer's hand, it is a push and the player's bet is returned.
