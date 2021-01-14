let newDocButton = document.querySelector("#createNewDoc")
let nextButton = document.querySelector("#next")
let fileInput = document.querySelector("#fileInput")
let previewCont = document.querySelector(".previewImageContainer")
let pickingSaveLocations = false

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
	fileInput.value = ""
}
function createNewDoc() {
	if (newDocButton.classList.contains("disabled")) {
		return
	}
	let imgs = previewCont.querySelectorAll(":scope > img")
	let divDoc = document.createElement("div")
	divDoc.classList.add("doc")
	
	let divDocImgCont = document.createElement("div")
	divDocImgCont.classList.add("docImgCont")
	let closeButton = document.createElement("div")
	closeButton.classList.add("closeButton")
	closeButton.addEventListener("click", e => {
		let div = e.target.parentElement.parentElement
		div.parentElement.removeChild(div)
	})
	divDocImgCont.appendChild(closeButton)

	imgs.forEach((img) => {
		divDocImgCont.appendChild(img)
	})
	divDoc.appendChild(divDocImgCont)
	
	let label = document.createElement("label")
	label.classList.add("docLabel")
	label.innerText = "SAVE AS"
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
function next() {
	if (nextButton.classList.contains("disabled")) {
		return false
	}
	if (!pickingSaveLocations) {
		createNewDoc()
		fileInput.disabled = true
		document.querySelectorAll(".doc label").forEach((el) => {
			el.classList.add("visible")
		})
		document.querySelector("header > h1").innerText = "Pick save formats and locations"
		newDocButton.style.visibility = "hidden";
		pickingSaveLocations = true
		return false
	} else {
		let valid = validateDocs()
		if (valid) {
			let docs = []
			document.querySelectorAll(".doc").forEach((doc) => {
				let newDocImgs = []
				doc.querySelectorAll("img").forEach((img) => {
					newDocImgs.push(img.src)
				})
				docs.push([doc.querySelector("label").dataset.path, newDocImgs])
			})
			eel.inputDocuments(docs)
		}
		return valid
	}
}
function validateDocs() {
	let valid = true
	let errorMsg = ""
	let docs = document.querySelectorAll(".doc")
	let saveLocations = []
	docs.forEach(doc => {
		doc.classList.remove("error")
		if (!(doc.querySelector("label").dataset.path)) {
			valid = false
			doc.classList.add("error")
		}
	})
	if (!valid) {
		errorMsg += "You haven't picked save locations for some documents. They are highlighted. Please pick save locations for them and try again."
		alert(errorMsg)
		return valid
	}
	docs.forEach(doc => {
		let saveLocation = doc.querySelector("label").dataset.path
		if (saveLocations.includes(saveLocation)) {
			valid = false
			doc.classList.add("error")
			docs[saveLocations.indexOf(saveLocation)].classList.add("error")
		}
		saveLocations.push(saveLocation)
	})
	if (!valid) {
		errorMsg += "You're trying to save multiple documents to the same location. They are highlighted. Please pick different save locations for them and try again."
		alert(errorMsg)
		return valid
	}
	return valid
}
