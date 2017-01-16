var tags;
var averageSpeed = 0;
function generateUUID() {
    var d = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
};

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

function checkUploadSpeed( iterations, update ) {
    var index = 0,
        timer = window.setInterval( check, 500 ); //check every 5 seconds
    check();

    function check() {
        var xhr = new XMLHttpRequest(),
            url = '?cache=' + Math.floor( Math.random() * 10000 ), //random number prevents url caching
            data = getRandomString( 1 ), //1 meg POST size handled by all servers
            startTime,
            speed = 0;
        xhr.onreadystatechange = function ( event ) {
            if( xhr.readyState == 4 ) {
                speed = Math.round( 1024 / ( ( new Date() - startTime ) / 1000 ) );
                averageSpeed == 0 
                    ? averageSpeed = speed 
                    : averageSpeed = Math.round( ( averageSpeed + speed ) / 2 );
                update( speed, averageSpeed );
                index++;
                if( index == iterations ) {
                    window.clearInterval( timer );
                };
            };
        };
        xhr.open( 'POST', url, true );
        startTime = new Date();
        xhr.send( data );
    };

    function getRandomString( sizeInMb ) {
        var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~!@#$%^&*()_+`-=[]\{}|;':,./<>?", //random data prevents gzip effect
            iterations = sizeInMb * 1024 * 1024, //get byte count
            result = '';
        for( var index = 0; index < iterations; index++ ) {
            result += chars.charAt( Math.floor( Math.random() * chars.length ) );
        };     
        return result;
    };
};

function fileSelected() {
  	var file = document.getElementById('files').files[0];
  		if (file) {
    	var fileSize = 0;
    	if (file.size > 1024 * 1024)
      		fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
    	else
      	fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';
          
    	document.getElementById('fileName').innerHTML = 'Name: ' + file.name;
    	document.getElementById('fileSize').innerHTML = 'Size: ' + fileSize;
    	document.getElementById('fileType').innerHTML = 'Type: ' + file.type;
  	}
}

function uploadFile() {
	var file = document.getElementById('files').files[0];
	var loaded = 0;
	var step = 256*1024;
	var total = file.size;
	var start = 0;
  	var xhr = new XMLHttpRequest();
  	var fd = new FormData();
  	fileName = generateUUID();
  	averageSpeed = 0;

  	fd.append('fileName', fileName);
  	fd.append('reading', 'false');
  	fd.append('title', document.getElementById('title'));
  	fd.append('author', document.getElementById('author'));
  	fd.append('tags', document.getElementById('tags'));
  	fd.append('description', document.getElementById('description'));
  	fd.append('category', document.getElementById('category'));
  	xhr.open("POST", "/upload/upload_data");
    xhr.send(fd);

  	var reader = new FileReader();

	reader.onload = function(e){
		var xhr = new XMLHttpRequest();
		var fd = new FormData();
        var upload = xhr.upload;
        xhr.addEventListener("load", uploadComplete, false);
        upload.addEventListener('load',function(){
	        loaded += step;
	        var percentComplete = Math.round((loaded / total) * 100);
	        document.getElementById('progressNumber').innerHTML = percentComplete.toString() + '%';
            if (loaded <= total) {
                    blob = file.slice(loaded, loaded+step);
                    reader.readAsBinaryString(blob);
            } else {
                    loaded = total;
                    window.location = window.location.href + "/upload_success"
            }
	    },false);
	    fd.append('blob', e.target.result);
	    fd.append('reading', 'true');
	    fd.append('fileName', fileName);
	    xhr.open("POST", "/upload/upload_data?fileName="+fileName+"&nocache="+new Date().getTime());
	    xhr.send(fd);

	    checkUploadSpeed( 1, function ( speed, average ) {
	    	document.getElementById( 'speed' ).textContent = 'speed: ' + speed + 'kbs';
	    	document.getElementById( 'time' ).textContent = 'time remaining: ' + Math.round(((total-loaded) / 1024) / averageSpeed) + 's';
		});
	};
	var blob = file.slice(start, step);
	reader.readAsBinaryString(blob); 
}

function uploadProgress(evt) {
  	if (evt.lengthComputable) {
    	var percentComplete = Math.round(evt.loaded * 100 / evt.total);
    	document.getElementById('progressNumber').innerHTML = percentComplete.toString() + '%';
  	}
  	else {
    	document.getElementById('progressNumber').innerHTML = 'unable to compute';
  	}
}

function uploadComplete(evt) {
  	/* This event is raised when the server send back a response */
  	if (evt.target.responseText == 'upload_fail')
  		window.location = window.location.href + "/" + evt.target.responseText;
}

function uploadFailed(evt) {
  	alert("There was an error attempting to upload the file.");
}

function uploadCanceled(evt) {
  	alert("The upload has been canceled by the user or the browser dropped the connection.");
} 

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
