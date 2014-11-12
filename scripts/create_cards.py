import sys
import os
from PIL import Image
from util import Deck

directory = "new_cards/"
os.system("mkdir " + directory)

if __name__ == "__main__":
	d = Deck();
	for card in d.cards:
		img_name = d.imageName[card];
		im = Image.open(img_name);
		im.thumbnail((im.size[0]/2, im.size[1]/2), Image.ANTIALIAS);
		im.save(directory + card + ".JPG");
