from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup
from PIL import Image
import urllib.request
import requests
import shutil
import time
import os

class Screenshot:
	def __init__(self, URL):
		#Settings for future easy updates
		self.expectedImageAmount = 3
		self.realImageIndex = 0 #counting from 0
		#Settings over
		self.URL = URL
		page = BeautifulSoup(self.getPage(), 'html.parser')
		self.imageURL = self.getImage(page)
		timestamp = time.strftime("%H%M%S%Y")
		self.downloadImage(filename = str(timestamp))

	def getPage(self):
		return urllib.request.urlopen(urllib.request.Request(self.URL,headers={'User-Agent': 'Mozilla/5.0'})).read().decode('ISO-8859-1')

	def getImage(self,page):
		imageURLs = page.find_all('img')
		if len(imageURLs) != self.expectedImageAmount:
			print(imageURLs)
			raise ValueError(f"[INFO] {self.URL} is invalid.")
		else:
			return imageURLs[self.realImageIndex]['src']

	def downloadImage(self,filename = "idk", path = "./Screenshots/"):
		if not os.path.isfile(f"{path}{filename}.png"):
			try:
				#* Using a User Agent to not be *sus*
				with requests.get(self.imageURL,headers={'User-Agent': 'Mozilla/5.0'}, stream=True) as url:
					with open(path + filename + ".png", "wb") as file:
						shutil.copyfileobj(url.raw, file)
				self.path = path + filename
			except MissingSchema:
				print("yo fuck up")
				raise ValueError(f"[INFO] {self.URL} is invalid.")
			except FileNotFoundError:
				os.makedirs(path)
				self.downloadImage(filename = filename)

	def destroy(self):
		del self

if __name__ == '__main__':
	#* Works
	screenshot = Screenshot("https://prnt.sc/av3ghr")
