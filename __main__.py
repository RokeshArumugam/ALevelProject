import os, eel, glob, base64, shutil, ai
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

os.chdir(os.path.dirname(os.path.realpath(__file__)))
eel.init("web")

historyDirectory = "history"
toConvertDirectory = "toConvert"
saveLocationFile = "saveLocation.txt"

try:
	shutil.rmtree(docPath)
except:
	pass
os.mkdir(toConvertDirectory)

@eel.expose
def pickSaveLocation():
	Tk().withdraw()
	loc = asksaveasfilename(title = "Choose save location", filetypes = (("text files", "*.txt")))
	#print(tkinter.tkFileDialog.askopenfilename(initialdir = curr_directory,title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*"))))
	return loc, os.path.basename(loc)

@eel.expose
def inputDocuments(docs):
	for docLoc, docFiles in docs:
		docPath = os.path.join(toConvertDirectory, "_".join(os.path.basename(docLoc).rsplit(".", 1)))
		os.mkdir(docPath)
		os.chdir(docPath)
		with open(saveLocationFile, "w") as f:
			f.write(docLoc)
		numDigits = len(str(len(docFiles)))
		fileCounter = 0
		for fileExt, fileContent in docFiles:
			fileCounter += 1
			with open(f"img_{str(fileCounter).zfill(numDigits)}.{fileExt}", "wb") as f:
				f.write(base64.b64decode(fileContent.split("base64,")[1]))
		os.chdir(os.path.join("..", ".."))

@eel.expose
def convertDocuments():
	os.chdir(toConvertDirectory)
	for docName in os.listdir("."):
		os.chdir(docName)
		text = ""
		docFiles = sorted(os.listdir("."))
		docFiles.remove(saveLocationFile)
		for docFile in docFiles:
			text += ai.readText(docFile)
		with open(".".join(docName.rsplit("_", 1)), "w") as f:
			f.write(text)
		os.chdir("..")
		# TODO move doc from toConvert directory to history directory
	os.chdir("..")

eel.start("index.html", size=(800, 600))
