from bs4 import BeautifulSoup
import urllib.request
import requests
import time

class Screenshot:
	def __init__(self, URL):
		#Settings for future easy updates
		self.expectedImageAmount = 3
		self.realImageIndex = 0 #counting from 0
		#Settings over
		self.URL = URL
		self.page = BeautifulSoup(self.getPage(), 'html.parser')
		self.imageURL = self.getImage()
		self.ImageSizeInBytes = self.getImageSize()

	def getPage(self):
		return urllib.request.urlopen(urllib.request.Request(self.URL,headers={'User-Agent': 'Mozilla/5.0'})).read().decode('ISO-8859-1')

	def getImage(self):
		imageURLs = self.page.find_all('img')
		if len(imageURLs) != self.expectedImageAmount:
			raise Exception(f"[INFO] {self.URL} is invalid.")
		else:
			return imageURLs[self.realImageIndex]['src']

	def getImageSize(self):
		# kinda inaccurate for some reason smth smth downloading
		return requests.get(self.imageURL, stream = True).headers['Content-length']

	def downloadImage(self,filename = "InDev.png", path = "./"):
		self.ImagePath = path + filename
		with open(self.ImagePath, 'wb') as f:
			f.write(requests.get(self.imageURL).content)

if __name__ == '__main__':
	screenshot = Screenshot("https://prnt.sc/1vfw3wr")
	print(screenshot.imageURL)
	print(screenshot.ImageSizeInBytes + " bytes")