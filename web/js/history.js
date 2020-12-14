let entryCont = document.querySelector(".historyEntriesCont")

eel.readHistory()(historyEntries => {
	historyEntries.forEach(entry => {
		let entryDiv = document.createElement("div")
		entryDiv.classList.add("historyEntry")

		let divDoc = document.createElement("div")
		divDoc.classList.add("doc")
		
		let divDocImgCont = document.createElement("div")
		divDocImgCont.classList.add("docImgCont")
		entry[1].forEach(imgSrc => {
			let img = document.createElement("img")
			img.src = imgSrc
			divDocImgCont.appendChild(img)
		})
		divDoc.appendChild(divDocImgCont)

		let label = document.createElement("label")
		label.classList.add("docLabel", "visible")
		label.innerText = "VIEW"
		label.addEventListener("click", e => {
			//TODO add preview image feature
		})
		divDoc.appendChild(label)
		entryDiv.appendChild(divDoc)
		
		let divDocInfo = document.createElement("div")
		divDocInfo.classList.add("docInfo")
		
		let divDocName = document.createElement("div")
		divDocName.classList.add("docName")
		divDocName.innerText = entry[0][0]
		divDocInfo.appendChild(divDocName)
		
		let divDocTime = document.createElement("div")
		divDocTime.classList.add("docTime")
		divDocTime.innerText = entry[0][1]
		divDocInfo.appendChild(divDocTime)
		entryDiv.appendChild(divDocInfo)
		entryCont.appendChild(entryDiv)
	})
})
