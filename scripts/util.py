import random
import sys
import os
import PIL
from PIL import Image
import copy
from pokereval.card import Card
from pokereval.hand_evaluator import HandEvaluator
from table import *
import time
from tkSimpleDialog import askstring

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

class Deck:
	def __init__(self):
		self.size = 52;
		self.cards = copy.deepcopy(cardsList);
		self.imageName = imageName;
		self.cardstoC = cardstoC

	def shuffle(self):
		random.shuffle(self.cards);
	
	def pop(self):
		card = self.cards[0];
		del(self.cards[0]);
		self.size -= 1;
		return card;
	
	def peek(self):
		card = self.cards[0];
		return card;
	
	def showTop(self):
		topCard = self.cards[0];
		print topCard
		img = Image.open(self.imageName[topCard]);
		img.show()		

class Player:
	def __init__(self,name,stack,params=None,opp_params = None, agent = None):
		self.name = name;
		self.stack = stack;
		self.cards = [];
		self.isDealer = False;
		self.agent = agent;
		self.params = params;
		self.opp_params = opp_params;
		self.num_of_hands_won = 0;
		self.action = None;
		self.actionList = [];

class Hand:
	def __init__(self, players, dealer = 0, blind = 2, table = None):
		self.deck = Deck();
		self.deck.shuffle();
		self.pot = 0;
		self.dealer = dealer;
		players[0].cards = [];
		players[1].cards = [];
		players[dealer].isDealer = True;
		players[1-dealer].isDealer = False;
		self.players = players;
		self.state = "start"
		self.blind = blind;
		self.flop = [];
		self.turn = None;
		self.river = None;
		self.board = [];
		self.table = table;
		self.actionHist = {};
	
	def deal(self):
		if self.state == "start":
			self.players[0].cards.append(self.deck.pop());
			self.players[1].cards.append(self.deck.pop());
			self.players[0].cards.append(self.deck.pop());
			self.players[1].cards.append(self.deck.pop());
			print self.players[0].name + ":" ,  self.players[0].cards;
			print self.players[1].name + ":" , self.players[1].cards;
			self.state = "pre-flop";
		
		elif self.state == "pre-flop":	
			self.deck.pop();
			self.flop.append(self.deck.pop())
			self.flop.append(self.deck.pop())
			self.flop.append(self.deck.pop())
			self.board.extend(self.flop)
			self.state = "pre-turn"
		
		elif self.state == "pre-turn":	
			self.deck.pop();
			self.turn = self.deck.pop()
			self.board.append(self.turn);
			self.state = "pre-river"

		elif self.state == "pre-river":	
			self.deck.pop();
			self.river = self.deck.pop()
			self.board.append(self.river)
			self.state = "done"
	
	def getState(self):
		return self.state;
	def update(self, player, amount):
		player.stack -= amount;
		self.pot += amount;
	def bid(self):
		state = self.state;
		self.actionHist[state] = [];
		player_turn = 1 - self.dealer;
		if state == "pre-flop":
			actionList = ["bet", "fold", "call"];
		else:
			actionList = ["bet", "fold", "check"];
			
		observation = {'player': self.players[player_turn], 'state': state, 
			       'board': self.board, 'pot': self.pot,  'History': self.actionHist};
		action = self.players[player_turn].agent.act(observation, actionList);
		self.table.update_action(action, player_turn)	
		self.table.update_action('', 1-player_turn)	
		assert(action in actionList);

		if action == "fold":
			return 1 - player_turn; 
			
		if state=="pre-flop":
			self.update(self.players[player_turn], self.blind/2);

		if action == "bet":
			self.update(self.players[player_turn], self.blind);
		self.actionHist[state].append((player_turn, action))
		self.updateTable(False)	
			
		while True:
			self.printStatus()	
			player_turn = 1 - player_turn;
			new_actionList = [];
			if action == "call":
				new_actionList = ["bet", "check", "fold"];
			if action == "bet":
				new_actionList = ["bet", "call", "fold"];
			elif action == "check":
				new_actionList = ["bet", "check", "fold"];
				
			observation = {'player': self.players[player_turn], 'state': state, 
				       'board': self.board, 'pot': self.pot, 'History': self.actionHist};
			new_action = self.players[player_turn].agent.act(observation, new_actionList);
			assert (new_action in new_actionList);

			self.table.update_action(new_action, player_turn)	
			self.table.update_action('', 1-player_turn)	

			self.actionHist[state].append((player_turn, new_action))

			if new_action == "call":
				self.update(self.players[player_turn], self.blind);
			if new_action == "bet" and action == "bet":
				self.update(self.players[player_turn], 2 * self.blind);
			if new_action == "bet" and (action == "check" or action=="call"):
				self.update(self.players[player_turn], self.blind);

			if new_action=="check" or new_action == "fold" or new_action == "call":
				break;
			action = new_action;
			self.updateTable(False)	

		if new_action == "fold":
			return 1 - player_turn; 
		return -1;
	
	def updateTable(self, show_cards = True):
		if self.table!= None:
			self.table.update({"state": self.state, "hole_cards":[self.players[0].cards, self.players[1].cards], 
					   "flop": self.flop, "turn":self.turn, "river":self.river, "pot": self.pot, 
					   "stacks":[self.players[0].stack, self.players[1].stack], 'show_cards':show_cards})
		
	def printStatus(self):
		print self.players[0].name + "'s stack: " + str(self.players[0].stack)
		print self.players[1].name + "'s stack: " + str(self.players[1].stack)
		print "pot: " + str(self.pot)
	def play(self):
		self.players[self.dealer].stack -= self.blind;
		self.players[1-self.dealer].stack -= self.blind/2;
		self.pot += 3*self.blind/2;

		while True:	
			self.deal();
			self.table.update_action('', 0);
			self.table.update_action('', 1);
			self.updateTable()
			self.printStatus();
			print self.board;
			winner = self.bid();
			if winner > -1:
				break;
			if self.state == "done":
				board = [self.deck.cardstoC[c] for c in self.board];
				hole0 = [self.deck.cardstoC[c] for c in self.players[0].cards]
				hole1 = [self.deck.cardstoC[c] for c in self.players[1].cards]
				score0 = HandEvaluator.evaluate_hand(hole0, board)
				score1 = HandEvaluator.evaluate_hand(hole1, board)
				winner = 0;
				if score1 > score0:
					winner = 1;
				break;
		print self.players[winner].name + ' won the hand.\n'
		self.players[winner].stack += self.pot;
		self.players[winner].num_of_hands_won += 1;
		return winner;
			

