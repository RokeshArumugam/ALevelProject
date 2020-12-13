let newDocButton = document.querySelector("#createNewDoc")
let nextButton = document.querySelector("#next")
let fileInput = document.querySelector("#fileInput")
let previewCont = document.querySelector(".previewImageContainer")
let docs = []

previewCont.addEventListener("DOMSubtreeModified", e => {
	if (previewCont.querySelectorAll(":scope > *").length > 0) {
		nextButton.classList.remove("disabled")
	} else {
		nextButton.classList.add("disabled")
	}
	if (previewCont.querySelectorAll(":scope > img").length > 0) {
		newDocButton.classList.remove("disabled")
	} else {
		newDocButton.classList.add("disabled")
	}
})

function inputFile() {
	for (let file of fileInput.files) {
		let freader = new FileReader()
		freader.onload = function() {
			let img = document.createElement("img")
			img.src = this.result
			img.dataset.ext = file.name.split(".").pop()
			previewCont.appendChild(img)
		}
		freader.readAsDataURL(file)
	}
}
function createNewDoc() {
	let imgs = previewCont.querySelectorAll(":scope > img")
	let divDoc = document.createElement("div")
	divDoc.classList.add("doc")
	let closeButton = document.createElement("div")
	closeButton.classList.add("closeButton")
	closeButton.addEventListener("click", e => {
		let div = e.target.parentElement
		div.parentElement.removeChild(div)
	})
	divDoc.appendChild(closeButton)
	
	let divDocImgCont = document.createElement("div")
	divDocImgCont.classList.add("docImgCont")
	imgs.forEach((img) => {
		divDocImgCont.appendChild(img)
	})
	divDoc.appendChild(divDocImgCont)
	
	let label = document.createElement("label")
	label.classList.add("docLabel")
	label.innerText = "SAVE"
	label.addEventListener("click", e => {
		eel.pickSaveLocation()(function (locs) {
			if (locs[0]) {
				label.dataset.path = locs[0]
				label.innerText = locs[1]
			}
		})
	})
	divDoc.appendChild(label)
	previewCont.appendChild(divDoc)
}
function saveDocs() {
	createNewDoc()
	document.querySelectorAll(".doc label").forEach((el) => {
		el.classList.add("visible")
	})
	nextButton.setAttribute("onclick", "submitDocs()")
}
function submitDocs() {
	document.querySelectorAll(".doc").forEach((doc) => {
		let newDocImgs = []
		doc.querySelectorAll("img").forEach((img) => {
			newDocImgs.push([img.dataset.ext, img.src])
		})
		docs.push([doc.querySelector("label").dataset.path, newDocImgs])
	})
	eel.inputDocuments(docs)
}
