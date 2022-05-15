from bs4 import BeautifulSoup
from requests.exceptions import MissingSchema
import urllib.request
import requests
import shutil
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
		print(self.imageURL)

	def getPage(self):
		return urllib.request.urlopen(urllib.request.Request(self.URL,headers={'User-Agent': 'LS-Crawlercls'})).read().decode('ISO-8859-1')

	def getImage(self,page):
		imageURLs = page.find_all('img')
		if len(imageURLs) != self.expectedImageAmount:
			raise Exception(f"[INFO] {self.URL} is invalid.")
		else:
			return imageURLs[self.realImageIndex]['src']

	def downloadImage(self,filename = "InDev.png", path = "./Screenshots/"):
		try:
			#* Using a User Agent to not be *sus*
			with requests.get(self.imageURL,headers={'User-Agent': 'LS-Crawler'}, stream=True) as url:
				with open(path + filename, "wb") as file:
					shutil.copyfileobj(url.raw, file)
		except MissingSchema:
			raise Exception(f"[INFO] {self.URL} is invalid.")
		except FileNotFoundError:
			os.makedirs(path)
			self.downloadImage()

if __name__ == '__main__':
	#* Works
	screenshot = Screenshot("https://prnt.sc/1vfidg")
	screenshot.downloadImage()
	#! Fails
	screenshot = Screenshot("https://prnt.sc/1vfh5g")
	screenshot.downloadImage()