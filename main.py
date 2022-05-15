import dearpygui.dearpygui as dpg

class GUI:
	def __init__(self):
		dpg.create_context()
		dpg.create_viewport(title='LS-Crawler', width=648, height=284)
		dpg.setup_dearpygui()
		dpg.show_viewport()
		self.mainWindow()
		self.setWindowAsPrimary()
		self.run()

	def mainWindow(self):

		#TODO add registry shits
		#TODO add sample image to it from assets
		#TODO add button with said image on the left side
		#TODO resize image to button dimensions

		#TODO add text as disclaimer that image can be distorted
		#TODO image button opens image in original size in a popup

		with dpg.window(tag="Window"):
			dpg.add_button(label="Next Image",callback=self.nextImg, pos=(324,25), width=300, height=40)
			dpg.add_button(label="Copy Image",callback=self.copyImg, pos=(324,77), width=300, height=40)
			dpg.add_button(label="Open Image URL",callback=self.openUrl, pos=(324,129), width=300, height=40)
			dpg.add_button(label="Copy Image URL",callback=self.copyUrl, pos=(324,181), width=300, height=40)

	def setWindowAsPrimary(self):
		dpg.set_primary_window("Window", True)

	def nextImg(self):
		print("Next image")

	def copyImg(self):
		print("Copy image")

	def openUrl(self):
		print("Open image url")

	def copyUrl(self):
		print("Copy image url")

	def run(self):
		dpg.start_dearpygui()
		dpg.destroy_context()


gui = GUI()

