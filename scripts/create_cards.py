import sys
import os
from PIL import Image
#from util import Deck

directory = "new_cards2/"
os.system("mkdir " + directory)

suits = ['H', 'S', 'D', 'C'];
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J','Q', 'K']; # 10 is missed (should be fixed) 

if __name__ == "__main__":
	image = Image.open("poker.cards.bypx.png");
	width, height = image.size
	delta_w = width/len(ranks);
	delta_h = height/len(suits)
	for i, suit in enumerate(suits):
		for j, rank in enumerate(ranks):
			new_image = image.crop((j * delta_w, i * delta_h, (j+1) * delta_w, (i+1) * delta_h));
			new_image.save(directory + suit + rank + '.png');
	'''for card in d.cards:
		img_name = d.imageName[card];
		im = Image.open(img_name);
		im.thumbnail((im.size[0]/2, im.size[1]/2), Image.ANTIALIAS);
		im.save(directory + card + ".JPG");'''
