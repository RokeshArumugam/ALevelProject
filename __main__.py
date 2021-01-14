import os, eel, glob, base64, json, copy, time, contextlib
import sqlite3 as sl
from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
import ai, docx
from fpdf import FPDF

os.chdir(os.path.dirname(os.path.realpath(__file__)))
eel.init("web")

databaseFile = "data.db"
settingsFile = "settings.json"
defaultFileExtension = "txt"
supportedFileTypes = (("Text files", "*.txt"), ("Microsoft Word documents", "*.docx"), ("Portable Document Format (PDF)", "*.pdf"), ("All files", "*.*"))

fullSettings = {}
userSettings = {}
defaultSettings = {
	"__extToType": {
		"DOCX": "Microsoft Word Document",
		"PDF": "PDF"
	},
	"__constraints": {
		"fontSizeMin": 1,
		"fontSizeMax": 40,
		"lineHeightMin": 5,
		"lineHeightMax": 40
	},
	"document": {
		"PDF": {
			"fontName": "Arial",
			"fontSize": 15,
			"lineHeight": 20,
			"__fontNameAllowed": ["Arial", "Courier", "Helvetica", "Times", "Symbol", "ZapfDingbats"],
			"__lineWidth": (595 - (72 / 2.5 * 2))
		}
	}
}

def initDatabase():
	with contextlib.closing(sl.connect(databaseFile)) as con:
		with con:
			with contextlib.closing(con.cursor()) as cur:
				cur.execute("""
					CREATE TABLE IF NOT EXISTS document (
						id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
						save_location TEXT,
						creation_time REAL
					)
				""")
				cur.execute("""
					CREATE TABLE IF NOT EXISTS image (
						id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
						document_id INTEGER NOT NULL,
						position INTEGER,
						data TEXT,
						filetype TEXT,
						FOREIGN KEY(document_id) REFERENCES document(id)
					)
				""")
				cur.execute("DELETE FROM document WHERE creation_time IS Null")

def constructDataURI(data, filetype):
	return f"data:image/{filetype};base64,{data}"

def saveFile(filepath, contents):
	try:
		ext = os.path.basename(filepath).rsplit(".", 1)[1]
	except:
		ext = defaultFileExtension
	ext = ext.upper()
	prefs = fullSettings["document"].get(defaultSettings["__extToType"].get(ext), {})
	if ext == "DOCX":
		wordDoc = docx.Document()
		for para in contents.split("\n\n"):
			wordDoc.add_paragraph(para)
		wordDoc.save(filepath)
	elif ext == "PDF":
		pdf = FPDF("P", "pt", "A4") # 595pt x 842pt
		pdf.set_font(prefs["fontName"], size=prefs["fontSize"])
		pdf.add_page()
		for para in contents.encode('latin-1', 'replace').decode('latin-1').split("\n\n"):
			pdf.multi_cell(prefs["__lineWidth"], prefs["lineHeight"], txt=para)
			pdf.ln()
		pdf.output(filepath)
	else:
		with open(filepath, "w") as f:
			f.write(contents)

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
	for saveLoc, imgs in docs:
		with contextlib.closing(sl.connect(databaseFile)) as con:
			with con:
				with contextlib.closing(con.cursor()) as cur:
					cur.execute("INSERT INTO document (save_location) VALUES (?)", (saveLoc,))
					docId = cur.lastrowid
					cur.executemany("INSERT INTO image (document_id, position, data, filetype) VALUES (?, ?, ?, ?)", [(docId, pos, imgData.split("base64,")[1], imgData.split('/')[1].split(';')[0]) for pos, imgData in enumerate(imgs)])

@eel.expose
def convertDocuments():
	with contextlib.closing(sl.connect(databaseFile)) as con:
		with contextlib.closing(con.cursor()) as cur:
			docs = cur.execute("SELECT id, save_location FROM document WHERE creation_time IS NULL").fetchall()
		
		eel.setOverallProgressBarTotal(len(docs))
		for docsCompleted, (docId, saveLoc) in enumerate(docs):
			docName = os.path.basename(saveLoc)
			eel.setDocProgressMsg("")
			eel.setOverallProgressMsg(f"Converting {docName}...")
			
			with contextlib.closing(con.cursor()) as cur:
				imgs = cur.execute(f"SELECT data, filetype FROM image WHERE document_id={docId} ORDER BY position").fetchall()
			
			text = ""
			eel.setConvertedText(text)
			eel.setDocProgressBarCompleted(0)
			eel.setDocProgressBarTotal(len(imgs))
			
			for imgsCompleted, (imgData, imgFiletype) in enumerate(imgs):
				eel.setInputImg(constructDataURI(imgData, imgFiletype))
				text += ai.readText(imgData)
				eel.setConvertedText(text)
				eel.setDocProgressBarCompleted(imgsCompleted + 1)
			
			eel.setDocProgressMsg("Saving document...")
			saveFile(saveLoc, text)
			eel.setDocProgressMsg("Saved document!")
			
			eel.setOverallProgressBarCompleted(docsCompleted + 1)
			eel.setOverallProgressMsg(f"Converted {docName}")
			with con:
				with contextlib.closing(con.cursor()) as cur:
					cur.execute(f"UPDATE document SET creation_time={time.time()} WHERE id={docId}")
	eel.finishedConverting()

@eel.expose
def readHistory():
	entries = []
	with contextlib.closing(sl.connect(databaseFile)) as con:
		with contextlib.closing(con.cursor()) as cur:
			docs = cur.execute("SELECT id, save_location, creation_time FROM document ORDER BY creation_time DESC").fetchall()
		for docId, saveLoc, docTime in docs:
			entry = []
			entry.append([os.path.basename(saveLoc), datetime.fromtimestamp(float(docTime)).strftime("%d %b %Y %H:%M:%S")])
			
			with contextlib.closing(con.cursor()) as cur:
				entry.append([constructDataURI(data, filetype) for data, filetype in cur.execute(f"SELECT data, filetype FROM image WHERE document_id={docId} ORDER BY position").fetchall()])
			entries.append(entry)
	return entries

@eel.expose
def clearHistory():
	with contextlib.closing(sl.connect(databaseFile)) as con:
		with con:
			with contextlib.closing(con.cursor()) as cur:
				cur.execute("DELETE FROM document")
				cur.execute("DELETE FROM image")

def readSettings():
	global fullSettings, userSettings
	with open(settingsFile, "a+") as f:
		f.seek(0)
		contents = f.read()
		userSettings = json.loads(contents if contents else "{}")
	fullSettings = copy.deepcopy(defaultSettings)
	updateDict(userSettings, fullSettings)
	return fullSettings

@eel.expose
def getSettings():
	return fullSettings

@eel.expose
def writeSettings():
	with open(settingsFile, "w") as f:
		json.dump(userSettings, f)

def updateDict(newDict, storedDict):
	for key, val in newDict.items():
		if (key not in storedDict) or not isinstance(val, dict):
			storedDict.update({key: val})
		else:
			updateDict(val, storedDict[key])

@eel.expose
def updateSettings(newSettings):
	global fullSettings, userSettings
	updateDict(newSettings, fullSettings)
	updateDict(newSettings, userSettings)
	writeSettings()

@eel.expose
def resetSettings():
	open(settingsFile, "w").close()
	readSettings()

initDatabase()
readSettings()
eel.start("index.html", size=(1024, 640))
