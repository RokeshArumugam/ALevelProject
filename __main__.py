import os, eel, glob, base64, ai
import tkinter, tkinter.filedialog

os.chdir(os.path.dirname(os.path.realpath(__file__)))
eel.init("web")

historyDirectory = "history"
toConvertDirectory = "toConvert"

@eel.expose
def pickSaveLocation():
	root = tkinter.Tk()
	loc = tkinter.filedialog.asksaveasfilename(title = "Choose save location")
	#print(tkinter.tkFileDialog.askopenfilename(initialdir = curr_directory,title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*"))))
	root.destroy()
	return loc

@eel.expose
def inputDocuments(docs):
	for path in glob.glob(os.path.join(toConvertDirectory, "doc*")):
		os.remove(path)
	docCounter = 0
	for docName, docFiles in docs:
		docCounter += 1
		fileCounter = 0
		os.makedirs(os.path.join(toConvertDirectory, docName))
		for fileExt, fileContent in docFiles:
			fileCounter += 1
			with open(os.path.join(toConvertDirectory, docName, f"img_{fileCounter}.{fileExt}"), "wb") as fw:
				fw.write(base64.b64decode(fileContent.split("base64,")[1]))

@eel.expose
def convertDocuments():
	for docName in os.listdir(toConvertDirectory):
		text = ""
		for docFile in sorted(os.listdir(os.path.join(toConvertDirectory, docName))):
			text += ai.readText(os.path.join(toConvertDirectory, docName, docFile))
		with open(os.path.join(toConvertDirectory, docName, "out.txt"), "w") as f:
			f.write(text)
		# TODO copy doc from toConvert directory to history directory

eel.start("index.html", size=(800, 600))
