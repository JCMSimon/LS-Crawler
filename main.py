from io import BytesIO
import win32clipboard
from Crawler import LSCrawler
from PIL import Image
import os
class GUI:
	def __init__(self):
		self.Logic = LSCrawler()
		self.Screenshot = None


	def addImage(self, image):
		width, height, _, data = dpg.load_image(str(image))

		with dpg.texture_registry():
			test = dpg.add_dynamic_texture(width, height, data)
			return test

	def nextImg(self):
		if self.Screenshot != None:
			self.Screenshot.destroy()
		self.Screenshot = self.Logic.createScreenshotClass(self.Logic.genURL())
		print(f"Next image: {self.Screenshot.prntURL}")

	def copyImg(self):
		path = self.Screenshot.path
		image = Image.open(path)
		send_to_clipboard(image)
		print("Copy image")

	def openUrl(self):
		os.system(f"start {self.Screenshot.imageURL} && exit")
		print(f"Open image url: {self.screenshotURL}")

	def copyUrl(self):
		# copy self.screenshotURL to clipboard
		os.system(f"echo {self.Screenshot.imageURL} | clip")
		print(f"Copy image url: {self.screenshotURL}")
		tes = self.addImage("./assets/placeholder.png")
		print(tes)


def send_to_clipboard(image):
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

gui = GUI()

