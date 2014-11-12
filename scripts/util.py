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
		self.imageName = {card:cards_dirName+card+'.png' for card in cardsList}

	def shuffle(self):
		random.shuffle(self.cards);
	
	def pop(self):
		card = self.cards[0];
		del(self.cards[0]);
		return card;
	
	def peek(self):
		card = self.cards[0];
		return card;
	
	def showTop(self):
		topCard = self.cards[0];
		print topCard
		img = Image.open(self.imageName[topCard]);
		img.show()		
		
