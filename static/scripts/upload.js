var tags;
var averageSpeed = 0;

//search
document.getElementById("search")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode == 13) {
        document.getElementById("go-btn").click();
    }
});

function go_upload() {
  window.location = "/upload";
}

function go_search() {
  var key = document.getElementById('search').value;
  window.location = "/search/"+key;
}

//Progress Bar
var progress = document.querySelector('.percent');

// Setup the dnd listeners.
var dropZone = document.getElementById('drop_zone');
dropZone.addEventListener('dragover', handleDragOver, false);
dropZone.addEventListener('drop', handleFileDropped, false);
// document.getElementById('files').addEventListener('change', handleFileSelect, false);

//Prevent Drag Over
window.addEventListener("dragover",function(e){
	e = e || event;
	e.preventDefault();
},false);
window.addEventListener("drop",function(e){
	e = e || event;
	e.preventDefault();
},false);

function base64ArrayBuffer(arrayBuffer) {
  var base64    = ''
  var encodings = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

  var bytes         = new Uint8Array(arrayBuffer)
  var byteLength    = bytes.byteLength
  var byteRemainder = byteLength % 3
  var mainLength    = byteLength - byteRemainder

  var a, b, c, d
  var chunk

  // Main loop deals with bytes in chunks of 3
  for (var i = 0; i < mainLength; i = i + 3) {
    // Combine the three bytes into a single integer
    chunk = (bytes[i] << 16) | (bytes[i + 1] << 8) | bytes[i + 2]

    // Use bitmasks to extract 6-bit segments from the triplet
    a = (chunk & 16515072) >> 18 // 16515072 = (2^6 - 1) << 18
    b = (chunk & 258048)   >> 12 // 258048   = (2^6 - 1) << 12
    c = (chunk & 4032)     >>  6 // 4032     = (2^6 - 1) << 6
    d = chunk & 63               // 63       = 2^6 - 1

    // Convert the raw binary segments to the appropriate ASCII encoding
    base64 += encodings[a] + encodings[b] + encodings[c] + encodings[d]
  }

  // Deal with the remaining bytes and padding
  if (byteRemainder == 1) {
    chunk = bytes[mainLength]

    a = (chunk & 252) >> 2 // 252 = (2^6 - 1) << 2

    // Set the 4 least significant bits to zero
    b = (chunk & 3)   << 4 // 3   = 2^2 - 1

    base64 += encodings[a] + encodings[b] + '=='
  } else if (byteRemainder == 2) {
    chunk = (bytes[mainLength] << 8) | bytes[mainLength + 1]

    a = (chunk & 64512) >> 10 // 64512 = (2^6 - 1) << 10
    b = (chunk & 1008)  >>  4 // 1008  = (2^6 - 1) << 4

    // Set the 2 least significant bits to zero
    c = (chunk & 15)    <<  2 // 15    = 2^4 - 1

    base64 += encodings[a] + encodings[b] + encodings[c] + '='
  }
  
  return base64
}

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

    // var author = document.forms["upload_form"]["author"].value.trim();
    // var title = document.forms["upload_form"]["title"].value.trim();
    // var category = document.forms["upload_form"]["category"].value.trim();
    // var tags = document.forms["upload_form"]["tags-hidden"].value.trim();
    // var tags_input = document.forms["upload_form"]["tags-input"].value.trim();

    // if (tags == "" && tags_input != ""){
    // 	tags = tags_input;
    // }

    // if (author == "" || title == "" || category == "" || tags == "") {
    //     alert("All fields marked with * are required");
    //     return false;
    // }

    return uploadFile();
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

// function uploadFile() {

// 	var file = document.getElementById('files').files[0];

// 	if (!file) {
// 		alert("File not uploaded!")
// 		return;
// 	}
	
