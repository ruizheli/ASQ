$(".logo").on("click", function(){
	$(location).attr('href', 'home');
})

//Read Tags
document.addEventListener("DOMContentLoaded", function() {
	var textarea = document.getElementById("tags");
	var tagOut = document.getElementById("tags-output");
	var hidden = document.getElementsByName("tags")[0];

	textarea.addEventListener("keyup", function() {

		function makeTagDiv(tag) {
			var div = document.createElement("div");
			div.innerHTML = tag;
			
			div.style.border = "Gpx solid silver";
			div.style.borderRadius = "4px";
			div.style.display = "inline-block";
			div.style.padding = ".25em 1em .25em 1em";

			div.addEventListener("click", function() {
				div.parentNode.removeChild(div);
				// hidden.value = hidden.value.replace(div.innerHTML + " ", "");
			});
			
			return div;
		}

		console.log( textarea.value );

		while(true) {
			var match = /(\w+)(,|\s+)/.exec(textarea.value);
			if( match === null )
				break;
			textarea.value = textarea.value.replace(/.*(,|\s+)/, "");
			tagOut.appendChild( makeTagDiv(match[1]) );

			// e.g. add tag (match[1]) to hidden fild's list
			// hidden.value += match[1] + " ";
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



//Progress Bar
var reader;
var progress = document.querySelector('.percent');

function abortRead() {
	reader.abort();
	document.getElementById("files").disabled = false;
}

function errorHandler(evt) {
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
		};
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
	document.getElementById("drop_zone").style.display = "none";

	progress.style.width = '0%';
	progress.textContent = '0%';

	reader = new FileReader();
	reader.onerror = errorHandler;
	reader.onprogress = updateProgress;
	reader.onabort = function(e) {
		alert('File read cancelled');
	};
	reader.onloadstart = function(e) {
		document.getElementById('progress_bar').className = 'loading';
	};
	reader.onload = function(e) {
		// Ensure that the progress bar displays 100% at the end.
		progress.style.width = '100%';
		progress.textContent = '100%';
		setTimeout("document.getElementById('progress_bar').className='';", 2000);
	}

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
	document.getElementById("drop_zone").style.display = "none";

	evt.stopPropagation();
	evt.preventDefault();

	var files = evt.dataTransfer.files; // FileList object.

	progress.style.width = '0%';
	progress.textContent = '0%';

	reader = new FileReader();
	reader.onerror = errorHandler;
	reader.onprogress = updateProgress;

	reader.onabort = function(e) {
		alert('File read cancelled');
	};

	reader.onloadstart = function(e) {
		document.getElementById('progress_bar').className = 'loading';
	};
	
	reader.onload = function(e) {
		// Ensure that the progress bar displays 100% at the end.
		progress.style.width = '100%';
		progress.textContent = '100%';
		setTimeout("document.getElementById('progress_bar').className='';", 2000);
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

// Setup the dnd listeners.
var dropZone = document.getElementById('drop_zone');
dropZone.addEventListener('dragover', handleDragOver, false);
dropZone.addEventListener('drop', handleFileDropped, false);

document.getElementById('files').addEventListener('change', handleFileSelect, false);