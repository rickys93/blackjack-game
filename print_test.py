from players import Player
from cards import Hand, Card

player = Player('John', 1000, 1)
hand1 = Hand([Card('s', 'K'), Card('s', 'K'), Card('s', 'K')])
hand2 = Hand([Card('s', 'Q'), Card('s', '3'), Card('s', 'K')])
hand3 = Hand([Card('s', 'K'), Card('s', '6'), Card('s', 'K'), Card('s', 'K')])
player.pending_hands = [hand1]
player.current_hand = hand2
player.completed_hands = [hand3]



print(hand_string)

# string = ''
# middle_string = ''
# bottom_string = ''


# for hand in player.completed_hands:
#     middle_string += f'{str(hand)}  '

# for hand in hands:
#     space_length = int(len(str(hand)) / 2 - 2)
#     bottom_string += '  ' * space_length + str(hand.score) + ' ' * space_length + '  '
    

# space_length = int(len(str(player.current_hand)) / 2 - 2)
# top_string = ' ' * len(middle_string) + ' ' * space_length + 'vvv'

# for hand in [player.current_hand] + player.pending_hands:
#     middle_string += f'{str(hand)}  '

# difference = len(middle_string) - len(top_string)
# top_string += ' ' * difference

# print(top_string)
# print(middle_string)
# print(bottom_string)

