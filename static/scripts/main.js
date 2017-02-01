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
	key = key.split(' ').join('+');
	window.location = "/search/"+key;
}