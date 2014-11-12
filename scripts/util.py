import random
import sys
import os
import PIL
from PIL import Image

suits = ['H', 'S', 'D', 'C'];
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K']; 
cardsList = [];
for suit in suits:
	for rank in ranks:
		cardsList.append(suit + rank);
cards_dirName = 'cards/'
class Deck:
	def __init__(self):
		self.size = 52;
		self.cards = cardsList;
		self.imageName = {card:cards_dirName+card+'.JPG' for card in cardsList}

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
	def __init__(self,name,stack,params=None):
		self.name = name;
		self.stack = stack;
		self.cards = [];
		self.action = None;
		self.isDealer = False;
		self.amount = 0;

class Hand:
	def __init__(self, players, dealer):
		self.deck = Deck();
		self.deck.shuffle();
		self.pot = 0;
		self.dealer = dealer;
		self.players = players;
		self.state = "start"
		self.flop = [];
		self.turn = None;
		self.river = None;
		self.actionHist = [];
	
	def deal(self):
		if self.state == "start":
			self.players[0].cards.append(self.deck.pop());
			self.players[1].cards.append(self.deck.pop());
			self.players[0].cards.append(self.deck.pop());
			self.players[1].cards.append(self.deck.pop());
			self.state = "pre-flop";
		
		elif self.state == "pre-flop":	
			self.deck.pop();
			self.flop.append(self.deck.pop())
			self.flop.append(self.deck.pop())
			self.flop.append(self.deck.pop())
			self.state = "pre-turn"
		
		elif self.state == "pre-turn":	
			self.deck.pop();
			self.turn = self.deck.pop()
			self.state = "pre-river"

		elif self.state == "pre-river":	
			self.deck.pop();
			self.river = self.deck.pop()
			self.state = "done"
	def getState(self):
		return self.state;
	def update(self, player, action):
		return	
