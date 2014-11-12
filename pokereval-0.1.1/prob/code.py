from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator
import itertools
import copy

card1 = Card(14,1)
card2 = Card(14,2)
hole = [card1, card2]
board = []
score = HandEvaluator.evaluate_hand(hole, board)

cards = []
for i in range(2,15):
    for j in range(1,5):
        if (Card(i,j) == card1) or (Card(i,j) == card2):
            continue
        cards.append(Card(i,j))

cardsCopy = copy.deepcopy(cards)
wins = 0.0
count = 0
i = 0
next_scores = []

for board in itertools.combinations(cards,3):
    count += 1
    next_scores.append(HandEvaluator.evaluate_hand(hole,list(board)))
print sum(next_scores)/len(next_scores)
print count

'''
for hand in itertools.combinations(cards,2):
    cardsCopy.remove(hand[0])
    cardsCopy.remove(hand[1])
    for board in itertools.combinations(cardsCopy,5):
        count += 1
        print count
        if HandEvaluator.evaluate_hand(hand,list(board)) < score:
            wins += 1
    print "---------------------------------------------------"
    i += 1
    cardsCopy.append(hand[0])
    cardsCopy.append(hand[1])

print wins/(count)
print count
'''
