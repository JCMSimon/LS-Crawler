import os
import shutil
import time
from bs4 import BeautifulSoup
import dearpygui.dearpygui as dpg
import random
from PIL import Image

import urllib.request
import requests

class LSCrawler:
	def __init__(self):
		debugPrint("Starting...")
		self.chars = "abcdefghijklmnopqrstuvwxyz0123456789"
		self.folderSetup()
		debugPrint("Startup complete.")

####################################################
#         Functions below are for the gui          #
####################################################

		#GUI
		dpg.create_context()
		dpg.create_viewport(title='LS-Crawler', width=562, height=250, resizable=False)
		dpg.setup_dearpygui()
		dpg.show_viewport()
		self.initMainWindow()
		self.setWindowAsPrimary()
		self.run()

	def initMainWindow(self):
		with dpg.texture_registry():
			width, height, _, data = dpg.load_image("./assets/placeholder.png")
			self.texture_id = dpg.add_dynamic_texture(width, height, data, tag="ImagePreview")
		with dpg.window(tag="Window"):
			#Image Button
			dpg.add_image_button(texture_tag=self.texture_id,width=200,height=175,pos=(12,12))
			#Next Image Button
			dpg.add_button(label="Next Image",callback=self.nextImage, pos=(232,14), width=300, height=50)
			#Copy Image Button
			dpg.add_button(label="Copy Image",callback=self.copyImage, pos=(232,76), width=300, height=50)
			#Copy Image URL Button
			dpg.add_button(label="Copy Image URL",callback=self.copyImageURL, pos=(232,138), width=300, height=51)

	def setWindowAsPrimary(self):
		dpg.set_primary_window("Window", True)

	def run(self):
		dpg.start_dearpygui()
		dpg.destroy_context()

####################################################
#     Functions below are for the buttons          #
####################################################

	def nextImage(self):
		self.setImageToPreview("./assets/download.png") #placeholder for a loading thingy
		self.ImageData = self.downloadImage(self.genURLCode())
		if not self.ImageData:
			debugPrint("Failed to download image. Trying again.")
			self.nextImage()
		else:
			image = Image.open(os.path.expandvars(self.ImageData["ImagePath"]))
			image.resize((259,194), Image.ANTIALIAS).save(os.path.expandvars(str(self.ImageData["ImagePath"]).replace("/Screenshots","/Screenshots/preview")))
			self.setImageToPreview(os.path.expandvars(self.ImageData["ImagePath"]).replace("/Screenshots","/Screenshots/preview"))

	def copyImage(self):
		try:
			path = os.path.expandvars(self.ImageData["ImagePath"])
		except KeyError:
			os.system("echo " + "I tried to copy a Image before i generated a Image. Man i am dumb lol" + " | clip")


	def copyImageURL(self):
		try:
			os.system("echo " + self.ImageData["ImageURL"] + " | clip")
		except KeyError:
			os.system("echo " + "I tried to copy a Image Url before i generated a Image. Man i am dumb lol" + " | clip")

	def setImageToPreview(self, path):
		with dpg.texture_registry():
			_, _, _, data = dpg.load_image(f"{path}")
			dpg.set_value(item = self.texture_id, value = data)
			debugPrint("Updated Image Preview")

####################################################
#      Functions below do the actual work          #
####################################################

	def downloadImage(self, code):
		debugPrint("#####Start of Download Thread#####")
		debugPrint(f"Trying to download image from https://prnt.sc/{code}")
		try:
			webpage = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(f"https://prnt.sc/{code}",headers={'User-Agent': 'Mozilla/5.0'}),timeout=20).read().decode('ISO-8859-1'), 'html.parser')
		except:
			debugPrint("Timeout reached. (20 Sec)")
			debugPrint("######End of Download Thread######")
			return False
		imageURLs = webpage.find_all('img')
		debugPrint(f"Found {len(imageURLs)} images.")
		for imageURL in imageURLs:
			debugPrint(f"{imageURL['src']}")
		debugPrint(f"Choosing {imageURLs[0]['src']}")
		if not str(imageURLs[0]['src']).startswith("https://"):
			debugPrint("Invalid image URL.")
			debugPrint("######End of Download Thread######")
			return False
		if not os.path.isfile(os.path.expandvars(f"%appdata%/LSCrawler/Screenshots/{code}.png")):
			with requests.get(str(imageURLs[0]['src']),headers={'User-Agent': 'Mozilla/5.0'}, stream=True) as url:
				#test if the request returned a 404 response
				if url.status_code == 404:
					debugPrint("Image not found.")
					return False
				with open(str(os.path.expandvars(f"%appdata%/LSCrawler/Screenshots/{code}.png")), "wb") as file:
					shutil.copyfileobj(url.raw, file)
		else:
			debugPrint(f"Image already exists.")
			debugPrint("######End of Download Thread######")
			return False
		debugPrint("######End of Download Thread######")
		results = {"ImagePath":f"%appdata%/LSCrawler/Screenshots/{code}.png","ImageURL":f"https://prnt.sc/{code}"}
		return results

	def folderSetup(self):
		if not os.path.exists(os.path.expandvars("%appdata%/LSCrawler/Screenshots")):
			os.makedirs(os.path.expandvars("%appdata%/LSCrawler/Screenshots"))
		if not os.path.exists(os.path.expandvars("%appdata%/LSCrawler/Screenshots/preview")):
			os.makedirs(os.path.expandvars("%appdata%/LSCrawler/Screenshots/preview"))

	def placeholder(self):
		pass

	def genURLCode(self):
		code = ""
		for _ in range(7):
			code += self.chars[random.randint(0,len(self.chars)-1)]
		return code

####################################################
#     Functions below are helper functions         #
####################################################

debug = True
def debugPrint(message):
	if debug:
		print(f"[LS]> {message}")


if __name__ == "__main__":
	thing = LSCrawler()
