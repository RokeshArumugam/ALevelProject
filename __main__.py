import os, eel, glob, base64, shutil, ai
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

os.chdir(os.path.dirname(os.path.realpath(__file__)))
eel.init("web")

historyDirectory = "history"
toConvertDirectory = "toConvert"
saveLocationFile = "saveLocation.txt"

@eel.expose
def pickSaveLocation():
	Tk().withdraw()
	loc = asksaveasfilename(title = "Choose save location", filetypes = (("Text files", "*.txt"),("All files", "*.*")))
	#print(tkinter.tkFileDialog.askopenfilename(initialdir = curr_directory,title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*"))))
	return loc, os.path.basename(loc)

@eel.expose
def inputDocuments(docs):
	try:
		shutil.rmtree(toConvertDirectory)
	except:
		pass
	os.mkdir(toConvertDirectory)
	
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
			with open(f"{str(fileCounter).zfill(numDigits)}_{fileContent.split('/')[1].split(';')[0]}.{fileExt}", "wb") as f:
				f.write(base64.b64decode(fileContent.split("base64,")[1]))
		os.chdir(os.path.join("..", ".."))

@eel.expose
def convertDocuments():
	os.chdir(toConvertDirectory)
	docs = os.listdir(".")
	eel.setOverallProgressBarTotal(len(docs))
	for docsCompleted, docName in enumerate(docs):
		docSaveName = ".".join(docName.rsplit("_", 1))
		eel.setDocProgressMsg("")
		eel.setOverallProgressMsg(f"Converting {docSaveName}...")

		os.chdir(docName)
		docFiles = sorted(os.listdir("."))
		docFiles.remove(saveLocationFile)

		text = ""
		eel.setConvertedText(text)
		eel.setDocProgressBarCompleted(0)
		eel.setDocProgressBarTotal(len(docFiles))
		for docFilesCompleted, docFile in enumerate(docFiles):
			with open(docFile, "rb") as f:
				eel.setInputImg(f"data:image/{docFile.split('_')[1].split('.')[0]};base64,{bytes.decode(base64.b64encode(f.read()))}")

			text += ai.readText(docFile)
			eel.setConvertedText(text)
			eel.setDocProgressBarCompleted(docFilesCompleted + 1)
		eel.setDocProgressMsg("Saving document...")
		with open(docSaveName, "w") as f:
			f.write(text)
		with open(saveLocationFile, "r") as f:
			shutil.copyfile(docSaveName, f.read())
		eel.setDocProgressMsg("Saved document!")
		eel.setOverallProgressBarCompleted(docsCompleted + 1)
		eel.setOverallProgressMsg(f"Converted {docSaveName}")
		os.chdir("..")
		# TODO move doc from toConvert directory to history directory
	os.chdir("..")
	eel.finishedConverting()

eel.start("index.html", size=(800, 600))
