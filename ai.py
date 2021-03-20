import base64, re

import cv2, easyocr
import numpy as np

def readText(imgData):
	return formatText(
		" ".join(
			easyocr.Reader(
				['en'],
				gpu=False,
				model_storage_directory="./model",
				user_network_directory=False
			).readtext(
				cv2.imdecode(
					np.fromstring(base64.b64decode(imgData), np.uint8),
					cv2.IMREAD_COLOR
				),
				detail=0
			)
		)
	)

def formatText(text):
	# text = text[:-1]
	# text = re.sub(r"([^.!?\n])\n([^\n])", r"\1 \2", text)
	return text
