import cv2, pytesseract, re

def readText(imgPath):
	# Uncomment the line below to provide path to tesseract manually
	# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
	
	# Read image from disk
	im = cv2.imread(imgPath, cv2.IMREAD_COLOR)
	
	# Run tesseract OCR on image
	# '-l eng'	  for using the English language
	# '--oem 1' for using LSTM OCR Engine
	return formatText(pytesseract.image_to_string(im, config=('-l eng --oem 1 --psm 3'))[:-1])

def formatText(text):
	text = re.sub(r"([^.!?\n])\n([^\n])", r"\1 \2", text)
	return text
