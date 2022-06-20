import os
import shutil
from bs4 import BeautifulSoup
import dearpygui.dearpygui as dpg
import random

import urllib.request
import requests


class LSCrawler:
	def __init__(self):
		self.expectedImageAmount = 3
		self.realImageIndex = 0
		self.chars = "abcdefghijklmnopqrstuvwxyz0123456789"
		dpg.create_context()
		dpg.create_viewport(title='LS-Crawler', width=562, height=250)
		dpg.setup_dearpygui()
		dpg.show_viewport()
		self.setup()
		self.initMainWindow()
		self.setWindowAsPrimary()
		self.run()

	def initMainWindow(self):
		with dpg.texture_registry():
			width, height, _, data = dpg.load_image("./assets/placeholder.png")
			texture_id = dpg.add_dynamic_texture(width, height, data, tag="ImagePreview")
		with dpg.window(tag="Window"):
			#Image Button
			dpg.add_image_button(texture_tag=texture_id,width=200,height=175,pos=(12,12))
			#Next Image Button
			dpg.add_button(label="Next Image",callback=self.nextImage, pos=(232,14), width=300, height=50)
			#Copy Image Button
			dpg.add_button(label="Copy Image",callback=self.placeholder, pos=(232,76), width=300, height=50)
			#Copy Image URL Button
			dpg.add_button(label="Copy Image URL",callback=self.placeholder, pos=(232,138), width=300, height=51)

	def setWindowAsPrimary(self):
		dpg.set_primary_window("Window", True)

	def run(self):
		dpg.start_dearpygui()
		dpg.destroy_context()

####################################################
#     Functions below are for the actual work      #
####################################################

	def nextImage(self):
		code = self.genURLCode()
		pathToImage = self.downloadImage(code)
		print(pathToImage)

####################################################
#      Functions below are helper functions        #
####################################################

	def downloadImage(self, code):
		webpage = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(f"https://prnt.sc/{code}",headers={'User-Agent': 'Mozilla/5.0'})).read().decode('ISO-8859-1'), 'html.parser')
		imageURLs = webpage.find_all('img')
		if len(imageURLs) != self.expectedImageAmount:
			self.nextImage()
			return
		else:
			addon= ""
			if not os.path.isfile(os.path.expandvars(f"%appdata%/LSCrawler/Screenshots/{code}.png")):
				if not str(imageURLs[self.realImageIndex]['src']).startswith("http"):
					addon = "https:"
				with requests.get(addon + str(imageURLs[self.realImageIndex]['src']),headers={'User-Agent': 'Mozilla/5.0'}, stream=True) as url:
					with open(str(os.path.expandvars(f"%appdata%/LSCrawler/Screenshots/{code}.png")), "wb") as file:
						shutil.copyfileobj(url.raw, file)
			print(imageURLs[self.realImageIndex]['src'])
			return os.path.expandvars(f"%appdata%/LSCrawler/Screenshots/{code}.png")

		# def downloadImage(self,filename = "idk", path = "./Screenshots/"):
		# if not os.path.isfile(f"{path}{filename}.png"):
		# 	try:
		# 		#* Using a User Agent to not be *sus*
		# 		with requests.get(self.imageURL,headers={'User-Agent': 'Mozilla/5.0'}, stream=True) as url:
		# 			with open(path + filename + ".png", "wb") as file:
		# 				shutil.copyfileobj(url.raw, file)
		# 		self.path = path + filename
		# 	except MissingSchema:
		# 		print("shit")
		# 	except FileNotFoundError:
		# 		os.makedirs(path)
		# 		self.downloadImage(filename = filename)


	def setup(self):
		if not os.path.exists(os.path.expandvars("%appdata%/LSCrawler/Screenshots")):
			os.makedirs(os.path.expandvars("%appdata%/LSCrawler/Screenshots"))

	def placeholder(self):
		pass

	def genURLCode(self):
		code = ""
		for _ in range(7):
			code += self.chars[random.randint(0,len(self.chars)-1)]
		return code



if __name__ == "__main__":
	thing = LSCrawler()