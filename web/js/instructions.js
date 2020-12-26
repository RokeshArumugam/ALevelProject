let instructionsCont = document.querySelector(".contentCont");

function fetchInstructions() {
	let req = new XMLHttpRequest();
	req.open('GET', 'loadParts/instructions.md');
	req.onreadystatechange = function() {
		if (req.readyState == 4) {
			loadInstructions(req.responseText);
		};
	};
	req.send();
};

function loadInstructions(text) {
	lines = [];
	openLists = [];
	for (let line of text.split("\n").filter(line => {return line})) {
		let lastLine = lines[lines.length - 1];

		line = line.replace(/^# ([^#]*)$/g, "<h2>$1</h2>");
		line = line.replace(/^## ([^#]*)$/g, "<h3>$1</h3>");
		line = line.replace(/^### ([^#]*)$/g, "<h4>$1</h4>");
		line = line.replace(/^#### ([^#]*)$/g, "<h5>$1</h5>");
		
		line = line.replace(/^\-{3,}.*/g, "<hr>");

		let listType = "";
		let lineBeforeList = line;
		line = line.replace(/^( *) \- (.*)$/g, "$1<li>$2</li>");
		line = line.replace(/^( *) \* (.*)$/g, "$1<li>$2</li>");
		if (line != lineBeforeList) {
			listType = "ul";
		} else {
			line = line.replace(/^( *)[0-9]*\. (.*)$/g, "$1<li>$2</li>");
			if (line != lineBeforeList) {
				listType = "ol";
			};
		};
		if (listType) {
			let indentLevel = (line.replace(/^( *).*/g, "$1").split(" ").length - 1) / 2 + 1;
			if ((indentLevel == openLists.length) && (openLists[openLists.length - 1] != listType)) {
				lines.push("</" + openLists.pop() + ">");
				lines.push("<" + listType + ">");
				openLists.push(listType);
			} else if (indentLevel > openLists.length) {
				lines.push("<" + listType + ">");
				openLists.push(listType);
			} else if (indentLevel < openLists.length) {
				lines.push("</" + openLists.pop() + ">");
			};
			line = line.replace(/^ *(.*)/g, "$1");
		};

		line = line.replace(/^([^<][^\n]*)$/g, "<p>$1</p>");
		while (!listType && openLists.length) {
			lines.push("</" + openLists.pop() + ">");
		};
		lines.push(line);
	};
	instructionsCont.innerHTML = lines.join("");
};
fetchInstructions();
