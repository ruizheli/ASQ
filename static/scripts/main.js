$(document).ready(function(){
	$(".col-md-4").on("click", function(){
		alert("This feature is still under development, please come back later");
	})
	$(".btn").on("click", function(){
		$(location).attr('href', 'upload');
	})
});