// 	var loaded = 0;
// 	var step = 512*1024;
// 	var total = file.size;
// 	var start = 0;
// 	var xhr = new XMLHttpRequest();
// 	var fd = new FormData();
// 	fileName = generateUUID() + '.' + file.name.split('.').pop();
// 	averageSpeed = 0;

// 	// alert(fileName);

// 	document.getElementById("progress-bar").style.display = "block";
// 	document.getElementById("cancel_upload").style.display = "none";
// 	document.getElementById("submit_button").style.display = "none";
// 	document.getElementById("form_data").style.display = "none";
// 	document.getElementById("insturction").style.display = "block";

// 	fd.append('fileName', fileName);
// 	fd.append('reading', 'false');
// 	fd.append('title', document.getElementById('title').value);
// 	fd.append('author', document.getElementById('author').value);
// 	fd.append('tags', document.getElementById('tags').value);
// 	fd.append('description', document.getElementById('description').value);
// 	fd.append('category', document.getElementById('category').value);
// 	fd.append('school', document.getElementById('school').value);
// 	fd.append('course', document.getElementById('course').value);

// 	xhr.open("POST", "/upload/upload_data");
//   xhr.send(fd);

// 	var reader = new FileReader();
// 	var xhr = new XMLHttpRequest();

// 	reader.onload = function(e){
// 		var fd = new FormData();
// 		var xhr = new XMLHttpRequest();
//         var upload = xhr.upload;
//         var processDone = false;
//         xhr.addEventListener("load", uploadComplete, false);
//         upload.addEventListener('load',function(){
// 	        loaded += step;
// 	        var percentComplete = Math.round((loaded / total) * 100);

// 	        progress.style.width = percentComplete.toString() + '%';
//     			progress.textContent = percentComplete.toString() + '%';

//             if (loaded <= total) {
//                     blob = file.slice(loaded, loaded+step);
//                     reader.readAsArrayBuffer(blob);
//             } else {
//             	if (!processDone) {
//                     loaded = total;
//                     fd.append('finished', 'true');
//                     fd.append('fileName', fileName);
//                     xhr.open("POST", "/upload/upload_data?fileName="+fileName+"&nocache="+new Date().getTime());
// 	    			xhr.send(fd);
// 	    			processDone = true;
//                 } else {
//         //         	setTimeout(function () {
// 	       //  			window.location = window.location.href + "/upload_success";
//     				// }, 2000);
//                 }
//             }
// 	    },false);
// 	    fd.append('blob', base64ArrayBuffer(e.target.result));
// 	    fd.append('reading', 'true');
// 	    fd.append('fileName', fileName);
// 	    xhr.open("POST", "/upload/upload_data?fileName="+fileName+"&nocache="+new Date().getTime());
// 	    xhr.send(fd);

// 	    checkUploadSpeed( 10, function ( speed, average ) {
// 	    	document.getElementById( 'speed' ).innerHTML = '<strong>Speed: </strong>' + speed + 'kbs';
// 	    	document.getElementById( 'time' ).innerHTML = '<strong>Time Remaining: </strong> ' + Math.round(((total-loaded) / 1024) / averageSpeed) + 's';
// 		});
// 	};
// 	var blob = file.slice(start, step);
// 	reader.readAsArrayBuffer(blob); 
// }


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


