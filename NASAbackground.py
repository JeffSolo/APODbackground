import ctypes, urllib, os, sys
import datetime as dt
from bs4 import BeautifulSoup
from PIL import Image


user32 = ctypes.windll.user32 # see SIZE variable

# what resolution to set picture to
SIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# path to save images in
PATH = os.path.dirname(os.path.abspath(__file__)) + '\\apod\\'
# image path and name
SAVEIMAGE = PATH + str(dt.date.today()) + '.jpg'
# url to extract image from
URL = "http://apod.nasa.gov/"
# whether to log errors or not
LOG = True 
# log path and name
LOGFILE = os.path.dirname(os.path.abspath(__file__)) + '\\logfile.txt'

SPI_SETDESKWALLPAPER = 20; #don't change

#creates folder to save images in if doesn't exist
def createFolder(folderPath):
	if not os.path.exists(folderPath):
		os.makedirs(folderPath)	

def setWallpaper(image):
	try:
		ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image, 0)
	except:
		Error("Error setting wallpaper", LOG)
	else: 
		writeToFile(LOGFILE, "No errors encountered. New wallpaper set")
	
def downloadImage(url, imagePath):
	# attempt to establish connection to URL
	try: 
		html = urllib.urlopen(url)
	except:
		# maybe eventually write to log or other means instead
		Error("Error connecting to \"" + url + "\". Please check URL", LOG)
		
	# read html of URL	
	soup = BeautifulSoup(html.read(), "html.parser")
	try:
		#grabs first <img> tag picture source
		imagelink = url + soup.img['src']
	except: 
		Error("Error: No images found", LOG)
	html.close()
	#save image
	urllib.urlretrieve(imagelink, imagePath)
	urllib.urlcleanup()
	
def resizeImage(image, newSize):
	try:
		img = Image.open(image)
		img = img.resize((newSize))
		img.save(image)
	except:
		Error("Error resizing picture", LOG)
	
def writeToFile(file, message):
	f = open(file, 'a+')
	f.write(str(dt.datetime.now()) + '\n' + message + '\n\n'+ '-'*65 + '\n')
	f.close()
	
def Error(message, log):
	print message
	if log:
		writeToFile(LOGFILE, message)
	sys.exit(-1)
	
if __name__ == '__main__':
	createFolder(PATH)
	downloadImage(URL, SAVEIMAGE)
	resizeImage(SAVEIMAGE, SIZE)
	setWallpaper(SAVEIMAGE)
