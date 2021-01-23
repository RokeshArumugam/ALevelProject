import base64, re

import cv2, pytesseract
import numpy as np

def readText(imgData):
	# Uncomment the line below to provide path to tesseract manually
	# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
	
	# Read image from base64 string
	nparr = np.fromstring(base64.b64decode(imgData), np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	
	# Run tesseract OCR on image
	# '-l eng'	  for using the English language
	# '--oem 1' for using LSTM OCR Engine
	return formatText(pytesseract.image_to_string(img, config=('-l eng --oem 1 --psm 3')))

def formatText(text):
	text = re.sub(r"([^.!?\n])\n([^\n])", r"\1 \2", text[:-1])
	return text
