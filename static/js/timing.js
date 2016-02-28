function padDigits(number, digits) {
    return Array(Math.max(digits - String(number).length + 1, 0)).join(0) + number;
}

function startTimer(timing_data) {
    console.log(timing_data)
    var time_display = $('#time');
	var timer = timing_data.localtime;
	var hours = parseInt(timer.hour)
    var minutes = parseInt(timer.minute);
    var seconds = parseInt(timer.second);

	setInterval(
	    function () {
	        seconds = seconds + 1;
	        if (seconds > 59) {
	            minutes = minutes + 1;
	            seconds = 0;
	        }
	        if (minutes > 59) {
	            minutes = 0;
	            hours = hours + 1;
	        }
	        if (hours > 24) {
	            hours = 0;
	        }
	        if (seconds == 0){
	            $("body").css("background-color", "red")
	        }
            time_display.text(hours + ":" + padDigits(minutes,2) + ":" + padDigits(seconds, 2));
        }
	, 1000);
}

function initiateTimer(time) {
    startTimer(JSON.parse(time));
}

jQuery(function ($) {
    var present_url = window.location.href;
    var split_url = present_url.split("/");
    var talk_key = split_url[split_url.length-1];
	$.ajax({url: "/timing_data/" + talk_key, success: initiateTimer })
});
