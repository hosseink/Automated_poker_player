import Tkinter as tk
from Tkinter import *
from PIL import ImageTk, Image
from util import *
import tkFont
import sys
from StringIO import StringIO

image_name = "/Users/Carrie/Desktop/CS221/project/scripts/poker-table.JPG"
import os

image_name = os.getcwd()+"/poker-table.JPG"
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
facedown_card = cards_dirName + 'facedown_card.JPG'
for i, suit in enumerate(suits):
        for j, rank in enumerate(ranks):
                card = suit + rank;
                cardsList.append(card);
                imageName[card] = cards_dirName+card+'.JPG'
                cardstoC[card] = Card(j+2,i+1);

class Table():
	def __init__(self, players):
		self.players = players;
		self.size = img.size
		self.root = Tk()
		self.root.title("Heads-Up Poker")
		self.canvas = Canvas(self.root, width = w, height = h, bg = 'gray')
		self.canvas.pack( expand = YES, fill = BOTH)
		self.image = ImageTk.PhotoImage(file = image_name)
		self.canvas.create_image(0, 0, image = self.image, anchor = NW)
		self.font = tkFont.Font(family='Helvetica',size=30);
		self.potAmount = 0;
		self.stack1Amount = self.players[0].stack
		self.stack2Amount = self.players[1].stack
		self.canvas.create_text((220, 378), text = "POT", font = self.font);
		self.next_action0 = self.canvas.create_text((680, 200), text = "", font = self.font);
		self.next_action1 = self.canvas.create_text((680, 600), text = "", font = self.font);

		self.potRec = self.canvas.create_rectangle((260, 360, 320, 395), fill = 'white')
		self.canvas.create_rectangle((910, 135, 970, 170), fill = 'white')
		self.canvas.create_rectangle((910, 645, 970, 680), fill = 'white')
		self.pot = self.canvas.create_text((265, 365), text = str(self.potAmount), font = self.font, anchor = NW)
		self.stack1 = self.canvas.create_text((915, 140), text = str(self.stack1Amount), font = self.font, anchor = NW)
		self.stack2 = self.canvas.create_text((915, 650), text = str(self.stack2Amount), font = self.font, anchor = NW)
	
		self.updateStacks();	

		self.seats = [((570, 10), (685, 10)),((570, 650), (685, 650)) ]
		self.center = [(380, 300), (495, 300), (610, 300), (730,300), (850, 300)]
		self.images = []
		self.canvasImages = [];
		
		'''if players[1].agent.fromTable:
			#sys.stdin = StringIO();
			#sys.stdin.truncate(0);
			self.bet2_button = Button(self.canvas, text = "Bet", command = self.bet2, anchor = W)
			self.bet2_button.configure(width = 5, activebackground = "#33B5E5",relief = FLAT)
			self.canvas.create_window(545, 600, anchor=NW, window=self.bet2_button)	
=======
		self.deal_button = Button(self.canvas, text = "Deal", command = self.deal, anchor = W)
		self.deal_button.configure(width = 10, activebackground = "#33B5E5",relief = FLAT)
		self.canvas.create_window(10, 10, anchor=NW, window=self.deal_button)
>>>>>>> 5bc0db33e6e2367d54c9ed335a740dd298869569

			self.check2_button = Button(self.canvas, text = "Check", command = self.check2, anchor = W)
			self.check2_button.configure(width = 5, activebackground = "#33B5E5",relief = FLAT)
			self.canvas.create_window(613, 600, anchor=NW, window=self.check2_button)	

			self.call2_button = Button(self.canvas, text = "Call", command = self.call2, anchor = W)
			self.call2_button.configure(width = 5, activebackground = "#33B5E5",relief = FLAT)
			self.canvas.create_window(681, 600, anchor=NW, window=self.call2_button)	

			self.fold2_button = Button(self.canvas, text = "Fold", command = self.fold2, anchor = W)
			self.fold2_button.configure(width = 5, activebackground = "#33B5E5",relief = FLAT)
			self.canvas.create_window(749, 600, anchor=NW, window=self.fold2_button)'''	
		#button.pack(side = TOP)
		#self.root.mainloop()
	'''def bet2(self):
		if 'bet' in self.players[1].agent.actionList:
			#sys.stdin.truncate(0);
			#sys.stdin.write('bet')
	#		sys.stdin.seek(0)
			return
	def check2(self):
		if 'check' in self.players[1].agent.actionList:
			#sys.stdin.truncate(0);
			#sys.stdin.write('check')
	#		sys.stdin.seek(0)
			return
	def call2(self):
		if 'call' in self.players[1].agent.actionList:
			#sys.stdin.truncate(0);
			#sys.stdin.write('call')
	#		sys.stdin.seek(0)
			return
	def fold2(self):
		if 'fold' in self.players[1].agent.actionList:
			#sys.stdin.truncate(0);
			#sys.stdin.write('fold')
	#		sys.stdin.seek(0)
			return
	'''
	def update_action(self, action, player):
		if player ==0:
			self.canvas.itemconfig(self.next_action0, text = action);
		else:
			self.canvas.itemconfig(self.next_action1, text = action);
			
	def printImg(self, im_idx, location):
		return self.canvas.create_image(location[0],location[1] , image = self.images[im_idx], anchor = NW)

	def updateStacks(self):
		#self.canvas.delete(self.pot);
		#self.canvas.delete(self.potRec) 
		#self.canvas.delete(self.stack1);
		#self.canvas.delete(self.stack2);
		#self.potRec = self.canvas.create_rectangle((260, 360, 320, 395), fill = 'white')
		#self.pot = self.canvas.create_text((265, 365), text = str(self.potAmount), font = self.font, anchor = NW)
		self.canvas.itemconfig(self.pot, text = str(self.potAmount))
		self.canvas.itemconfig(self.stack1, text = str(self.stack1Amount))
		self.canvas.itemconfig(self.stack2, text = str(self.stack2Amount))

	def update(self, hand_state):
		self.potAmount = hand_state["pot"];
		self.stack1Amount = hand_state['stacks'][0];
		self.stack2Amount = hand_state['stacks'][1];
		self.updateStacks()
		state = hand_state['state'];
		hole_cards = hand_state['hole_cards']
		show_cards = hand_state['show_cards'];
		if show_cards:
			if state == "pre-flop":
				print hole_cards
				for i, hole in enumerate(hole_cards):
					if i==0:
						self.images.append(ImageTk.PhotoImage(file = facedown_card))
						self.images.append(ImageTk.PhotoImage(file = facedown_card))
					else:
						self.images.append(ImageTk.PhotoImage(file = imageName[hole[0]]))
						self.images.append(ImageTk.PhotoImage(file = imageName[hole[1]]))
					
					im = self.printImg(2*i, self.seats[i][0]);
					self.canvasImages.append(im)
					im = self.printImg(2*i+1, self.seats[i][1]);
					self.canvasImages.append(im)

			elif state == "pre-turn":
				flop = hand_state['flop'];
				for i, card in enumerate(flop):
					self.images.append(ImageTk.PhotoImage(file = imageName[card]))
					im = self.printImg(4+i, self.center[i])
					self.canvasImages.append(im)

			elif state == "pre-river":
				card = hand_state['turn'];
				self.images.append(ImageTk.PhotoImage(file = imageName[card]))
				im = self.printImg(7, self.center[3])

			elif state == "done":
				card = hand_state['river'];
				self.images.append(ImageTk.PhotoImage(file = imageName[card]))
				im = self.printImg(8, self.center[4])
				self.canvasImages.append(im)
			elif state == "show_cards":
				self.images.append(ImageTk.PhotoImage(file = imageName[hole_cards[0][0]]))
				self.images.append(ImageTk.PhotoImage(file = imageName[hole_cards[0][1]]))
				self.canvas.delete(self.canvasImages[0])
				self.canvas.delete(self.canvasImages[1])
				im = self.printImg(9, self.seats[0][0]);
				self.canvasImages.append(im)
				im = self.printImg(10, self.seats[0][1]);
				self.canvasImages.append(im)
				

	def reset(self):
		for im in self.canvasImages:
			self.canvas.delete(im);
		self.images = []
		self.canvasImages = [];
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
