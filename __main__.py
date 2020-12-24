import os, eel, glob, base64, json, shutil, time
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
import ai, docx
from fpdf import FPDF

os.chdir(os.path.dirname(os.path.realpath(__file__)))
eel.init("web")

historyDirectory = "history"
toConvertDirectory = "toConvert"
settingsFile = "settings.json"
saveLocationFile = "saveLocation.txt"
defaultFileExtension = "txt"
supportedFileTypes = (("Text files", "*.txt"), ("Microsoft Word documents", "*.docx"), ("Portable Document Format (PDF)", "*.pdf"), ("All files", "*.*"))

settings = {}
defaultSettings = {
	"pdf": {
		"fontName": "Arial",
		"fontSize": 15,
		"lineHeight": 20,
		"lineWidth": (595 - (72 / 2.5 * 2))
	}
}

def readSettings():
	global settings
	try:
		with open(settingsFile, "r") as f:
			settings = json.load(f)
	except:
		pass

def writeSettings():
	global settings
	with open(settingsFile, "w") as f:
		json.dump(settings, f)

def escapeFilename(name):
	return "_".join(name.rsplit(".", 1))

def unescapeFilename(name):
	return ".".join(name.rsplit("_", 1))

def convertImgFileToBase64(filename):
	with open(filename, "rb") as f:
		return f"data:image/{filename.split('_')[1].split('.')[0]};base64,{bytes.decode(base64.b64encode(f.read()))}"

def saveFile(filename, contents):
	try:
		ext = filename.rsplit(".", 1)[1]
	except:
		ext = defaultFileExtension
	prefs = settings.get(ext, defaultSettings.get(ext))
	if ext == "docx":
		wordDoc = docx.Document()
		for para in contents.split("\n\n"):
			wordDoc.add_paragraph(para)
		wordDoc.save(filename)
	elif ext == "pdf":
		pdf = FPDF("P", "pt", "A4") # 595pt x 842pt
		pdf.set_font(prefs["fontName"], size=prefs["fontSize"])
		pdf.add_page()
		for para in contents.split("\n\n"):
			pdf.multi_cell(prefs["lineWidth"], prefs["lineHeight"], txt=para)
			pdf.ln()
		pdf.output(filename)
	else:
		with open(filename, "w") as f:
			f.write(contents)

@eel.expose
def updateSettings(newSettings):
	settings.update(newSettings)
	writeSettings()

@eel.expose
def pickSaveLocation():
	root = Tk()
	root.withdraw()
	root.update()
	loc = asksaveasfilename(title = "Choose save location", filetypes = supportedFileTypes)
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
		saveFile(docSaveName, text)
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
	for folder in os.listdir(historyDirectory):
		shutil.rmtree(os.path.join(historyDirectory, folder))

open(settingsFile, "a").close()
os.makedirs(historyDirectory, exist_ok=True)
readSettings()
eel.start("index.html", size=(800, 600))