function abortRead() {
	if( reader != null ) {
		reader.abort();
		document.getElementById("upload_form").reset();
		
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

// // Progress bar update
// function updateProgress(evt) {
// if (evt.lengthComputable) {
// 	var percentLoaded = Math.round((evt.loaded / evt.total) * 100);
// 		// Increase the progress bar length.
// 		if (percentLoaded < 100) {
// 			progress.style.width = percentLoaded + '%';
// 			progress.textContent = percentLoaded + '%';
// 		}
// 	}
// }


// Select file
// function handleFileSelect(evt) {

// 	uploadhint = document.getElementsByClassName("upload_hint");
// 	for (var i = 0; i < uploadhint.length; i++) {
// 		uploadhint[i].style.display = 'none';
// 	}

// 	uploadshow = document.getElementsByClassName("upload_show");
// 	for (var i = 0; i < uploadshow.length; i++) {
// 		uploadshow[i].style.display = 'block';
// 	}

// 	progress.style.width = '0%';
// 	progress.textContent = '0%';

// 	reader = new FileReader();
// 	reader.onerror = errorHandler;

// 	// Read in the image file as a binary string.
// 	reader.readAsBinaryString(evt.target.files[0]);

// }



// Drop file
function handleFileDropped(evt) {
	fileSelected();
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

	// Read in the image file as a binary string.
	reader.readAsBinaryString(files[0]);

}


function handleDragOver(evt) {
	evt.stopPropagation();
	evt.preventDefault();
	evt.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
}


function uploadFailed(evt) {
  	alert("There was an error attempting to upload the file.");
}


function uploadCanceled(evt) {
  	alert("The upload has been canceled by the user or the browser dropped the connection.");
} 


// Testing new upload method

var maxBlockSize = 256 * 1024;//Each file will be split in 256 KB.
var numberOfBlocks = 1;
var selectedFile = null;
var currentFilePointer = 0;
var totalBytesRemaining = 0;
var blockIds = new Array();
var blockIdPrefix = "block-";
var submitUri = null;
var bytesUploaded = 0;
var fileName = '';
var averageSpeed = 0;

$(document).ready(function () {
    $("#files").bind('change', handleFileSelect);
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        // Great success! All the File APIs are supported.
    } else {
        alert('The File APIs are not fully supported in this browser.');
    }
});
 
//Read the file and find out how many blocks we would need to split it.
function handleFileSelect(e) {
    maxBlockSize = 256 * 1024;
    currentFilePointer = 0;
    totalBytesRemaining = 0;
    selectedFile = document.getElementById('files').files[0];
    // $("#output").show();
    document.getElementById('fileName').innerHTML = '<strong>Name:</strong> ' + selectedFile.name;
    document.getElementById('fileSize').innerHTML = '<strong>Size:</strong> ' + selectedFile.size;
    document.getElementById('fileType').innerHTML = '<strong>Type:</strong> ' + selectedFile.type;

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

    var fileSize = selectedFile.size;
    if (fileSize < maxBlockSize) {
        maxBlockSize = fileSize;
        console.log("max block size = " + maxBlockSize);
    }
    totalBytesRemaining = fileSize;
    if (fileSize % maxBlockSize == 0) {
        numberOfBlocks = fileSize / maxBlockSize;
    } else {
        numberOfBlocks = parseInt(fileSize / maxBlockSize, 10) + 1;
    }
    console.log("total blocks = " + numberOfBlocks);

    var fd = new FormData();
    var xhr = new XMLHttpRequest();
    UUID = generateUUID();
    fileName = UUID + '.' + selectedFile.name.split('.').pop();

    fd.append('geturi', 'true');
    xhr.open("POST", "/upload/upload_data");
    xhr.addEventListener("load", function(evt) {
      var baseUrl = evt.target.responseText;
      var indexOfQueryStart = baseUrl.indexOf("?");
      submitUri = baseUrl.substring(0, indexOfQueryStart) + '/' + UUID + baseUrl.substring(indexOfQueryStart);
      console.log(submitUri);
    }, false);
    xhr.send(fd);
}

function uploadFile() {
    var xhr = new XMLHttpRequest();
    var fd = new FormData();

    averageSpeed = 0;
    document.getElementById("progress-bar").style.display = "block";
    document.getElementById("cancel_upload").style.display = "none";
    document.getElementById("submit_button").style.display = "none";
    document.getElementById("form_data").style.display = "none";
    document.getElementById("insturction").style.display = "block";

    fd.append('fileName', fileName);
    fd.append('reading', 'false');
    fd.append('title', document.getElementById('title').value);
    fd.append('author', document.getElementById('author').value);
    fd.append('tags', document.getElementById('tags').value);
    fd.append('description', document.getElementById('description').value);
    fd.append('category', document.getElementById('category').value);
    fd.append('school', document.getElementById('school').value);
    fd.append('course', document.getElementById('course').value);

    xhr.open("POST", "/upload/upload_data");
    xhr.send(fd);

    uploadFileInBlocks();
}

var reader = new FileReader();

reader.onloadend = function (evt) {
    if (evt.target.readyState == FileReader.DONE) { // DONE == 2
        var uri = submitUri + '&comp=block&blockid=' + blockIds[blockIds.length - 1];
        var requestData = new Uint8Array(evt.target.result);
        $.ajax({
            url: uri,
            type: "PUT",
            data: requestData,
            processData: false,
            beforeSend: function(xhr) {
                xhr.setRequestHeader('x-ms-blob-type', 'AppendBlob');
            },
            success: function (data, status) {
                console.log(data);
                console.log(status);
                bytesUploaded += requestData.length;
                var percentComplete = ((parseFloat(bytesUploaded) / parseFloat(selectedFile.size)) * 100).toFixed(2);
                progress.style.width = percentComplete.toString() + '%';
                progress.textContent = percentComplete.toString() + '%';
                uploadFileInBlocks();
            },
            error: function(xhr, desc, err) {
                console.log(desc);
                console.log(err);
            }
        });
    }
};

function uploadFileInBlocks() {
    if (totalBytesRemaining > 0) {
        console.log("current file pointer = " + currentFilePointer + " bytes read = " + maxBlockSize);
        var fileContent = selectedFile.slice(currentFilePointer, currentFilePointer + maxBlockSize);
        var blockId = blockIdPrefix + pad(blockIds.length, 6);
        console.log("block id = " + blockId);
        blockIds.push(btoa(blockId));
        reader.readAsArrayBuffer(fileContent);
        currentFilePointer += maxBlockSize;
        totalBytesRemaining -= maxBlockSize;
        if (totalBytesRemaining < maxBlockSize) {
            maxBlockSize = totalBytesRemaining;
        }
        // checkUploadSpeed( 10, function ( speed, average ) {
        //     document.getElementById( 'speed' ).innerHTML = '<strong>Speed: </strong>' + speed + 'kbs';
        //     document.getElementById( 'time' ).innerHTML = '<strong>Time Remaining: </strong> ' + Math.round((totalBytesRemaining / 1024) / averageSpeed) + 's';
        // });
    } else {
        commitBlockList();
    }
}
 
function commitBlockList() {
    var uri = submitUri + '&comp=blocklist';
    console.log(uri);
    var requestBody = '<?xml version="1.0" encoding="utf-8"?><BlockList>';
    for (var i = 0; i < blockIds.length; i++) {
        requestBody += '<Latest>' + blockIds[i] + '</Latest>';
    }
    requestBody += '</BlockList>';
    console.log(requestBody);
    $.ajax({
        url: uri,
        type: "PUT",
        data: requestBody,
        beforeSend: function (xhr) {
            xhr.setRequestHeader('x-ms-blob-content-type', selectedFile.type);
        },
        success: function (data, status) {
            console.log(data);
            console.log(status);
        },
        error: function (xhr, desc, err) {
            console.log(desc);
            console.log(err);
        }
    });

    var xhr = new XMLHttpRequest();
    var fd = new FormData();

    fd.append('finished', 'true');
    fd.append('fileName', fileName);
    xhr.open("POST", "/upload/upload_data?fileName="+fileName+"&nocache="+new Date().getTime());
    xhr.send(fd);
    setTimeout(function () {
        window.location = window.location.href + "/upload_success";
    }, 500);
}
function pad(number, length) {
    var str = '' + number;
    while (str.length < length) {
        str = '0' + str;
    }
    return str;
}