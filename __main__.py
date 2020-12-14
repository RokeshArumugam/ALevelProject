import os, eel, glob, base64, shutil, time, ai
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

os.chdir(os.path.dirname(os.path.realpath(__file__)))
eel.init("web")

historyDirectory = "history"
toConvertDirectory = "toConvert"
saveLocationFile = "saveLocation.txt"

def escapeFilename(name):
	return "_".join(name.rsplit(".", 1))

def unescapeFilename(name):
	return ".".join(name.rsplit("_", 1))

def convertImgFileToBase64(filename):
	with open(filename, "rb") as f:
		return f"data:image/{filename.split('_')[1].split('.')[0]};base64,{bytes.decode(base64.b64encode(f.read()))}"

@eel.expose
def pickSaveLocation():
	root = Tk()
	root.withdraw()
	root.update()
	loc = asksaveasfilename(title = "Choose save location", filetypes = (("Text files", "*.txt"),("All files", "*.*")))
	root.update()
	root.destroy()
	return loc, os.path.basename(loc)

@eel.expose
def inputDocuments(docs):
	try:
		shutil.rmtree(toConvertDirectory)
	except:
		pass
	os.mkdir(toConvertDirectory)
	
	for docLoc, docFiles in docs:
		docPath = os.path.join(toConvertDirectory, escapeFilename(os.path.basename(docLoc)))
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
	for docsCompleted, docDirName in enumerate(docs):
		docSaveName = unescapeFilename(docDirName)
		eel.setDocProgressMsg("")
		eel.setOverallProgressMsg(f"Converting {docSaveName}...")

		os.chdir(docDirName)
		docFiles = sorted(os.listdir("."))
		docFiles.remove(saveLocationFile)

		text = ""
		eel.setConvertedText(text)
		eel.setDocProgressBarCompleted(0)
		eel.setDocProgressBarTotal(len(docFiles))
		for docFilesCompleted, docFile in enumerate(docFiles):
			eel.setInputImg(convertImgFileToBase64(docFile))
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
		shutil.move(docDirName, os.path.join("..", historyDirectory, f"{time.time()} {docDirName}"))
	os.chdir("..")
	os.rmdir(toConvertDirectory)
	eel.finishedConverting()

@eel.expose
def readHistory():
	os.makedirs(historyDirectory, exist_ok=True)
	entries = []
	os.chdir(historyDirectory)
	for docDirName in sorted(os.listdir("."), reverse=True):
		entry = []
		docTime, docSaveName = docDirName.split(" ", 1)
		docSaveName = unescapeFilename(docSaveName)
		entry.append([docSaveName, datetime.fromtimestamp(float(docTime)).strftime("%d %b %Y %H:%M:%S")])
		
		os.chdir(docDirName)
		docFiles = sorted(os.listdir("."))
		docFiles.remove(saveLocationFile)
		docFiles.remove(docSaveName)
		entry.append([convertImgFileToBase64(docFile) for docFile in docFiles])
		entries.append(entry)
		os.chdir("..")
	os.chdir("..")
	return entries

@eel.expose
def clearHistory():
	try:
		shutil.rmtree(historyDirectory)
	except:
		pass

eel.start("index.html", size=(800, 600))
