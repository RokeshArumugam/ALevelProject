import os, eel, glob, base64
import tkinter, tkinter.filedialog

os.chdir(os.path.dirname(os.path.realpath(__file__)))

eel.init("web")

@eel.expose
def pickSaveLocation():
	root = tkinter.Tk()
	print(tkinter.filedialog.asksaveasfilename(title = "Choose save location"))
	#print(tkinter.tkFileDialog.askopenfilename(initialdir = curr_directory,title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*"))))
	root.destroy()

@eel.expose
def inputDocuments(docs):
	for path in glob.glob("doc*"):
		os.remove(path)
	docCounter = 0
	for doc in docs:
		docCounter += 1
		fileCounter = 0
		os.makedirs(f"doc_{docCounter}")
		for fileExt, fileContent in doc:
			fileCounter += 1
			with open(f"doc_{docCounter}{os.path.sep}img_{fileCounter}.{fileExt}", "wb") as fw:
				fw.write(base64.b64decode(fileContent.split("base64,")[1]))

eel.start("index.html", size=(800, 600))

