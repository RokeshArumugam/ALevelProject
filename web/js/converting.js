let inputImg = document.querySelector("#inputImg")
let convertedText = document.querySelector(".previewDoc.converted")
let docProgressBar = document.querySelector(".docProgressCont .progressBar")
let docProgressMsg = document.querySelector(".docProgressCont .progressMsg")
let overallProgressBar = document.querySelector(".overallProgressCont .progressBar")
let overallProgressMsg = document.querySelector(".overallProgressCont .progressMsg")

eel.convertDocuments()

eel.expose(setInputImg)
function setInputImg(data) {
	inputImg.src = data
}

eel.expose(setConvertedText)
function setConvertedText(text) {
	convertedText.innerText = text
}

convertedText.addEventListener("DOMSubtreeModified", e => {
	convertedText.scrollTop = convertedText.scrollHeight
})

eel.expose(setDocProgressBarTotal)
function setDocProgressBarTotal(val) {
	docProgressBar.style.setProperty("--total", val)
}

eel.expose(setDocProgressBarCompleted)
function setDocProgressBarCompleted(val) {
	docProgressBar.style.setProperty("--completed", val)
	docProgressBar.style.setProperty("--percentage", "'" + Math.round(val / getComputedStyle(docProgressBar).getPropertyValue("--total") * 100).toString() + "%'")
}

eel.expose(setDocProgressMsg)
function setDocProgressMsg(text) {
	docProgressMsg.innerText = text
}

eel.expose(setOverallProgressBarTotal)
function setOverallProgressBarTotal(val) {
	overallProgressBar.style.setProperty("--total", val)
}

eel.expose(setOverallProgressBarCompleted)
function setOverallProgressBarCompleted(val) {
	overallProgressBar.style.setProperty("--completed", val)
	overallProgressBar.style.setProperty("--percentage", "'" + Math.round(val / getComputedStyle(overallProgressBar).getPropertyValue("--total") * 100).toString() + "%'")
}

eel.expose(setOverallProgressMsg)
function setOverallProgressMsg(text) {
	overallProgressMsg.innerText = text
}

eel.expose(finishedConverting)
function finishedConverting() {
	document.querySelector("h1").innerText = "Converted!"
	document.querySelector(".goBackPrompt").classList.add("visible")
}
