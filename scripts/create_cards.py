import sys
import os
from PIL import Image
#from util import Deck

directory = "new_cards2/"
#os.system("mkdir " + directory)
card_size= (112, 156)

suits = ['H', 'S', 'D', 'C'];
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J','Q', 'K']; # 10 is missed (should be fixed) 

if __name__ == "__main__":
	'''image = Image.open("poker.cards.bypx.png");
	width, height = image.size
	delta_w = width/len(ranks);
	delta_h = height/len(suits)
	for i, suit in enumerate(suits):
		for j, rank in enumerate(ranks):
			im = image.crop((j * delta_w, i * delta_h, (j+1) * delta_w, (i+1) * delta_h));
			im.thumbnail((im.size[0]/2, im.size[1]/2), Image.ANTIALIAS);
			im.save(directory + suit + rank + '.JPG');'''
	facedown_card =  Image.open("facedown_card.jpg");
	facedown_card.thumbnail(card_size, Image.ANTIALIAS);
	facedown_card.save('facedown_card.JPG');

