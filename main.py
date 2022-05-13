import random
from image import Screenshot
class LSCrawler:
	def __init__(self):
		self.chars = "abcdefghijklmnopqrstuvwxyz0123456789"

	def genURL(self, codeAmount):
		codes = []
		for _ in range(codeAmount):
			code = ""
			for _ in range(7):
				code += self.chars[random.randint(0,len(self.chars)-1)]
			codes.append(code)
		return codes

	def createScreenshotClass(code):
		return Screenshot(f"https://prnt.sc/{code}")

