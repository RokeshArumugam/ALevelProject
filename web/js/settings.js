let settingsCont = document.querySelector(".contentCont");

function camelToSentence(text) {
	return (text.charAt(0).toUpperCase() + text.slice(1)).replace(/([a-z])([A-Z])/g, "$1 $2")
};
function getInputValue(input) {
	switch (input.type) {
		case "number":
			return input.valueAsNumber;
			break;
		case "checkbox":
			return input.checked;
			break;
		default:
			return input.value;
	};
}
function updateInputSetting(ev) {
	let el = ev.target;
	let inputSettings = {[el.id]: getInputValue(el)};
	
	if (!inputSettings[el.id] || (el.type == "number" && isNaN(inputSettings[el.id]))) return
	
	el = el.parentElement;
	while (el.parentElement.hasAttribute("id")) {
		el = el.parentElement;
		inputSettings = {[el.id]: inputSettings}
	};
	eel.updateSettings(inputSettings);
}
function createSetting(settings, section, key) {
	let setting = document.createElement("div");
	setting.classList.add("setting");

	let label = document.createElement("label");
	label.classList.add("settingLabel");
	label.setAttribute("for", key);
	label.innerText = camelToSentence(key);
	setting.appendChild(label);

	let input = document.createElement("input");
	input.classList.add("settingInput");
	input.id = key;
	switch (typeof section[key]) {
		case "number":
			input.type = "number";
			input.min = settings["--constraints"][key + "Min"]
			input.max = settings["--constraints"][key + "Max"]
			break;
		case "boolean":
			input.type = "checkbox";
			break;
		default:
			input.type = "text";
	};
	if (input.type == "checkbox") {
		input.checked = section[key];
	} else {
		input.value = section[key];
	}
	input.addEventListener("change", updateInputSetting);
	setting.appendChild(input);
	return setting;
};
function createSettingsSection(settings, section, sectionName) {
	let sectionDiv = document.createElement("div");
	sectionDiv.classList.add("settingsSection");
	sectionDiv.id = sectionName;
	sectionDiv.setAttribute("title", camelToSentence(sectionName));
	Object.keys(section).filter(key => {return !key.startsWith("--")}).forEach(key => {
		if (typeof section[key] == "object") {
			sectionDiv.appendChild(createSettingsSection(settings, section[key], key));
		} else {
			sectionDiv.appendChild(createSetting(settings, section, key));
		}
	});
	return (sectionName) ? sectionDiv : sectionDiv.children;
};
function showSettings() {
	settingsCont.innerHTML = "";
	eel.readSettings()(settings => {
		[...createSettingsSection(settings, settings, "")].forEach(el => {
			settingsCont.appendChild(el);
		});
	});
};
showSettings();
