function go_upload() {
	window.location = "/upload";
}

function go_search() {
	var key = document.getElementById('search').value;
	window.location = "/search/"+key;
}