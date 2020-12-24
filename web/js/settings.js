let settingsCont = document.querySelector(".contentCont");

function updateInputSetting(ev) {
	let el = ev.target;
	let inputSettings = {[el.id]: getInputValue(el)};

	el = el.parentElement;
	while (el.parentElement.hasAttribute("id")) {
		el = el.parentElement;
		inputSettings = {[el.id]: inputSettings}
	};
	eel.updateSettings(inputSettings);
}
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
function createSetting(settings, prefType, pref) {
	let setting = document.createElement("div");
	setting.classList.add("setting");

	let label = document.createElement("label");
	label.classList.add("settingLabel");
	label.setAttribute("for", pref);
	label.innerText = (pref.charAt(0).toUpperCase() + pref.slice(1)).replace(/([a-z])([A-Z])/g, "$1 $2");
	setting.appendChild(label);

	let input = document.createElement("input");
	input.classList.add("settingInput");
	input.id = pref;
	switch (typeof settings[prefType][pref]) {
		case "number":
			input.type = "number";
			input.min = settings["constraints"][pref + "Min"]
			input.max = settings["constraints"][pref + "Max"]
			break;
		case "boolean":
			input.type = "checkbox";
			break;
		default:
			input.type = "text";
	};
	if (input.type == "checkbox") {
		input.checked = settings[prefType][pref];
	} else {
		input.value = settings[prefType][pref];
	}
	input.addEventListener("change", updateInputSetting);
	setting.appendChild(input);
	return setting;
};
function createSettingsSection(settings, prefType, title) {
	let prefsDiv = document.createElement("div");
	prefsDiv.classList.add("settingsSection");
	prefsDiv.id = prefType;
	prefsDiv.setAttribute("title", title);
	Object.keys(settings[prefType]).filter(key => {return !key.startsWith("--")}).forEach(pref => {
		prefsDiv.appendChild(createSetting(settings, prefType, pref));
	});
	return prefsDiv;
};
function showSettings() {
	settingsCont.innerHTML = "";
	eel.readSettings()(settings => {
		[["general", "General Preferences"]].forEach(item => {
			settingsCont.appendChild(createSettingsSection(settings, ...item));
		});
		let docPrefsDiv = document.createElement("div");
		docPrefsDiv.classList.add("settingsSection");
		docPrefsDiv.setAttribute("title", "Documents Preferences");
		[["pdf", "PDF"]].forEach(item => {
			docPrefsDiv.appendChild(createSettingsSection(settings, ...item));
		});
		settingsCont.appendChild(docPrefsDiv);
	});
};
showSettings();