class heads_up_poker:
	def __init__(self, players, dealer = 0, num_of_hands = 1, blind = 2):
		self.players = players;
		self.table = Table(players)
		self.dealer = dealer;
		self.num_of_hands = num_of_hands;
		self.num_of_hands_played = 0;
		self.blind = blind;
	def play(self):
		while self.num_of_hands_played < self.num_of_hands:
			self.table.reset();
			hand = Hand(self.players, self.dealer, self.blind, self.table);
			hand.play();
			self.dealer = 1 - self.dealer;
			self.num_of_hands_played += 1;
		
class CheckAgent:
	def __init__(self):
		self.fromTable = False
	def act(self, observations, actionList):
		return actionList[0];
	def update_blief(self, observations):
		return

class FoldAgent:
	def __init__(self):
		self.fromTable = False
	def act(self, observations, actionList):
		return "fold"

class HumanAgent:
	def __init__(self):
		self.fromTable = True
		self.actionList = []
		self.action = None;
	def act(self, observations, actionList):
		#print observations
		#print actionList
		#action = raw_input(observations['player'].name+", enter your action: ")
		#while action not in actionList:
		#	print "Invalid action\n"
		#	action = raw_input(observations['player'].name+", enter your action: ")
		#return action
		self.actionList = actionList;
		print actionList
		#action = raw_input(observations['player'].name+", enter your action: ")
		action = askstring("Action","your action? (" + '/'.join([str(action) for action in actionList])+ ")")
		while action not in actionList:
			action = askstring("Action","invalid action! (" + '/'.join([str(action) for action in actionList])+ ")")
		self.actionList = [];
		return action

class HumanAgent0:
	def __init__(self):
		self.fromTable = False
		self.actionList = []
		self.action = None;
	def act(self, observations, actionList):
		#print observations
		print actionList
		action = raw_input(observations['player'].name+", enter your action: ")
		while action not in actionList:
			print "Invalid action\n"
			action = raw_input(observations['player'].name+", enter your action: ")
		return action
		
 
if __name__ == "__main__":
	player1 =Player('Hossein', 100, agent = CheckAgent());
	player2 =Player('Reza', 100, agent = HumanAgent());
	players = [player1, player2] 
	#table = Table(players)
	heads_up = heads_up_poker(players, num_of_hands = 5, dealer = 1);
	heads_up.play();
	
	print players[0].name + "'s stack is " + str(players[0].stack) + "(won " + str(players[0].num_of_hands_won)+ "hands)"	
	print players[1].name + "'s stack is " + str(players[1].stack) + "(won " + str(players[1].num_of_hands_won)+ "hands)"	
