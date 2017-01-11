var tags;

//Validate Form
function validateForm() {
    var author = document.forms["upload_form"]["author"].value.trim();
    var title = document.forms["upload_form"]["title"].value.trim();
    var category = document.forms["upload_form"]["category"].value.trim();
    var tags = document.forms["upload_form"]["tags-hidden"].value.trim();

    if (author == "" || title == "" || category == "" || tags == "") {
        alert("All fields marked with * are required");
        return false;
    }
    return true;
}


//Read Tags
document.addEventListener("DOMContentLoaded", function() {
	var textarea = document.getElementById("tags");
	var tagOut = document.getElementById("tags-output");
	var hidden = document.getElementsByName("tags-hidden")[0];

	textarea.addEventListener("keyup", function() {

		function makeTagDiv(tag) {
			var div = document.createElement("div");
			div.innerHTML = "&#10005;&emsp;" + tag;
			
			div.style.border = "1px solid silver";
			div.style.borderRadius = "3px";
			div.style.display = "inline-block";
			div.style.padding = "0em 0.5em 0em 0.5em";
			div.style.fontSize = ".8em";

			div.addEventListener("click", function() {
				div.parentNode.removeChild(div);
				hidden.value = hidden.value.replace(div.innerHTML + " ", "");
			});
			
			return div;
		}

		while(true) {
			var match = /(\w+)(,|\s+)/.exec(textarea.value);
			if( match === null )
				break;
			textarea.value = textarea.value.replace(/.*(,|\s+)/, "");
			tagOut.appendChild( makeTagDiv(match[1]) );

			hidden.value += match[1] + " ";
		}

	});
});



//Prevent Drag Over
window.addEventListener("dragover",function(e){
	e = e || event;
	e.preventDefault();
},false);


window.addEventListener("drop",function(e){
	e = e || event;
	e.preventDefault();
},false);



// Setup the dnd listeners.
var dropZone = document.getElementById('drop_zone');
dropZone.addEventListener('dragover', handleDragOver, false);
dropZone.addEventListener('drop', handleFileDropped, false);
document.getElementById('files').addEventListener('change', handleFileSelect, false);


//Progress Bar
var reader = null;
var progress = document.querySelector('.percent');

function abortRead() {
	//console.log( "reader = " + reader ); 
	if( reader != null ) {
		reader.abort();
		
		// TODO (only a simpke fix; handler put here)
		reader.onabort(); // call handler explicitly
		uploadhint = document.getElementsByClassName("upload_hint");
		for (var i = 0; i < uploadhint.length; i++) {
			uploadhint[i].style.display = 'block';
		}

		uploadshow = document.getElementsByClassName("upload_show");
		for (var i = 0; i < uploadshow.length; i++) {
			uploadshow[i].style.display = 'none';
		}

		document.getElementById("browse_button").style.display = "table";

		document.getElementById("files").disabled = false;
	}
}

function errorHandler(evt) {
	//console.log("errorHandler(" + evt + ")");
	switch(evt.target.error.code) {
		case evt.target.error.NOT_FOUND_ERR:
			alert('File Not Found!');
			break;
		case evt.target.error.NOT_READABLE_ERR:
			alert('File is not readable');
			break;
		case evt.target.error.ABORT_ERR:
			break; // noop
		default:
			alert('An error occurred reading this file.');
	}
}

// Progress bar update
function updateProgress(evt) {
// evt is an ProgressEvent.
if (evt.lengthComputable) {
	var percentLoaded = Math.round((evt.loaded / evt.total) * 100);
		// Increase the progress bar length.
		if (percentLoaded < 100) {
			progress.style.width = percentLoaded + '%';
			progress.textContent = percentLoaded + '%';
		}
	}
}



// Select file
function handleFileSelect(evt) {
	document.getElementById("files").disabled = true;

	uploadhint = document.getElementsByClassName("upload_hint");
	for (var i = 0; i < uploadhint.length; i++) {
		uploadhint[i].style.display = 'none';
	}

	uploadshow = document.getElementsByClassName("upload_show");
	for (var i = 0; i < uploadshow.length; i++) {
		uploadshow[i].style.display = 'block';
	}

	progress.style.width = '0%';
	progress.textContent = '0%';

	reader = new FileReader();
	reader.onerror = errorHandler;
	reader.onprogress = updateProgress;
	reader.onabort = function(e) {
		//alert('File upload cancelled');
	};
	// reader.onloadstart = function(e) {
	// 	document.getElementById('progress_bar').className = 'loading';
	// };
	reader.onload = function(e) {
		// Ensure that the progress bar displays 100% at the end.
		progress.style.width = '100%';
		progress.textContent = '100%';
	};

// Read in the image file as a binary string.
reader.readAsBinaryString(evt.target.files[0]);

var output = [];
for (var i = 0, f; f = evt.target.files[i]; i++) {
	output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
		f.size, ' bytes, last modified: ',
		f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
		'</li>');
}
document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
}



// Drop file
function handleFileDropped(evt) {
	document.getElementById("files").disabled = true;
	uploadhint = document.getElementsByClassName("upload_hint");
	for (var i = 0; i < uploadhint.length; i++) {
		uploadhint[i].style.display = 'none';
	}

	uploadshow = document.getElementsByClassName("upload_show");
	for (var i = 0; i < uploadshow.length; i++) {
		uploadshow[i].style.display = 'block';
	}

	evt.stopPropagation();
	evt.preventDefault();

	var files = evt.dataTransfer.files; // FileList object.

	progress.style.width = '0%';
	progress.textContent = '0%';

	reader = new FileReader();
	reader.onerror = errorHandler;
	reader.onprogress = updateProgress;

	reader.onabort = function(e) {
		//alert('File read cancelled');
	};

	// reader.onloadstart = function(e) {
	// 	document.getElementById('progress_bar').className = 'loading';
	// };
	
	reader.onload = function(e) {
		// Ensure that the progress bar displays 100% at the end.
		progress.style.width = '100%';
		progress.textContent = '100%';
	}

	// Read in the image file as a binary string.
	reader.readAsBinaryString(files[0]);

	// files is a FileList of File objects. List some properties.
	var output = [];
	for (var i = 0, f; f = files[i]; i++) {
		output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
			f.size, ' bytes, last modified: ',
			f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
			'</li>');
	}
	document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
}

function handleDragOver(evt) {
	evt.stopPropagation();
	evt.preventDefault();
	evt.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
}
