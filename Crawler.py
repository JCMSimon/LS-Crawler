import random
from Screenshot import Screenshot

class LSCrawler:
	def __init__(self):
		self.chars = "abcdefghijklmnopqrstuvwxyz0123456789"

	def genURL(self, codeAmount = 1):
		codes = []
		for _ in range(codeAmount):
			code = ""
			for _ in range(7):
				code += self.chars[random.randint(0,len(self.chars)-1)]
			codes.append(code)
		return codes

	def createScreenshotClass(self, code):
		try:
			return Screenshot(f"https://prnt.sc/{code}")
		except Exception:
			newCode = self.genURL()
			self.createScreenshotClass(newCode)