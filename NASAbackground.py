import ctypes
import urllib
import os
import sys
import datetime as dt
from bs4 import BeautifulSoup
from PIL import Image

#SIZE = 1366, 768
user32 = ctypes.windll.user32

SIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
SPI_SETDESKWALLPAPER = 20;
NASAURL = "http://apod.nasa.gov/"

# path to save images in, change to whatever you want
PATH = os.path.dirname(os.path.abspath(__file__)) + '\\apod\\'
#saved image location and name
SAVEIMAGE = PATH + str(dt.date.today()) + '.jpg'

#creates folder to save images in if doesn't exist
def createFolder():
	if not os.path.exists(PATH):
		os.makedirs(PATH)	

def setWallpaper(image):
	ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image, 0)
	
def downloadNASAimage(url):
	# attempt to establish connection to URL
	try: 
		html = urllib.urlopen(url)
	except:
		# maybe eventually write to log or other means instead
		print "Error connecting to " + url + " . Please check URL"
		sys.exit(-1)
		
	# read html of URL	
	soup = BeautifulSoup(html.read(), "html.parser")

	imagelink = NASAURL + soup.img['src']
	html.close()
	urllib.urlretrieve(imagelink, SAVEIMAGE)
	
def resizeImage():
	img = Image.open(SAVEIMAGE)
	img = img.resize((SIZE))
	img.save(SAVEIMAGE)
	
if __name__ == '__main__':
	createFolder()
	image = downloadNASAimage(NASAURL)
	resizeImage()
	setWallpaper(SAVEIMAGE)
