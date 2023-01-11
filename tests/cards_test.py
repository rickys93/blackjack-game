import unittest

from cards import Card, Hand, Deck
from players import Player, Dealer


class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card('s', 'A')

    def test_init(self):
        self.assertEqual(self.card.suit, 's')
        self.assertEqual(self.card.rank, 'A')
        self.assertEqual(self.card.ascii_value, '\u2660')

    def test_str(self):
        self.assertEqual(str(self.card), 'A\u2660')

    def test_get_ascii_value(self):
        self.assertEqual(self.card.get_ascii_value(), '\u2660')


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck(2)

    def test_init(self):
        self.assertEqual(len(self.deck.cards), 104)

    def test_shuffle(self):
        # Since the implementation of the random.shuffle function is not deterministic,
        # we can't assert that the shuffle changed the order of the cards but we can
        # assert that the length of the deck hasn't changed
        length_before_shuffle = len(self.deck.cards)
        self.deck.shuffle()
        self.assertEqual(len(self.deck.cards), length_before_shuffle)

    def test_deal(self):
        dealer = object()
        players = [Player(), object()]
        self.deck.deal(players, dealer)
        self.assertEqual(len(players[0].pending_hands[0].cards), 2)
        self.assertEqual(len(players[1].pending_hands[0].cards), 2)
        self.assertEqual(len(dealer.current_hand.cards), 1)
        self.assertEqual(len(self.deck.cards), 99)


class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = Hand([Card('s', 'A'), Card('h', '2')])

    def test_init(self):
        self.assertEqual(len(self.hand.cards), 2)
        self.assertEqual(self.hand.bet_size, 0)

    def test_str(self):
        self.assertEqual(str(self.hand), 'A\u2660 2\u2665 ')

    def test_calculate_score(self):
        self.assertEqual(self.hand.calculate_score(), 13)


if __name__ == '__main__':
    unittest.main()
