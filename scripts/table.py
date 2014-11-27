import Tkinter as tk
from Tkinter import *
from PIL import ImageTk, Image
from util import *
import os

image_name = os.getcwd() + "/poker-table.JPG"
img = Image.open(image_name);
w, h = img.size
#canvas.pack(expand = YES, fill = BOTH)
card_size= (112, 156)

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

class Table():
	def __init__(self):
		self.size = img.size
		self.root = Tk()
		self.root.title("Heads-Up Poker")
		self.canvas = Canvas(self.root, width = w, height = h, bg = 'gray')
		self.canvas.pack( expand = YES, fill = BOTH)
		self.image = ImageTk.PhotoImage(file = image_name)
		self.canvas.create_image(0, 0, image = self.image, anchor = NW)
		self.seats = [((570, 650), (685, 650)), ((570, 10), (685, 10))]
		self.center = [(380, 300), (495, 300), (610, 300), (730,300), (850, 300)]
		self.images = []

		self.deal_button = Button(self.canvas, text = "Deal", command = self.deal, anchor = W)
		self.deal_button.configure(width = 10, activebackground = "#33B5E5",relief = FLAT)
		self.canvas.create_window(10, 10, anchor=NW, window=self.deal_button)

		#button.pack(side = TOP)
		#self.root.mainloop()


	def printImg(self, im_idx, location):
		self.canvas.create_image(location[0],location[1] , image = self.images[im_idx], anchor = NW)


	def update(self, hand_state):
		state = hand_state['state'];
		hole_cards = hand_state['hole_cards']
		print hole_cards
		if state == "pre-flop":
			for i, hole in enumerate(hole_cards):
				self.images.append(ImageTk.PhotoImage(file = imageName[hole[0]]))
				self.images.append(ImageTk.PhotoImage(file = imageName[hole[1]]))

				self.printImg(2*i, self.seats[i][0]);
				self.printImg(2*i+1, self.seats[i][1]);

		elif state == "pre-turn":
			flop = hand_state['flop'];
			for i, card in enumerate(flop):
				self.images.append(ImageTk.PhotoImage(file = imageName[card]))
				self.printImg(4+i, self.center[i])

		elif state == "pre-river":
			card = hand_state['turn'];
			self.images.append(ImageTk.PhotoImage(file = imageName[card]))
			self.printImg(7, self.center[3])

		elif state == "done":
			card = hand_state['river'];
			self.images.append(ImageTk.PhotoImage(file = imageName[card]))
			self.printImg(8, self.center[4])

	def deal(self):
		if self.hand==None:
			print "No player added"
		assert(self.hand!=None);
		if self.hand.getState()=="done":
			print "No more dealing"
		else:
			self.hand.deal();
			if self.hand.getState() == "pre-flop":
				for i, player in enumerate(self.hand.players):
					self.images.append(ImageTk.PhotoImage(file = hand.deck.imageName[player.cards[0]]))
					self.images.append(ImageTk.PhotoImage(file = hand.deck.imageName[player.cards[1]]))

					self.printImg(2*i, self.seats[i][0]);
					self.printImg(2*i+1, self.seats[i][1]);

			elif self.hand.getState() == "pre-turn":
				for i, card in enumerate(self.hand.flop):
					self.images.append(ImageTk.PhotoImage(file = hand.deck.imageName[card]))
					self.printImg(4+i, self.center[i])

			elif self.hand.getState() == "pre-river":
				card = self.hand.turn
				self.images.append(ImageTk.PhotoImage(file = hand.deck.imageName[card]))
				self.printImg(7, self.center[3])

			else:
				card = self.hand.river
				self.images.append(ImageTk.PhotoImage(file = hand.deck.imageName[card]))
				self.printImg(8, self.center[4])


if __name__ == "__main__":
	H = Player("Hossein", 100);
	R = Player("Reza", 100);
	hand = Hand([H,R], 0);
	a = Table(hand);
	#a.deal()
