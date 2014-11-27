from util import *
import random
from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator
import itertools
import matplotlib.pyplot as plt
import numpy as np

suits = ['S', 'H', 'D', 'C'];
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J','Q', 'K', 'A']; # 10 is missed (should be fixed)
cardsList = [];
imageName = {};
cardstoC = {};
cards_dirName = 'cards/'
for i, suit in enumerate(suits):
	for j, rank in enumerate(ranks):
		card = suit + rank;
		cardsList.append(card);
		imageName[card] = cards_dirName+card+'.JPG'
		cardstoC[card] = Card(j+2,i+1);

class betAgent:
	def act(self, observations,actionList):
		return "bet";
	def update_blief(self, observations):
		return


class checkAgent:
    def act(self, observations,actionList):
        if "check" in actionList:
            return "check"
        else:
            return "fold"
	def update_blief(self, observations):
		return

class foldAgent:
	def act(self, observations, actionList):
		return "fold"

class randAgent:
    def act(self,observations, actionList):
        action = random.sample(actionList,1)[0]
        print action
        return action

class sahinaz:
    def act(self,observation, actionList):
        if observation['state'] != "pre-flop":
            possible_cards = [card for card in cardsList if (card not in observation['board'] and
                                                            card not in observation['player'].cards)];
            possible_cards = [cardstoC[card] for card in possible_cards];
            scores = []
            board = [cardstoC[c] for c in observation['board']]
            for (card1, card2) in itertools.combinations(possible_cards,2):
                hole = [card1,card2]
                scores.append(HandEvaluator.evaluate_hand(hole, board))
            agent_cards = [cardstoC[c] for c in observation['player'].cards]
            agent_score = HandEvaluator.evaluate_hand(agent_cards,board)
            confidence = 1 - float(sum(np.greater(scores,agent_score)))/len(scores)
            if (confidence > .75) and ("bet" in actionList):
                action =  "bet"
            elif "check" in actionList:
                action =  "check"
            else:
                action =  "fold"
        else:
            if "check" in actionList:
                action =  "check"
            else:
                action =  "call"
        print action
        return action

class humanAgent:
	def act(self, observations, actionList):
		#print observations
		print actionList
		action = raw_input(observations['player'].name+", enter your action: ")
		return action

if __name__ == "__main__":
	players = [Player('Hossein', 100, agent = sahinaz()), Player('Reza', 100, agent = humanAgent())];
	heads_up = heads_up_poker(players, num_of_hands = 50);
	heads_up.play();

	print players[0].name + "'s stack is " + str(players[0].stack) + "(won " + str(players[0].num_of_hands_won)+ "hands)"
	print players[1].name + "'s stack is " + str(players[1].stack) + "(won " + str(players[1].num_of_hands_won)+ "hands)"
