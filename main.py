import dearpygui.dearpygui as dpg
from io import BytesIO
import win32clipboard
from Crawler import LSCrawler
from PIL import Image
import os
class GUI:
	def __init__(self):
		self.Logic = LSCrawler()
		self.Screenshot = None

		dpg.create_context()
		dpg.create_viewport(title='LS-Crawler', width=648, height=284)
		dpg.setup_dearpygui()
		dpg.show_viewport()
		self.mainWindow()
		self.setWindowAsPrimary()
		self.run()

	def mainWindow(self):
		with dpg.window(tag="Window"):
			# dpg.add_image_button(
			# 	name = "ImageButton",
			# 	value="./assets/placeholder.png",
			# 	height = 100,
			# 	width= 100,
			# 	callback = self.testfnc(),
			# 	texture_tag=0
			# )
			dpg.add_button(label="Next Image",callback=self.nextImg, pos=(324,25), width=300, height=40)
			dpg.add_button(label="Copy Image",callback=self.copyImg, pos=(324,77), width=300, height=40)
			dpg.add_button(label="Open Image URL",callback=self.openUrl, pos=(324,129), width=300, height=40)
			dpg.add_button(label="Copy Image URL",callback=self.copyUrl, pos=(324,181), width=300, height=40)

	def setWindowAsPrimary(self):
		dpg.set_primary_window("Window", True)

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

	def run(self):
		dpg.start_dearpygui()
		dpg.destroy_context()

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

