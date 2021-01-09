let settingsCont = document.querySelector(".contentCont");
let SETTINGS = {};

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
	let inputType = el.type;
	let inputKey = el.id;
	let inputValue = getInputValue(el);
	let immediateInputSection = {[inputKey]: inputValue};
	let inputSection = immediateInputSection;
	
	if ((!inputValue && (inputValue != false)) || (inputType == "number" && isNaN(inputValue))) return
	
	el = el.parentElement;
	while (el.parentElement.hasAttribute("id")) {
		el = el.parentElement;
		inputSection = {[el.id]: inputSection}
	};
	
	let tempInputSection = inputSection;
	let section = SETTINGS;
	let newSection;
	do {
		let key = Object.keys(tempInputSection)[0];
		tempInputSection = tempInputSection[key];
		newSection = section[key];
		if (typeof newSection == "object") {
			section = newSection;
		};
	} while (typeof newSection == "object")
	
	switch (inputType) {
		case "number":
			let min = getConstraint(section, inputKey + "Min");
			let max = getConstraint(section, inputKey + "Max");
			if (inputValue < min) {
				ev.target.value = min;
				immediateInputSection[inputKey] = min;
			};
			if (inputValue > max) {
				ev.target.value = max;
				immediateInputSection[inputKey] = max;
			};
			break;
		default:
			break;
	};
	eel.updateSettings(inputSection)(() => {
		getSettings();
	});
}
function getConstraint(section, key) {
	if (section.hasOwnProperty("__" + key)) {
		return section["__" + key]
	} else {
		return SETTINGS["__constraints"][key]
	}
}
function createSetting(section, key) {
	let settingDiv = document.createElement("div");
	settingDiv.classList.add("settingDiv");

	let label = document.createElement("label");
	label.classList.add("settingLabel");
	label.setAttribute("for", key);
	label.innerText = camelToSentence(key);
	settingDiv.appendChild(label);

	let input;
	switch (typeof section[key]) {
		case "number":
			input = document.createElement("input");
			input.type = "number";
			input.min = getConstraint(section, key + "Min");
			input.max = getConstraint(section, key + "Max");
			break;
		case "string":
			input = document.createElement("select");
			getConstraint(section, key + "Allowed").forEach(val => {
				let option = document.createElement("option");
				option.value = val;
				option.innerText = val;
				input.appendChild(option);
			});
			break;
		case "boolean":
			input = document.createElement("input");
			input.type = "checkbox";
			input.checked = section[key];
			break;
		default:
			input = document.createElement("input");
			input.type = "text";
	};
	input.value = section[key];
	input.addEventListener("change", updateInputSetting);
	input.classList.add("settingInput");
	input.id = key;
	settingDiv.appendChild(input);
	return settingDiv;
};
function createSettingsSection(section, sectionName) {
	let sectionDiv = document.createElement("div");
	sectionDiv.classList.add("settingsSection");
	sectionDiv.id = sectionName;
	sectionDiv.setAttribute("title", camelToSentence(sectionName));
	Object.keys(section).filter(key => {return !key.startsWith("__")}).forEach(key => {
		if (typeof section[key] == "object") {
			sectionDiv.appendChild(createSettingsSection(section[key], key));
		} else {
			sectionDiv.appendChild(createSetting(section, key));
		}
	});
	return (sectionName) ? sectionDiv : sectionDiv.children;
};
function getSettings(callback) {
	eel.getSettings()(storedSettings => {
		SETTINGS = storedSettings;
		if (callback) {
			callback();
		};
	});
};
function showSettings() {
	settingsCont.innerHTML = "";
	getSettings(() => {
		[...createSettingsSection(SETTINGS, "")].forEach(el => {
			settingsCont.appendChild(el);
		});
	});
};
showSettings();
