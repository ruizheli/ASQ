
var links = document.querySelectorAll('.jump');
var time_table = [3,6,13,23,39,69];
var player = document.getElementById("video");

if (links.length != time_table.length){
	alert("Time table doesn't match the concept table");
}

function jumpToTime(time){
	player.currentTime = time;
	player.play();
}

// for (var i = 0; i < links.length; i++) {
// 	var element = links[i];
// 	element.addEventListener('click', function(){
// 		jumpToTime(time_table[i]);
// 	});
// }




